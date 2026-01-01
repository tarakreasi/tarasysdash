//go:build windows

package collector

func getRootPath() string {
	return "C:\\"
}

// collectNetworkStats is a placeholder for Windows.
// Note: This is currently unused in the main GetMetrics loop.
func collectNetworkStats() (bytesIn, bytesOut uint64, err error) {
	return 0, 0, nil
}

// measureLatency is a placeholder for Windows.
// Note: This is currently unused in the main GetMetrics loop.
func measureLatency() float64 {
	return 0.0
}
