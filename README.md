# Raspberry Pi Acquisition API

## Overview
This repo contains the control server running on the Raspberry Pi. It exposes a network-accessible API for triggering, monitoring, and retrieving the measurements.

## Architecture

- **C backend** : Handles acquisition logic (SPI, GPIO, file writing) compiled into a shared library (`libacquisition.so`,  generated in by pi-controller repo).
- **Python API server**: A FastAPI app loads and controls the C backend using `ctypes`.
- **Uvicorn server**: FastAPI is served via `uvicorn` as a systemd service that can start automatically at boot.
- **Frontend**: Any external machine can interact with the server using `curl` with CLI, `requests` for python, or browser clients via the Pi’s static IP address.

## Key Features

### Acquisition
- Start/stop acquisition via HTTP
- Stream downsampled live data
- Download or delete `.bin` result files
- Configure duration and filename remotely

### Voltage bias

## Example Usage

```bash
# Set acquisition duration to 5 seconds
curl -X POST "http://192.168.0.2:8000/acquisition/set-duration?duration=5000"

# Start acquisition
curl http://192.168.0.2:8000/acquisition/start

# Stream simplified data
curl http://192.168.0.2:8000/acquisition/stream?filename=my_run.bin\&max_points=200

# Download full file
curl -O http://192.168.0.2:8000/acquisition/download?filename=my_run.bin
```

## Deployment

The server listens on `0.0.0.0:8000` for remote commands
