package collector

import (
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

	dStats, err := disk.Usage(getRootPath())
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
