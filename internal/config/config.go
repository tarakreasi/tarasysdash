package config

import (
	"os"
	"time"
)

type Config struct {
	AgentInterval time.Duration
	LogLevel      string
}

func Load() *Config {
	return &Config{
		AgentInterval: parseDurationEnv("AGENT_INTERVAL", 1*time.Second),
		LogLevel:      parseStringEnv("LOG_LEVEL", "info"),
	}
}

func parseDurationEnv(key string, defaultVal time.Duration) time.Duration {
	if val, exists := os.LookupEnv(key); exists {
		if d, err := time.ParseDuration(val); err == nil {
			return d
		}
	}
	return defaultVal
}

func parseStringEnv(key, defaultVal string) string {
	if val, exists := os.LookupEnv(key); exists {
		return val
	}
	return defaultVal
}
