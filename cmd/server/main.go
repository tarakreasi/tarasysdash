package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/tarakreasi/taraSysDash/internal/auth"
	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func main() {
	// CLI Flags
	genToken := flag.Bool("gen-token", false, "Generate a new token for an agent")
	agentID := flag.String("agent-id", "", "Agent ID for token generation")
	flag.Parse()

	// Initialize SQLite Store
	store, err := storage.NewSQLiteStore("tara.db")
	if err != nil {
		log.Fatalf("Failed to initialize SQLite store: %v", err)
	}

	// Mode: Token Generation
	if *genToken {
		if *agentID == "" {
			log.Fatal("Error: --agent-id is required when generating a token")
		}

		token, err := auth.GenerateToken()
		if err != nil {
			log.Fatalf("Failed to generate token: %v", err)
		}

		hash := auth.HashToken(token)

		// Create/Update agent with this token
		// We need to ensure agent exists or insert it. RegisterAgent does upsert.
		agent := &storage.Agent{
			ID:       *agentID,
			Hostname: "provisioned",
			OS:       "unknown",
		}
		if err := store.RegisterAgent(context.Background(), agent); err != nil {
			log.Fatalf("Failed to register agent placeholder: %v", err)
		}

		if err := store.UpdateAgentToken(context.Background(), *agentID, hash); err != nil {
			log.Fatalf("Failed to save token hash: %v", err)
		}

		fmt.Printf("Token generated for Agent %s:\n%s\n", *agentID, token)
		fmt.Println("⚠️  Keep this token safe! It is stored as a hash and cannot be retrieved.")
		os.Exit(0)
	}

	// Mode: HTTP Server
	r := gin.Default()

	// CORS Middleware for local development
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
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
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update metadata"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "updated"})
	})

	r.GET("/api/v1/metrics/:agent_id", func(c *gin.Context) {
		agentID := c.Param("agent_id")
		limit := 60 // Default: last 60 data points
		metrics, err := store.GetRecentMetrics(c.Request.Context(), agentID, limit)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get metrics"})
			return
		}
		c.JSON(http.StatusOK, metrics)
	})

	// Authenticated Group
	api := r.Group("/api/v1")
	api.Use(authMiddleware(store))
	{
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

			// Validate that the token used belongs to the agent_id in payload?
			// For Sprint 3, we just check if token is valid for ANY agent, and maybe verify match.
			// Let's enforce: Return 403 if token's associated agentID != payload.agentID
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
				c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save metrics"})
				return
			}

			c.JSON(http.StatusOK, gin.H{"status": "recorded"})
		})
	}

	log.Println("Server executing on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Server failed: %v", err)
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
			// Either DB error or not found (sql.ErrNoRows).
			// We treat as Unauthorized.
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			return
		}

		// Valid! Pass agentID to context
		c.Set("agentID", agentID)
		c.Next()
	}
}
