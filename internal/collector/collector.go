package collector

import (
	"time"
)

type DiskStat struct {
	Path        string  `json:"path"`
	TotalBytes  uint64  `json:"total_bytes"`
	UsedBytes   uint64  `json:"used_bytes"`
	FreePercent float64 `json:"free_percent"`
}

type ServiceStatus struct {
	Name    string `json:"name"`
	Status  string `json:"status"` // "Running", "Stopped", "Unknown"
	Running bool   `json:"running"`
}

type SystemMetrics struct {
	Timestamp        int64           `json:"timestamp"`
	CPUUsagePercent  float64         `json:"cpu_usage_percent"`
	MemoryUsedBytes  uint64          `json:"memory_used_bytes"`
	MemoryTotalBytes uint64          `json:"memory_total_bytes"`
	DiskUsage        []DiskStat      `json:"disk_usage"`
	BytesIn          uint64          `json:"bytes_in"`
	BytesOut         uint64          `json:"bytes_out"`
	LatencyMs        float64         `json:"latency_ms"`
	Services         []ServiceStatus `json:"services"`
}

type Collector struct {
	prevNetTime  time.Time
	prevBytesIn  uint64
	prevBytesOut uint64
}

func New() *Collector {
	return &Collector{}
}
