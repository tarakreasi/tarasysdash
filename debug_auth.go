package main

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
)

func main() {
	// Simulate GenerateToken
	bytes := make([]byte, 32)
	rand.Read(bytes)
	token := hex.EncodeToString(bytes)
	fmt.Printf("Token: %s\n", token)

	// Simulate HashToken
	hash := sha256.Sum256([]byte(token))
	hashedToken := hex.EncodeToString(hash[:])
	fmt.Printf("Hash:  %s\n", hashedToken)
}
