//go:build linux

package collector

import (
	"math"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/host"
	"github.com/shirou/gopsutil/v3/mem"
	"github.com/shirou/gopsutil/v3/net"
	"github.com/shirou/gopsutil/v3/process"
)

// GetMetrics collects hardware metrics on Linux systems with htop/top standard accuracy.
func (c *Collector) GetMetrics(serviceNames []string) (*SystemMetrics, error) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// 1. Memory Calculation (Aligned with htop & modern Linux free -m)
	// In Linux, true memory occupied by running apps, desktop, and shared shmem is Total - Available.
	v, err := mem.VirtualMemory()
	if err != nil {
		return nil, err
	}

	memUsed := v.Used
	if v.Available > 0 && v.Total >= v.Available {
		memUsed = v.Total - v.Available
	}

	// 2. CPU Calculation (Aligned with htop /proc/stat delta algorithm)
	cpuPercent := 0.0
	currTimes, err := cpu.Times(false)
	if err == nil && len(currTimes) > 0 {
		curr := currTimes[0]
		if c.hasPrevCPU {
			prev := c.prevCPUTimes
			totalPrev := prev.User + prev.System + prev.Nice + prev.Iowait + prev.Irq + prev.Softirq + prev.Steal + prev.Idle
			totalCurr := curr.User + curr.System + curr.Nice + curr.Iowait + curr.Irq + curr.Softirq + curr.Steal + curr.Idle

			idlePrev := prev.Idle + prev.Iowait
			idleCurr := curr.Idle + curr.Iowait

			totalDelta := totalCurr - totalPrev
			idleDelta := idleCurr - idlePrev

			if totalDelta > 0 {
				busyDelta := totalDelta - idleDelta
				cpuPercent = math.Max(0.0, math.Min(100.0, (busyDelta/totalDelta)*100.0))
			}
		} else {
			// First tick fallback
			cStats, err := cpu.Percent(0, false)
			if err == nil && len(cStats) > 0 {
				cpuPercent = cStats[0]
			}
		}
		c.prevCPUTimes = curr
		c.hasPrevCPU = true
	} else {
		// Fallback to gopsutil if Times failed
		cStats, _ := cpu.Percent(0, false)
		if len(cStats) > 0 {
			cpuPercent = cStats[0]
		}
	}

	// 3. Disk (Multi-drive physical partitions)
	partitions, err := disk.Partitions(false)
	if err != nil {
		return nil, err
	}

	var diskStats []DiskStat
	for _, p := range partitions {
		// Filter out snap loops or special filesystems
		if p.Fstype == "squashfs" {
			continue
		}

		u, err := disk.Usage(p.Mountpoint)
		if err != nil {
			continue // Skip permission denied or unready drives
		}

		diskStats = append(diskStats, DiskStat{
			Path:        p.Mountpoint,
			TotalBytes:  u.Total,
			UsedBytes:   u.Used,
			FreePercent: 100.0 - u.UsedPercent,
		})
	}

	// 4. Network: Aggregating all physical NICs
	netStats, err := net.IOCounters(true) // true = per NIC
	bytesIn := uint64(0)
	bytesOut := uint64(0)
	if err == nil {
		for _, ns := range netStats {
			if ns.Name == "lo" {
				continue
			}
			bytesIn += ns.BytesRecv
			bytesOut += ns.BytesSent
		}
	}

	// 5. Host Info (Uptime)
	hostInfo, _ := host.Info()
	uptime := uint64(0)
	if hostInfo != nil {
		uptime = hostInfo.Uptime
	}

	// 6. Processes Count
	procs, _ := process.Processes()
	procCount := len(procs)

	// 7. Temperature Sensor Reading
	temps, _ := host.SensorsTemperatures()
	coreTemp := 0.0
	for _, t := range temps {
		// Heuristic: package or tctl temp
		if t.SensorKey == "coretemp_package_id_0" || t.SensorKey == "k10temp_tctl" {
			coreTemp = t.Temperature
			break
		}
		if coreTemp == 0 && t.Temperature > 0 {
			coreTemp = t.Temperature
		}
	}

	return &SystemMetrics{
		Timestamp:        time.Now().Unix(),
		CPUUsagePercent:  cpuPercent,
		MemoryUsedBytes:  memUsed,
		MemoryTotalBytes: v.Total,
		DiskUsage:        diskStats,
		BytesIn:          bytesIn,
		BytesOut:         bytesOut,
		Services:         []ServiceStatus{},
		UptimeSeconds:    uptime,
		ProcessCount:     procCount,
		Temperature:      coreTemp,
	}, nil
}
