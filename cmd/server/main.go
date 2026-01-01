package main

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func main() {
	// Initialize SQLite Store
	store, err := storage.NewSQLiteStore("tara.db")
	if err != nil {
		log.Fatalf("Failed to initialize SQLite store: %v", err)
	}

	r := gin.Default()

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	r.POST("/api/v1/metrics", func(c *gin.Context) {
		var payload struct {
			AgentID   string  `json:"agent_id"`
			Timestamp int64   `json:"timestamp"`
			CPU       float64 `json:"cpu_usage_percent"`
			MemUsed   uint64  `json:"memory_used_bytes"`
			MemTotal  uint64  `json:"memory_total_bytes"`
			DiskFree  float64 `json:"disk_free_percent"`
		}

		if err := c.ShouldBindJSON(&payload); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// Register/Update Agent
		agent := &storage.Agent{
			ID:        payload.AgentID,
			Hostname:  "unknown", // To be enhanced
			IPAddress: c.ClientIP(),
			OS:        "linux", // To be enhanced
		}
		if err := store.RegisterAgent(c.Request.Context(), agent); err != nil {
			log.Printf("Error registering agent: %v", err)
		}

		// Save Metric
		metric := &storage.Metric{
			Timestamp:        payload.Timestamp,
			CPUUsagePercent:  payload.CPU,
			MemoryUsedBytes:  payload.MemUsed,
			MemoryTotalBytes: payload.MemTotal,
			DiskFreePercent:  payload.DiskFree,
		}

		if err := store.SaveMetric(c.Request.Context(), payload.AgentID, metric); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save metrics"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"status": "recorded"})
	})

	log.Println("Server executing on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
