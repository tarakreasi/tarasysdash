# ─── Stage 1: Build Frontend ─────────────────────────────────────────────────
FROM node:22-alpine AS frontend
WORKDIR /app/web
COPY web/package*.json ./
RUN npm ci
COPY web/ ./
RUN npm run build

# ─── Stage 2: Build Go Server ────────────────────────────────────────────────
FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
COPY --from=frontend /app/web/dist ./cmd/server/web_dist
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-s -w" \
    -o /bin/tara-server ./cmd/server

# ─── Stage 3: Final Minimal Image ────────────────────────────────────────────
FROM alpine:3.21
RUN apk --no-cache add ca-certificates tzdata
WORKDIR /app

COPY --from=builder /bin/tara-server .

# Data volume for SQLite database
VOLUME ["/app/data"]

EXPOSE 8080

ENV PORT=8080

ENTRYPOINT ["./tara-server"]
