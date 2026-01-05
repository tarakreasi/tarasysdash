//go:build windows

package collector

import (
	"os/exec"
	"strings"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/mem"
	"github.com/shirou/gopsutil/v3/net"
)

func (c *Collector) GetMetrics(serviceNames []string) (*SystemMetrics, error) {
	// Same Gopsutil logic as Linux for CPU/Mem/Disk
	v, err := mem.VirtualMemory()
	if err != nil {
		return nil, err
	}

	cStats, err := cpu.Percent(0, false)
	if err != nil {
		return nil, err
	}
	cpuPercent := 0.0
	if len(cStats) > 0 {
		cpuPercent = cStats[0]
	}

	partitions, err := disk.Partitions(false)
	var diskStats []DiskStat
	if err == nil {
		for _, p := range partitions {
			u, err := disk.Usage(p.Mountpoint)
			if err != nil {
				continue
			}
			diskStats = append(diskStats, DiskStat{
				Path:        p.Mountpoint,
				TotalBytes:  u.Total,
				UsedBytes:   u.Used,
				FreePercent: 100.0 - u.UsedPercent,
			})
		}
	}

	// Network
	netStats, err := net.IOCounters(false)
	bytesIn := uint64(0)
	bytesOut := uint64(0)
	if err == nil && len(netStats) > 0 {
		bytesIn = netStats[0].BytesRecv
		bytesOut = netStats[0].BytesSent
	}

	// Windows Service Monitoring via SC QUERY
	var services []ServiceStatus
	for _, name := range serviceNames {
		status := "Unknown"
		running := false
		
		// MVP: Shell out to 'sc query'
		cmd := exec.Command("sc", "query", name)
		output, _ := cmd.CombinedOutput()
		outStr := string(output)
		
		if strings.Contains(outStr, "RUNNING") {
			status = "Running"
			running = true
		} else if strings.Contains(outStr, "STOPPED") {
			status = "Stopped"
		}

		services = append(services, ServiceStatus{
			Name:    name,
			Status:  status,
			Running: running,
		})
	}

	return &SystemMetrics{
		Timestamp:        time.Now().Unix(),
		CPUUsagePercent:  cpuPercent,
		MemoryUsedBytes:  v.Used,
		MemoryTotalBytes: v.Total,
		DiskUsage:        diskStats,
		BytesIn:          bytesIn,
		BytesOut:         bytesOut,
		Services:         services,
	}, nil
}
