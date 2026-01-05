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
	"github.com/tarakreasi/taraSysDash/internal/alert"
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

	// AGENT HANDSHAKE / REGISTER (Public for Bootstrapping)
	r.POST("/api/v1/register", func(c *gin.Context) {
		var agent storage.Agent
		if err := c.ShouldBindJSON(&agent); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// In a real prod env, we might want a "Shared Secret" header here to prevent spam.
		// For MVP/Air-gapped env, public register is acceptable.

		// Generate a token for the agent
		token, err := auth.GenerateToken()
		if err != nil {
			slog.Error("Failed to generate token", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to generate token"})
			return
		}
		tokenHash := auth.HashToken(token)

		// Register with the new token hash
		if err := store.RegisterAgent(c.Request.Context(), &agent); err != nil {
			slog.Error("Failed to register agent", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to register agent"})
			return
		}

		// Update the token hash in DB
		if err := store.UpdateAgentToken(c.Request.Context(), agent.ID, tokenHash); err != nil {
			slog.Error("Failed to update agent token", "error", err)
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update agent token"})
			return
		}

		slog.Info("Agent Registered", "id", agent.ID, "os", agent.OS, "ip", c.ClientIP())
		// Return the RAW token to the agent (ONLY ONCE)
		c.JSON(http.StatusOK, gin.H{
			"status": "registered",
			"token":  token,
			"config": gin.H{"interval": 1},
		})
	})

	r.PUT("/api/v1/agents/:id/metadata", func(c *gin.Context) {
		agentID := c.Param("id")
		var payload struct {
			RackLocation string  `json:"rack_location"`
			Temperature  float64 `json:"temperature"`
			LogRetention int     `json:"log_retention_days"`
		}
		if err := c.ShouldBindJSON(&payload); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// Validation (optional)
		if payload.LogRetention <= 0 {
			payload.LogRetention = 30 // Default fallback
		}

		if err := store.UpdateAgentMetadata(c.Request.Context(), agentID, payload.RackLocation, payload.Temperature, payload.LogRetention); err != nil {
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

	// PUBLIC: AGENT HANDSHAKE / REGISTER
	// Agents call this on startup to sync their Hostname/OS/IP.
	// We allow this to be public for the MVP ease-of-use (Auto-Discovery).

	// Authenticated Group
	api := r.Group("/api/v1")
	api.Use(authMiddleware(store))
	{
		// METRICS (Must be authenticated)

		api.POST("/metrics", func(c *gin.Context) {
			var payload struct {
				AgentID   string             `json:"agent_id"`
				Timestamp int64              `json:"timestamp"`
				CPU       float64            `json:"cpu_usage_percent"`
				MemUsed   uint64             `json:"memory_used_bytes"`
				MemTotal  uint64             `json:"memory_total_bytes"`
				DiskUsage []storage.DiskStat `json:"disk_usage"` // New List
				// Fallback/Legacy
				DiskFree float64 `json:"disk_free_percent"`
				BytesIn  uint64  `json:"bytes_in"`
				BytesOut uint64  `json:"bytes_out"`
			}
			// Note: Existing agents sending 'disk_free_percent' will still bind to DiskFree.
			// New agents will send 'disk_usage'.

			if err := c.ShouldBindJSON(&payload); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}

			authenticatedAgentID := c.GetString("agentID")
			if authenticatedAgentID != payload.AgentID {
				c.JSON(http.StatusForbidden, gin.H{"error": "Agent ID mismatch"})
				return
			}

			// Map to storage Metric
			metric := &storage.Metric{
				Timestamp:        payload.Timestamp,
				CPUUsagePercent:  payload.CPU,
				MemoryUsedBytes:  payload.MemUsed,
				MemoryTotalBytes: payload.MemTotal,
				DiskUsage:        payload.DiskUsage,
				BytesIn:          payload.BytesIn,
				BytesOut:         payload.BytesOut,
			}
			// Compatibility for legacy frontend or logic relying on DiskFreePercent
			if len(metric.DiskUsage) == 0 && payload.DiskFree > 0 {
				metric.DiskUsage = []storage.DiskStat{
					{Path: "/", FreePercent: payload.DiskFree},
				}
			}

			if err := store.SaveMetric(c.Request.Context(), payload.AgentID, metric); err != nil {
				slog.Error("Failed to save metrics", "error", err)
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save metrics"})
				return
			}

			c.JSON(http.StatusOK, gin.H{"status": "recorded"})
		})
	}

	// Alert Service
	alertCfg := alert.Config{
		SMTPHost:       os.Getenv("SMTP_HOST"),
		SMTPPort:       os.Getenv("SMTP_PORT"),
		SMTPUser:       os.Getenv("SMTP_USER"),
		SMTPPass:       os.Getenv("SMTP_PASS"),
		RecipientEmail: os.Getenv("ALERT_RECIPIENTS"),
	}
	// Defaults
	if alertCfg.SMTPHost == "" {
		alertCfg.SMTPHost = "smtp.gmail.com"
	}
	if alertCfg.SMTPPort == "" {
		alertCfg.SMTPPort = "587"
	}

	alertService := alert.NewService(alertCfg)

	// Watchdog Loop (Background)
	go func() {
		ticker := time.NewTicker(60 * time.Second)
		defer ticker.Stop()
		for range ticker.C {
			ctx := context.Background()
			agents, err := store.ListAgents(ctx)
			if err != nil {
				slog.Error("Watchdog: Failed to list agents", "error", err)
				continue
			}

			for _, agent := range agents {
				// 1. Check Offline & Disk Alert
				// We need the latest metric for disk check
				metrics, _ := store.GetRecentMetrics(ctx, agent.ID, 1) // Ignore error, might be empty
				var lastMetric *storage.Metric
				if len(metrics) > 0 {
					lastMetric = &metrics[0]
				}

				alertService.CheckAndSend(agent, lastMetric)
			}

			// 2. Cleanup Old Data (Run once per 24h ideally, but here every minute with check usually,
			// or just run it. Deleting a few rows every minute is better than millions at once).
			// Here we iterate all agents.
			for _, agent := range agents {
				retention := agent.LogRetentionDays
				if retention <= 0 {
					retention = 30
				}
				if err := store.DeleteOldMetrics(ctx, agent.ID, retention); err != nil {
					slog.Warn("Failed to cleanup old metrics", "agent", agent.ID)
				}
			}
		}
	}()

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
			slog.Error("Auth Failed", "error", err, "token_hash_preview", hash[:10])
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			return
		}

		// Valid! Pass agentID to context
		c.Set("agentID", agentID)
		c.Next()
	}
}
