package collector

import (
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/host"
	"github.com/shirou/gopsutil/v3/mem"
	"github.com/shirou/gopsutil/v3/net"
	"github.com/shirou/gopsutil/v3/process"
)

// Structs are defined in collector.go

func (c *Collector) GetMetrics(serviceNames []string) (*SystemMetrics, error) {
	// Memory
	v, err := mem.VirtualMemory()
	if err != nil {
		return nil, err
	}

	// CPU
	cStats, err := cpu.Percent(0, false)
	if err != nil {
		return nil, err
	}
	cpuPercent := 0.0
	if len(cStats) > 0 {
		cpuPercent = cStats[0]
	}

	// Disk (Multi-drive)
	partitions, err := disk.Partitions(false)
	if err != nil {
		return nil, err
	}

	var diskStats []DiskStat
	for _, p := range partitions {
		// Filter out snap loops or special filesystems if needed, but for now take all "physical"
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

	// Network: Aggregating all NICs for consistency
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

	// Host Info (Uptime)
	hostInfo, _ := host.Info()
	uptime := uint64(0)
	if hostInfo != nil {
		uptime = hostInfo.Uptime
	}

	// Processes
	procs, _ := process.Processes()
	procCount := len(procs)

	// Temperature
	temps, _ := host.SensorsTemperatures()
	coreTemp := 0.0
	for _, t := range temps {
		// Heuristic: try to find "core" or "package" id
		if t.SensorKey == "coretemp_package_id_0" || t.SensorKey == "k10temp_tctl" {
			coreTemp = t.Temperature
			break
		}
		// Fallback: take first non-zero
		if coreTemp == 0 && t.Temperature > 0 {
			coreTemp = t.Temperature
		}
	}

	return &SystemMetrics{
		Timestamp:        time.Now().Unix(),
		CPUUsagePercent:  cpuPercent,
		MemoryUsedBytes:  v.Used,
		MemoryTotalBytes: v.Total,
		DiskUsage:        diskStats,
		BytesIn:          bytesIn,
		BytesOut:         bytesOut,
		Services:         []ServiceStatus{}, // Stub for Linux
		UptimeSeconds:    uptime,
		ProcessCount:     procCount,
		Temperature:      coreTemp,
	}, nil
}
