package alert

import (
	"fmt"
	"log/slog"
	"net/smtp"
	"sync"
	"time"

	"github.com/tarakreasi/taraSysDash/internal/storage"
)

type Config struct {
	SMTPHost       string
	SMTPPort       string
	SMTPUser       string
	SMTPPass       string
	RecipientEmail string
}

type AlertService struct {
	config       Config
	lastSent     sync.Map // map[string]time.Time (Key: "agentID:alertType")
	debounceTime time.Duration
}

func NewService(cfg Config) *AlertService {
	return &AlertService{
		config:       cfg,
		debounceTime: 60 * time.Minute,
	}
}

func (s *AlertService) SendEmail(subject, body string) error {
	if s.config.SMTPHost == "" || s.config.SMTPUser == "" {
		slog.Warn("SMTP not configured. Skipping email.", "subject", subject)
		return nil
	}

	auth := smtp.PlainAuth("", s.config.SMTPUser, s.config.SMTPPass, s.config.SMTPHost)
	to := []string{s.config.RecipientEmail}
	msg := []byte("To: " + s.config.RecipientEmail + "\r\n" +
		"Subject: " + subject + "\r\n" +
		"\r\n" +
		body + "\r\n")

	addr := s.config.SMTPHost + ":" + s.config.SMTPPort
	err := smtp.SendMail(addr, auth, s.config.SMTPUser, to, msg)
	if err != nil {
		slog.Error("Failed to send email", "error", err)
		return err
	}
	slog.Info("Email sent successfully", "subject", subject)
	return nil
}

func (s *AlertService) CheckAndSend(agent storage.Agent, metric *storage.Metric) {
	// 1. Check Offline
	if agent.Status == "offline" { // Assumes calling code set this status based on LastSeen
		s.triggerAlert(agent, "OFFLINE", fmt.Sprintf("CRITICAL: Agent %s (%s) is OFFLINE. Last seen: %s", agent.Hostname, agent.ID, agent.UpdatedAt))
	}

	// 2. Check Disk
	if metric != nil && len(metric.DiskUsage) > 0 {
		for _, disk := range metric.DiskUsage {
			if disk.FreePercent < 5.0 {
				s.triggerAlert(agent, "DISK_FULL:"+disk.Path, fmt.Sprintf("CRITICAL: Disk %s on %s (%s) is at %.2f%% free.", disk.Path, agent.Hostname, agent.ID, disk.FreePercent))
			}
		}
	} else if metric != nil && metric.DiskFreePercent < 5.0 && metric.DiskFreePercent > 0 {
		// Legacy fallback
		s.triggerAlert(agent, "DISK_FULL:Legacy", fmt.Sprintf("CRITICAL: Disk on %s (%s) is at %.2f%% free.", agent.Hostname, agent.ID, metric.DiskFreePercent))
	}
}

func (s *AlertService) triggerAlert(agent storage.Agent, alertType, message string) {
	key := agent.ID + ":" + alertType

	last, ok := s.lastSent.Load(key)
	if ok {
		lastTime := last.(time.Time)
		if time.Since(lastTime) < s.debounceTime {
			// Debounced
			return
		}
	}

	// Send
	err := s.SendEmail("TaraSysDash Alert: "+alertType, message)
	if err == nil {
		s.lastSent.Store(key, time.Now())
	}
}
