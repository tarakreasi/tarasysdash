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

	if len(metrics.DiskUsage) == 0 {
		t.Error("Expected at least one disk in DiskUsage")
	} else {
		for _, d := range metrics.DiskUsage {
			if d.FreePercent < 0 || d.FreePercent > 100 {
				t.Errorf("DiskFreePercent out of range for %s: %f", d.Path, d.FreePercent)
			}
		}
	}

	// Network might be 0, but field should exist (struct check is implicit by compilation)
	// We can't really assert > 0 unless we force traffic.
	t.Logf("BytesIn: %d, BytesOut: %d", metrics.BytesIn, metrics.BytesOut)

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
