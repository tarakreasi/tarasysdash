package main

import (
	"context"
	"flag"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/tarakreasi/taraSysDash/internal/auth"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func main() {
	// Setup Structured Logging (JSON)
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	slog.SetDefault(logger)

	// CLI Flags
	genToken := flag.Bool("gen-token", false, "Generate a new token for an agent")
	agentID := flag.String("agent-id", "", "Agent ID for token generation")
	flag.Parse()

	// Initialize SQLite Store
	store, err := storage.NewSQLiteStore("tara.db")
	if err != nil {
		slog.Error("Failed to initialize SQLite store", "error", err)
		os.Exit(1)
	}

	// Mode: Token Generation
	if *genToken {
		if *agentID == "" {
			slog.Error("Error: --agent-id is required when generating a token")
			os.Exit(1)
		}

		token, err := auth.GenerateToken()
		if err != nil {
			slog.Error("Failed to generate token", "error", err)
			os.Exit(1)
		}

		hash := auth.HashToken(token)

		// Create/Update agent with this token (Placeholder)
		agent := &storage.Agent{
			ID:       *agentID,
			Hostname: "provisioned",
			OS:       "unknown",
		}
		if err := store.RegisterAgent(context.Background(), agent); err != nil {
			slog.Error("Failed to register agent placeholder", "error", err)
			os.Exit(1)
		}

		if err := store.UpdateAgentToken(context.Background(), *agentID, hash); err != nil {
			slog.Error("Failed to save token hash", "error", err)
			os.Exit(1)
		}

		fmt.Printf("Token generated for Agent %s:\n%s\n", *agentID, token)
		fmt.Println("⚠️  Keep this token safe! It is stored as a hash and cannot be retrieved.")
		os.Exit(0)
	}

	// Mode: HTTP Server
	r := gin.New() // Use New() to avoid default Logger middleware which uses standard log
	r.Use(gin.Recovery())

	// Custom Gin Logger using slog
	r.Use(func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path
		c.Next()
		latency := time.Since(start)
		status := c.Writer.Status()

		slog.Info("HTTP Request",
			"status", status,
			"method", c.Request.Method,
			"path", path,
			"latency", latency.String(),
			"ip", c.ClientIP(),
		)
	})

	// CORS Middleware for local development
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}
		c.Next()
	})

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// Public READ endpoints (no auth)
	r.GET("/api/v1/agents", func(c *gin.Context) {
		agents, err := store.ListAgents(c.Request.Context())
		if err != nil {
			slog.Error("Failed to list agents", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to list agents"})
			return
		}
		c.JSON(http.StatusOK, agents)
	})

	r.PUT("/api/v1/agents/:id/metadata", func(c *gin.Context) {
		agentID := c.Param("id")
		var payload struct {
			RackLocation string  `json:"rack_location"`
			Temperature  float64 `json:"temperature"`
		}
		if err := c.ShouldBindJSON(&payload); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if err := store.UpdateAgentMetadata(c.Request.Context(), agentID, payload.RackLocation, payload.Temperature); err != nil {
			slog.Error("Failed to update metadata", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update metadata"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "updated"})
	})

	r.PUT("/api/v1/agents/:id/hostname", func(c *gin.Context) {
		agentID := c.Param("id")
		var payload struct {
			Hostname string `json:"hostname"`
		}
		if err := c.ShouldBindJSON(&payload); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		if err := store.UpdateAgentHostname(c.Request.Context(), agentID, payload.Hostname); err != nil {
			slog.Error("Failed to update hostname", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update hostname"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "updated", "hostname": payload.Hostname})
	})

	r.GET("/api/v1/metrics/:agent_id", func(c *gin.Context) {
		agentID := c.Param("agent_id")
		limit := 60 // Default: last 60 data points
		metrics, err := store.GetRecentMetrics(c.Request.Context(), agentID, limit)
		if err != nil {
			slog.Error("Failed to get metrics", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get metrics"})
			return
		}
		c.JSON(http.StatusOK, metrics)
	})

	r.GET("/api/v1/metrics/:agent_id/network", func(c *gin.Context) {
		agentID := c.Param("agent_id")
		limit := 60
		metrics, err := store.GetRecentMetrics(c.Request.Context(), agentID, limit)
		if err != nil {
			slog.Error("Failed to get network metrics", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get network metrics"})
			return
		}

		type NetworkStat struct {
			Timestamp int64   `json:"timestamp"`
			BytesIn   uint64  `json:"bytes_in"`
			BytesOut  uint64  `json:"bytes_out"`
			MbpsIn    float64 `json:"mbps_in"`
			MbpsOut   float64 `json:"mbps_out"`
			LatencyMs float64 `json:"latency_ms"`
		}

		var networkStats []NetworkStat
		for i, m := range metrics {
			stat := NetworkStat{
				Timestamp: m.Timestamp,
				BytesIn:   m.BytesIn,
				BytesOut:  m.BytesOut,
				LatencyMs: m.LatencyMs,
			}

			if i > 0 {
				prev := metrics[i-1]
				timeDiff := float64(m.Timestamp - prev.Timestamp)
				if timeDiff > 0 {
					bytesDiffIn := float64(m.BytesIn - prev.BytesIn)
					bytesDiffOut := float64(m.BytesOut - prev.BytesOut)
					stat.MbpsIn = (bytesDiffIn * 8) / (timeDiff * 1000000)
					stat.MbpsOut = (bytesDiffOut * 8) / (timeDiff * 1000000)
				}
			}
			networkStats = append(networkStats, stat)
		}

		c.JSON(http.StatusOK, networkStats)
	})

	r.GET("/api/v1/stats/:agent_id/network", func(c *gin.Context) {
		agentID := c.Param("agent_id")
		limit := 60
		stats, err := store.GetNetworkStats(c.Request.Context(), agentID, limit)
		if err != nil {
			slog.Error("Failed to get network stats", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get network stats"})
			return
		}
		c.JSON(http.StatusOK, stats)
	})

	r.GET("/api/v1/stats/:agent_id/latency", func(c *gin.Context) {
		agentID := c.Param("agent_id")
		limit := 60
		stats, err := store.GetLatencyStats(c.Request.Context(), agentID, limit)
		if err != nil {
			slog.Error("Failed to get latency stats", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get latency stats"})
			return
		}
		c.JSON(http.StatusOK, stats)
	})

	r.GET("/api/v1/agents/rack/:rack_id", func(c *gin.Context) {
		rackID := c.Param("rack_id")
		agents, err := store.ListAgentsByRack(c.Request.Context(), rackID)
		if err != nil {
			slog.Error("Failed to list agents by rack", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to list agents"})
			return
		}
		c.JSON(http.StatusOK, agents)
	})

	// Authenticated Group
	api := r.Group("/api/v1")
	api.Use(authMiddleware(store))
	{
		// AGENT HANDSHAKE / REGISTER
		// Agents MUST call this on startup to sync their Hostname/OS/IP
		api.POST("/register", func(c *gin.Context) {
			var agent storage.Agent
			if err := c.ShouldBindJSON(&agent); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}

			// Security check: Ensure the authenticated token matches the agent ID claiming to register?
			// For now, we trust the token. But strictly we should match `agentID` from context.
			authenticatedAgentID := c.GetString("agentID")
			if authenticatedAgentID != agent.ID {
				// Allow registration ONLY if it matches the token owner
				c.JSON(http.StatusForbidden, gin.H{"error": "Agent ID mismatch with token"})
				return
			}

			if err := store.RegisterAgent(c.Request.Context(), &agent); err != nil {
				slog.Error("Failed to register agent", "error", err)
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to register agent"})
				return
			}

			slog.Info("Agent Registered/Updated", "id", agent.ID, "os", agent.OS, "ip", c.ClientIP())
			c.JSON(http.StatusOK, gin.H{"status": "registered", "config": gin.H{"interval": 1}})
		})

		api.POST("/metrics", func(c *gin.Context) {
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

			authenticatedAgentID := c.GetString("agentID")
			if authenticatedAgentID != payload.AgentID {
				c.JSON(http.StatusForbidden, gin.H{"error": "Agent ID mismatch"})
				return
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
				slog.Error("Failed to save metrics", "error", err)
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save metrics"})
				return
			}

			c.JSON(http.StatusOK, gin.H{"status": "recorded"})
		})
	}

	slog.Info("Server executing on :8080")
	if err := r.Run(":8080"); err != nil {
		slog.Error("Server failed", "error", err)
		os.Exit(1)
	}
}

func authMiddleware(store *storage.SQLiteStore) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Missing Authorization header"})
			return
		}

		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Invalid Authorization format"})
			return
		}

		token := parts[1]
		hash := auth.HashToken(token)

		agentID, err := store.GetAgentIDByTokenHash(c.Request.Context(), hash)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			return
		}

		// Valid! Pass agentID to context
		c.Set("agentID", agentID)
		c.Next()
	}
}
