package alert

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log/slog"
	"net/http"
	"net/smtp"
	"sync"
	"time"

	"github.com/tarakreasi/taraSysDash/internal/storage"
)

type Config struct {
	SMTPHost          string
	SMTPPort          string
	SMTPUser          string
	SMTPPass          string
	RecipientEmail    string
	TelegramBotToken  string
	TelegramChatID    string
	TelegramAPIBase   string // Optional: for testing / custom proxy, defaults to "https://api.telegram.org"
	DiscordWebhookURL string
}

type AlertService struct {
	config       Config
	httpClient   *http.Client
	lastSent     sync.Map // map[string]time.Time (Key: "agentID:alertType")
	debounceTime time.Duration
}

func NewService(cfg Config) *AlertService {
	if cfg.TelegramAPIBase == "" {
		cfg.TelegramAPIBase = "https://api.telegram.org"
	}
	return &AlertService{
		config: cfg,
		httpClient: &http.Client{
			Timeout: 10 * time.Second,
		},
		debounceTime: 60 * time.Minute,
	}
}

func (s *AlertService) SendEmail(subject, body string) error {
	if s.config.SMTPHost == "" || s.config.SMTPUser == "" {
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
		slog.Error("Failed to send email alert", "error", err)
		return err
	}
	slog.Info("Email alert sent successfully", "subject", subject)
	return nil
}

func (s *AlertService) SendTelegram(message string) error {
	if s.config.TelegramBotToken == "" || s.config.TelegramChatID == "" {
		return nil
	}

	url := fmt.Sprintf("%s/bot%s/sendMessage", s.config.TelegramAPIBase, s.config.TelegramBotToken)
	payload := map[string]string{
		"chat_id":    s.config.TelegramChatID,
		"text":       message,
		"parse_mode": "HTML",
	}

	body, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal telegram payload: %w", err)
	}

	resp, err := s.httpClient.Post(url, "application/json", bytes.NewBuffer(body))
	if err != nil {
		slog.Error("Failed to send Telegram alert", "error", err)
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		slog.Error("Telegram API returned non-200 status", "status", resp.StatusCode)
		return fmt.Errorf("telegram API error: status %d", resp.StatusCode)
	}

	slog.Info("Telegram alert sent successfully")
	return nil
}

func (s *AlertService) SendDiscord(message string) error {
	if s.config.DiscordWebhookURL == "" {
		return nil
	}

	payload := map[string]string{
		"content": message,
	}

	body, err := json.Marshal(payload)
	if err != nil {
		return fmt.Errorf("failed to marshal discord payload: %w", err)
	}

	resp, err := s.httpClient.Post(s.config.DiscordWebhookURL, "application/json", bytes.NewBuffer(body))
	if err != nil {
		slog.Error("Failed to send Discord alert", "error", err)
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		slog.Error("Discord webhook returned non-200 status", "status", resp.StatusCode)
		return fmt.Errorf("discord webhook error: status %d", resp.StatusCode)
	}

	slog.Info("Discord alert sent successfully")
	return nil
}

func (s *AlertService) CheckAndSend(agent storage.Agent, metric *storage.Metric) {
	// 1. Check Offline
	if agent.Status == "offline" {
		s.triggerAlert(agent, "OFFLINE", fmt.Sprintf("🚨 <b>CRITICAL ALERT:</b> Agent <code>%s</code> (%s) is <b>OFFLINE</b>.\nLast seen: %s", agent.Hostname, agent.ID, agent.UpdatedAt.Format(time.RFC3339)))
	}

	// 2. Check Disk
	if metric != nil && len(metric.DiskUsage) > 0 {
		for _, disk := range metric.DiskUsage {
			if disk.FreePercent < 5.0 {
				s.triggerAlert(agent, "DISK_FULL:"+disk.Path, fmt.Sprintf("⚠️ <b>DISK WARNING:</b> Disk <code>%s</code> on <code>%s</code> (%s) is at <b>%.2f%% free</b>.", disk.Path, agent.Hostname, agent.ID, disk.FreePercent))
			}
		}
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

	// Dispatch to all configured channels
	_ = s.SendEmail("TaraSysDash Alert: "+alertType, message)
	_ = s.SendTelegram(message)
	_ = s.SendDiscord(message)

	s.lastSent.Store(key, time.Now())
}
