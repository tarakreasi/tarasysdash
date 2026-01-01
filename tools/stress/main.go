package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"sync"
	"sync/atomic"
	"time"
)

type AgentConfig struct {
	ID       string `json:"id"`
	Hostname string `json:"hostname"`
	OS       string `json:"os"`
	IP       string `json:"ip_address"`
}

type MetricPayload struct {
	AgentID   string  `json:"agent_id"`
	Timestamp int64   `json:"timestamp"`
	CPU       float64 `json:"cpu_usage_percent"`
	MemUsed   uint64  `json:"memory_used_bytes"`
	MemTotal  uint64  `json:"memory_total_bytes"`
	DiskFree  float64 `json:"disk_free_percent"`
}

var (
	successCount int64
	failCount    int64
	serverURL    string
	token        string // We'll just use a fixed mock token or require one passed in
)

func main() {
	agents := flag.Int("agents", 50, "Number of concurrent agents")
	duration := flag.Duration("duration", 60*time.Second, "Test duration")
	url := flag.String("url", "http://localhost:8080/api/v1", "API Base URL")
	authToken := flag.String("token", "", "Bearer token for authentication")
	flag.Parse()

	serverURL = *url
	token = *authToken

	if token == "" {
		log.Fatal("Please provide a valid token with -token (use the one generated in Sprint 1)")
	}

	log.Printf("Starting stress test with %d agents for %v...", *agents, *duration)
	log.Printf("Target OS Mix: Windows Server, Windows 10/11, Windows IoT")

	var wg sync.WaitGroup
	wg.Add(*agents)

	// OS Options requested by user
	osTypes := []string{
		"Windows Server 2022 Datacenter",
		"Windows Server 2019 Standard",
		"Windows 11 Enterprise",
		"Windows 10 Pro",
		"Windows 10 IoT Core",
	}

	start := time.Now()

	for i := 0; i < *agents; i++ {
		go func(id int) {
			defer wg.Done()

			agentID := fmt.Sprintf("sim-agent-%d", id)
			osType := osTypes[rand.Intn(len(osTypes))]

			// Jitter: Stagger start times to avoid Thundering Herd on registration
			time.Sleep(time.Duration(rand.Intn(2000)) * time.Millisecond)

			// 1. Register (Handshake)
			if err := registerAgent(agentID, osType); err != nil {
				log.Printf("[%s] Registration failed: %v", agentID, err)
				atomic.AddInt64(&failCount, 1)
				return
			}

			// 2. Loop Metrics
			ticker := time.NewTicker(1 * time.Second)
			defer ticker.Stop()

			timeout := time.After(*duration)

			for {
				select {
				case <-timeout:
					return
				case <-ticker.C:
					if err := sendMetric(agentID); err != nil {
						// log.Printf("[%s] Metric failed: %v", agentID, err) // Verbose
						atomic.AddInt64(&failCount, 1)
					} else {
						atomic.AddInt64(&successCount, 1)
					}
				}
			}
		}(i)
	}

	wg.Wait()
	elapsed := time.Since(start)

	log.Println("==================================================")
	log.Printf("Stress Test Complete in %v", elapsed)
	log.Printf("Total Requests: %d", successCount+failCount)
	log.Printf("Success: %d", successCount)
	log.Printf("Failed:  %d", failCount)

	successRate := float64(successCount) / float64(successCount+failCount) * 100
	log.Printf("Success Rate: %.2f%%", successRate)
	log.Println("==================================================")

	if successRate < 99.0 {
		log.Fatal("Stress Test FAILED: Success rate < 99%")
	}
}

func registerAgent(id, osType string) error {
	payload := AgentConfig{
		ID:       id,
		Hostname: fmt.Sprintf("WIN-NODE-%s", id),
		OS:       osType,
		IP:       "10.0.0.x",
	}

	data, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", serverURL+"/register", bytes.NewBuffer(data))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+token)

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("bad status: %d", resp.StatusCode)
	}
	return nil
}

func sendMetric(id string) error {
	payload := MetricPayload{
		AgentID:   id,
		Timestamp: time.Now().Unix(),
		CPU:       rand.Float64() * 100,
		MemUsed:   1024 * 1024 * 100,       // 100MB
		MemTotal:  1024 * 1024 * 1024 * 16, // 16GB
		DiskFree:  50.0 + rand.Float64()*50,
	}

	data, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", serverURL+"/metrics", bytes.NewBuffer(data))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+token)

	client := &http.Client{Timeout: 2 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("bad status: %d", resp.StatusCode)
	}
	return nil
}
