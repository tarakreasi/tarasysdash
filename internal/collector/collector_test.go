package collector

import (
	"testing"
)

func TestGetMetrics(t *testing.T) {
	col := New()
	metrics, err := col.GetMetrics()
	if err != nil {
		t.Fatalf("Failed to get metrics: %v", err)
	}

	if metrics == nil {
		t.Fatal("Expected metrics to be non-nil")
	}

	if metrics.Timestamp == 0 {
		t.Error("Expected timestamp to be set")
	}

	// Basic sanity checks
	if metrics.MemoryTotalBytes == 0 {
		t.Error("Expected MemoryTotalBytes > 0")
	}

	if metrics.DiskFreePercent < 0 || metrics.DiskFreePercent > 100 {
		t.Errorf("DiskFreePercent out of range: %f", metrics.DiskFreePercent)
	}

	// CPU might be 0 on first run or idle, but verify it's a valid percentage
	if metrics.CPUUsagePercent < 0 || metrics.CPUUsagePercent > 100 {
		t.Errorf("CPUUsagePercent out of range: %f", metrics.CPUUsagePercent)
	}

	t.Logf("Got metrics: %+v", metrics)
}

func TestGetRootPath(t *testing.T) {
	path := getRootPath()
	if path == "" {
		t.Error("Expected root path to be non-empty")
	}
	t.Logf("Root path is: %s", path)
}
