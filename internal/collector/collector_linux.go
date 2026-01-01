//go:build linux

package collector

import (
	"os"
	"strconv"
	"strings"
	"time"
)

func getRootPath() string {
	return "/"
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
