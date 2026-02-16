//go:build windows

package collector

import (
	"log/slog"
	"os/exec"
	"strings"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/host"
	"github.com/shirou/gopsutil/v3/mem"
	"github.com/shirou/gopsutil/v3/net"
	"github.com/shirou/gopsutil/v3/process"
)

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

	// Disk
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

	// Network: Aggregating all NICs for Multi-NIC support (e.g. REC 7, REC 02)
	netStats, err := net.IOCounters(true) // true = per NIC
	bytesIn := uint64(0)
	bytesOut := uint64(0)
	if err == nil {
		for _, ns := range netStats {
			lowName := strings.ToLower(ns.Name)

			// Aggressively filter out loopback and virtual tunnel adapters
			if strings.Contains(lowName, "loopback") ||
				strings.Contains(lowName, "isatap") ||
				strings.Contains(lowName, "teredo") ||
				strings.Contains(lowName, "pseudo") ||
				strings.Contains(lowName, "tunnel") ||
				ns.Name == "lo" {
				continue
			}

			// Add to total
			bytesIn += ns.BytesRecv
			bytesOut += ns.BytesSent

			// Detailed logging to help user identify which NICs are seen
			slog.Info("NIC Detected", "interface", ns.Name, "rx_bytes", ns.BytesRecv, "tx_bytes", ns.BytesSent)
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

	// Temperature (Sensors on Windows are often limited/require admin/HID)
	temps, _ := host.SensorsTemperatures()
	coreTemp := 0.0
	if len(temps) > 0 {
		coreTemp = temps[0].Temperature
	}

	// Windows Service Monitoring via SC QUERY
	var services []ServiceStatus
	for _, name := range serviceNames {
		status := "Unknown"
		running := false

		// MVP: Shell out to 'sc query'
		// Note: We wrap name in quotes to handle spaces
		cmd := exec.Command("sc", "query", name)
		output, _ := cmd.CombinedOutput()
		outStr := strings.ToUpper(string(output))

		if strings.Contains(outStr, "RUNNING") || strings.Contains(outStr, "STATE              : 4  RUNNING") {
			status = "Running"
			running = true
		} else if strings.Contains(outStr, "STOPPED") || strings.Contains(outStr, "STATE              : 1  STOPPED") {
			status = "Stopped"
		} else if strings.Contains(outStr, "1060") { // The specified service does not exist
			status = "Not Found"
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
		UptimeSeconds:    uptime,
		ProcessCount:     procCount,
		Temperature:      coreTemp,
	}, nil
}
