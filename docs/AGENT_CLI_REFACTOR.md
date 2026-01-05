# Agent CLI Refactor Documentation

The `tara-agent` has been refactored to support shorter and more intuitive command-line flags. This update allows for easier manual configuration and automation.

## New Command-Line Flags

| Flag | Long Format | Description | Example |
|------|-------------|-------------|---------|
| `-n` | `--name` | The identity/hostname of the agent. Defaults to system hostname. | `-n "Rec"` |
| `-r` | `--rack` | The physical location/rack of the agent. | `-r "Rack A"` |
| `-s` | `--server` | The full HTTP URL of the remote server. | `-s "http://10.200.150.85:8080"` |

## Usage Examples

### Running via Binary
```bash
./bin/tara-agent -s http://10.200.150.85:8080 -n "Rec" -r "Production Rack A"
```

### Building the Agent
The `Makefile` has been updated to support local Go installations. To build for Linux:
```bash
make build-agent-linux
```

## Wrapper Script
A convenient wrapper script `run-agent-remote.sh` is provided in the repository root to simplify execution with pre-configured settings.
