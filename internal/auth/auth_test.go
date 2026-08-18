package auth

import (
	"testing"
)

func TestGenerateToken(t *testing.T) {
	token1, err := GenerateToken()
	if err != nil {
		t.Fatalf("GenerateToken failed: %v", err)
	}

	// 32 bytes hex encoded = 64 hex characters
	if len(token1) != 64 {
		t.Errorf("expected token length 64, got %d", len(token1))
	}

	token2, err := GenerateToken()
	if err != nil {
		t.Fatalf("GenerateToken second call failed: %v", err)
	}

	if token1 == token2 {
		t.Errorf("expected unique tokens, but got identical values: %s", token1)
	}
}

func TestHashToken(t *testing.T) {
	token := "sample-token-for-testing-12345"
	hash1 := HashToken(token)
	hash2 := HashToken(token)

	// SHA-256 hex string is 64 characters
	if len(hash1) != 64 {
		t.Errorf("expected hash length 64, got %d", len(hash1))
	}

	// Hash must be deterministic
	if hash1 != hash2 {
		t.Errorf("expected deterministic hash output, got %s != %s", hash1, hash2)
	}

	// Different input must produce different hash
	diffHash := HashToken("different-token")
	if hash1 == diffHash {
		t.Errorf("expected different hashes for different inputs")
	}
}
