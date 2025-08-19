# Raspberry Pi XTream API

## Overview
This repo contains the control server running on the Raspberry Pi. It exposes a network-accessible API for triggering, monitoring, and retrieving the measurements.

## Architecture

- **C backend** : Handles acquisition logic (SPI, GPIO, file writing) compiled into a shared library (`xtreamlib.so`,  generated in by pi-controller repo).
- **Python API server**: A FastAPI app loads and controls the C backend using `ctypes`.
- **Uvicorn server**: FastAPI is served via `uvicorn` as a systemd service that can start automatically at boot.
- **Frontend**: Any external machine can interact with the server using `curl` with CLI, `requests` for python, or browser clients via the Pi’s static IP address.

### File structure

Below is an example of this project implemented into `/home/pi/xtream` on the Raspberry Pi.

```text
/home/pi/xtream
├── python-src/           # This repo source code
│   ├── test/             # HTTP test scripts
│   ├── app.py            # Main entry point
│   └── ...               # Application .py files
├── xtreamlib.so          # The C library
├── requirements.txt      # Python dependencies
└── venv/                 # Python venv
```

## Key Features

### Acquisition
- Start/stop acquisition via HTTP
- Stream downsampled live data
- Download or delete `.bin` result files
- Configure duration and filename remotely

### Voltage bias

- Set the bias polarity and value
- Set the bias voltage on/off
- Get the bias status
  
## Example Usage of the API

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

### Python environment

Setup the python environment using : 

```
python -m venv venv
source venv/bin/activate
pip install -r requirements
```

### Running manually

Run using :

```python3 python-src/app.py```

The server will then listens on `0.0.0.0:8000`.

### Daemon

The `xtream.service` file can be installed to run the application automatically at boot.

1. Copy the service file into the systemd directory:
   ```sudo cp xtream.service /etc/systemd/system/xtream.service```

2. Reload systemd to pick up the new unit:
   ```sudo systemctl daemon-reload```

3. Enable the service to start on boot:
   ```sudo systemctl enable xtream.service```

4. Start the service now (without rebooting):
   ```sudo systemctl start xtream.service```

