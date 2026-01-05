package agent

import (
	"testing"
)

func TestGetMACAddressID(t *testing.T) {
	id, err := GetMACAddressID()
	if err != nil {
		t.Fatalf("Failed to get MAC address ID: %v", err)
	}

	if id == "" {
		t.Fatal("Expected non-empty ID")
	}

	// Should start with "agent-"
	if len(id) < 7 || id[:6] != "agent-" {
		t.Errorf("Expected ID to start with 'agent-', got: %s", id)
	}

	t.Logf("Generated ID: %s", id)

	// Test consistency - calling twice should return same ID
	id2, err := GetMACAddressID()
	if err != nil {
		t.Fatalf("Failed to get MAC address ID on second call: %v", err)
	}

	if id != id2 {
		t.Errorf("Expected consistent ID, got %s and %s", id, id2)
	}
}

func TestGetOrGenerateAgentID(t *testing.T) {
	// Test with provided ID
	providedID := "custom-id-123"
	result, err := GetOrGenerateAgentID(providedID)
	if err != nil {
		t.Fatalf("Failed with provided ID: %v", err)
	}
	if result != providedID {
		t.Errorf("Expected %s, got %s", providedID, result)
	}

	// Test with empty ID (should generate from MAC)
	result, err = GetOrGenerateAgentID("")
	if err != nil {
		t.Fatalf("Failed to generate ID: %v", err)
	}
	if result == "" {
		t.Error("Expected non-empty generated ID")
	}
	if len(result) < 7 || result[:6] != "agent-" {
		t.Errorf("Expected generated ID to start with 'agent-', got: %s", result)
	}

	t.Logf("Generated ID from empty string: %s", result)
}
