package alert

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"sync/atomic"
	"testing"
	"time"

	"github.com/tarakreasi/taraSysDash/internal/storage"
)

func TestSendTelegram_Success(t *testing.T) {
	var requestCount int32
	var receivedBody map[string]string

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt32(&requestCount, 1)
		body, _ := io.ReadAll(r.Body)
		_ = json.Unmarshal(body, &receivedBody)

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write([]byte(`{"ok":true}`))
	}))
	defer ts.Close()

	cfg := Config{
		TelegramBotToken: "test-bot-token",
		TelegramChatID:   "12345678",
		TelegramAPIBase:  ts.URL,
	}

	svc := NewService(cfg)
	err := svc.SendTelegram("Test alert message")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	if atomic.LoadInt32(&requestCount) != 1 {
		t.Errorf("expected 1 request, got %d", requestCount)
	}

	if receivedBody["chat_id"] != "12345678" || receivedBody["text"] != "Test alert message" {
		t.Errorf("unexpected payload: %+v", receivedBody)
	}
}

func TestSendDiscord_Success(t *testing.T) {
	var requestCount int32
	var receivedBody map[string]string

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt32(&requestCount, 1)
		body, _ := io.ReadAll(r.Body)
		_ = json.Unmarshal(body, &receivedBody)

		w.WriteHeader(http.StatusNoContent)
	}))
	defer ts.Close()

	cfg := Config{
		DiscordWebhookURL: ts.URL,
	}

	svc := NewService(cfg)
	err := svc.SendDiscord("🚨 Server Down Alert")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	if atomic.LoadInt32(&requestCount) != 1 {
		t.Errorf("expected 1 request, got %d", requestCount)
	}

	if receivedBody["content"] != "🚨 Server Down Alert" {
		t.Errorf("unexpected discord payload: %+v", receivedBody)
	}
}

func TestCheckAndSend_Offline(t *testing.T) {
	cfg := Config{
		SMTPHost: "",
	}
	svc := NewService(cfg)
	svc.debounceTime = 100 * time.Millisecond

	agent := storage.Agent{
		ID:        "agent-1",
		Hostname:  "test-host",
		Status:    "offline",
		UpdatedAt: time.Now().Add(-2 * time.Minute),
	}

	// 1. Should Trigger
	svc.CheckAndSend(agent, nil)

	key := "agent-1:OFFLINE"
	if _, ok := svc.lastSent.Load(key); !ok {
		t.Error("Expected Offline alert to be recorded (debounced)")
	}

	// 2. Immediate second call should strictly be debounced
	firstTime, _ := svc.lastSent.Load(key)
	svc.CheckAndSend(agent, nil)
	secondTime, _ := svc.lastSent.Load(key)

	if firstTime != secondTime {
		t.Error("Expected second alert to be debounced without updating timestamp")
	}
}

func TestCheckAndSend_DiskCritical(t *testing.T) {
	cfg := Config{SMTPHost: ""}
	svc := NewService(cfg)

	agent := storage.Agent{ID: "agent-2", Hostname: "disk-host", Status: "online"}
	metric := &storage.Metric{
		DiskUsage: []storage.DiskStat{
			{Path: "C:", FreePercent: 20.0}, // OK
			{Path: "D:", FreePercent: 1.0},  // CRITICAL (< 5%)
		},
	}

	svc.CheckAndSend(agent, metric)

	key := "agent-2:DISK_FULL:D:"
	if _, ok := svc.lastSent.Load(key); !ok {
		t.Error("Expected Disk Full alert to be recorded for D:")
	}

	// C: should not trigger alert
	okKey := "agent-2:DISK_FULL:C:"
	if _, ok := svc.lastSent.Load(okKey); ok {
		t.Error("Did not expect alert for non-critical disk C:")
	}
}
