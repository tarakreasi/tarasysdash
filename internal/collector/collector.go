package collector

import (
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/mem"
)

type SystemMetrics struct {
	Timestamp        int64   `json:"timestamp"`
	CPUUsagePercent  float64 `json:"cpu_usage_percent"`
	MemoryUsedBytes  uint64  `json:"memory_used_bytes"`
	MemoryTotalBytes uint64  `json:"memory_total_bytes"`
	DiskFreePercent  float64 `json:"disk_free_percent"`
	BytesIn          uint64  `json:"bytes_in"`
	BytesOut         uint64  `json:"bytes_out"`
	LatencyMs        float64 `json:"latency_ms"`
}

type Collector struct{}

func New() *Collector {
	return &Collector{}
}

func (c *Collector) GetMetrics() (*SystemMetrics, error) {
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

	dStats, err := disk.Usage("/")
	if err != nil {
		return nil, err
	}

	return &SystemMetrics{
		Timestamp:        time.Now().Unix(),
		CPUUsagePercent:  cpuPercent,
		MemoryUsedBytes:  v.Used,
		MemoryTotalBytes: v.Total,
		DiskFreePercent:  100.0 - dStats.UsedPercent,
	}, nil
}

func collectNetworkStats() (bytesIn, bytesOut uint64, err error) {
	data, err := os.ReadFile("/proc/net/dev")
	if err != nil {
		return 0, 0, err
	}

	lines := strings.Split(string(data), "\n")
	for _, line := range lines {
		fields := strings.Fields(line)
		if len(fields) < 10 {
			continue
		}
		// Skip loopback
		if strings.HasPrefix(fields[0], "lo:") {
			continue
		}
		// First interface with traffic (eth0, ens, etc)
		if strings.Contains(fields[0], ":") {
			in, _ := strconv.ParseUint(fields[1], 10, 64)
			out, _ := strconv.ParseUint(fields[9], 10, 64)
			bytesIn += in
			bytesOut += out
		}
	}
	return bytesIn, bytesOut, nil
}

func measureLatency() float64 {
	start := time.Now()
	// Simple self-test: measure time to read /proc/stat
	_, err := os.ReadFile("/proc/stat")
	if err != nil {
		return 0
	}
	return float64(time.Since(start).Microseconds()) / 1000.0
}
