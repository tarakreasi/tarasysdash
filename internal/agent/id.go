package agent

import (
	"fmt"
	"net"
	"os"
	"strings"
)

// GetOrGenerateAgentID returns the provided ID if non-empty,
// otherwise generates a deterministic ID based on hostname or MAC address.
func GetOrGenerateAgentID(providedID string) (string, error) {
	if providedID != "" {
		return providedID, nil
	}

	// Try hostname first
	if id, err := GetHostnameID(); err == nil {
		return id, nil
	}

	// Fallback to MAC address
	return GetMACAddressID()
}

// GetHostnameID returns the system hostname as the agent ID.
func GetHostnameID() (string, error) {
	hostname, err := os.Hostname()
	if err != nil || hostname == "" {
		return "", fmt.Errorf("failed to get hostname: %w", err)
	}
	return hostname, nil
}

// GetMACAddressID generates an agent ID based on the first non-loopback network interface MAC address.
func GetMACAddressID() (string, error) {
	interfaces, err := net.Interfaces()
	if err != nil {
		return "", fmt.Errorf("failed to get network interfaces: %w", err)
	}

	// Find first non-loopback interface with a hardware address
	for _, iface := range interfaces {
		// Skip loopback and interfaces without MAC
		if iface.Flags&net.FlagLoopback != 0 || len(iface.HardwareAddr) == 0 {
			continue
		}

		// Found valid interface
		mac := iface.HardwareAddr.String()
		if mac != "" {
			// Format: agent-<mac> (e.g., agent-00:1a:2b:3c:4d:5e)
			// Remove colons for cleaner ID
			cleanMAC := strings.ReplaceAll(mac, ":", "")
			return fmt.Sprintf("agent-%s", cleanMAC), nil
		}
	}

	return "", fmt.Errorf("no valid network interface found")
}
