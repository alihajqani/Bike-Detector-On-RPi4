
# 🚲 Bike Detector API on Raspberry Pi 4

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED.svg)
![YOLO](https://img.shields.io/badge/Model-Official_YOLO-FF9900.svg)
![Platform](https://img.shields.io/badge/Platform-Raspberry_Pi_4-C51A4A.svg)

A lightweight, robust, and containerized REST API designed to run on a **Raspberry Pi 4**. This project utilizes the latest official YOLO Nano model (`yolo26n.pt`) and OpenCV to detect bicycles in real-time through USB cameras.

It employs a multi-threaded camera manager to prevent frame buffering lags and uses FastAPI to serve the inference results efficiently.

---

## ✨ Features

- **Real-Time Detection:** Uses an optimized YOLO model to specifically track the "Bicycle" class (COCO class `1`).
- **Multi-Camera Support:** Configured via Docker Compose to handle multiple USB cameras simultaneously on different ports.
- **Hardware Optimized:** Frame-reading operates in an isolated daemon thread to guarantee the latest frame is processed without I/O blocking.
- **Fully Containerized:** Easily deployable using Docker & Docker Compose.
- **Systemd Integration:** Includes a `.service` file to automatically start the detection system upon Raspberry Pi boot.

---

## 📂 Project Structure

```text
.
├── Dockerfile                  # Multi-layer Dockerfile for Python 3.11 & OpenCV dependencies
├── README.md                   # Project documentation
├── config/
│   └── settings.py             # Pydantic BaseSettings for environment variables
├── docker-compose.yml          # Compose file for cam0 (port 8000) and cam1 (port 8001)
├── models/
│   └── yolo26n.pt              # Official YOLO Nano model file
├── requirements.txt            # Python dependencies
└── src/
    ├── __init__.py
    ├── camera.py               # Threaded OpenCV camera frame capture
    ├── detector.py             # YOLO Inference Singleton class
    └── main.py                 # FastAPI application
```

---

## ⚙️ Prerequisites

- **Raspberry Pi 4** (Recommended 4GB or 8GB RAM).
- **USB Webcams** connected to the RPi.
- Docker and Docker Compose installed on the RPi.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/alihajqani/Bike-Detector-On-RPi4.git
cd Bike-Detector-On-RPi4
```

### 2. Identify Camera Devices
Linux assigns devices like `/dev/video0`, `/dev/video2`, etc., to connected cameras. **You must find the correct path for your specific cameras before running the containers.**

Run the following command to list connected video devices:
```bash
ls -l /dev/video*
# OR
v4l2-ctl --list-devices
```

### 3. Update Configuration
Open `docker-compose.yml` and update the `devices` and `CAMERA_DEVICE` environments according to the outputs from the previous step.

> **Note:** If you are only using **one** camera, make sure to comment out or delete the `detector-cam1` service block in `docker-compose.yml` to prevent crash loops.

### 4. Build and Run via Docker Compose
Build the image and spin up the containers in detached mode:
```bash
docker compose up --build -d
```
To view the logs:
```bash
docker compose logs -f
```

---

## 🌐 API Usage

Once the containers are running, you can interact with the FastAPI endpoints.

### 1. Health Check
Verify the service is up and running.
```bash
curl http://<RASPBERRY_PI_IP>:8000/health
```
**Response:**
```json
{"status": "healthy", "threshold": 0.45}
```

### 2. Detect Bike
Triggers the camera to capture the latest frame and run inference.
```bash
curl http://<RASPBERRY_PI_IP>:8000/detect-bike
```
**Response (Bike Detected):**
```json
{
  "detected": true,
  "confidence": 0.875
}
```
**Response (No Bike Detected):**
```json
{
  "detected": false,
  "confidence": 0.0
}
```
*(If using the second camera, replace `8000` with `8001` in the URL).*

---

## 🔄 Autostart on Boot (Systemd)

To make sure the containers automatically start when the Raspberry Pi reboots, we have provided a systemd service file.

> ⚠️ **IMPORTANT:** Before installing the service, edit the `bike-detector.service` file and change the `WorkingDirectory` path to point to the exact location where you cloned this repository.
> 
> Example: `WorkingDirectory=/home/pi/Bike-Detector-On-RPi4`

**Setup Instructions:**
1. Copy the service file to the systemd directory:
   ```bash
   sudo cp bike-detector.service /etc/systemd/system/
   ```
2. Reload the systemd daemon:
   ```bash
   sudo systemctl daemon-reload
   ```
3. Enable the service to start on boot:
   ```bash
   sudo systemctl enable bike-detector.service
   ```
4. Start the service immediately:
   ```bash
   sudo systemctl start bike-detector.service
   ```
5. Check the status:
   ```bash
   sudo systemctl status bike-detector.service
   ```

---

## 🛠 Troubleshooting

- **No frame error (`"error": "no_frame"`):**
  This means OpenCV cannot open the camera. Double-check your `CAMERA_DEVICE` path (`/dev/videoX`) in `docker-compose.yml` and ensure the container has `privileged: true` (which is already set by default).
- **Docker Compose command not found:**
  Make sure you are using Docker Compose V2 (`docker compose`). If you have V1 installed, use `docker-compose up -d`.