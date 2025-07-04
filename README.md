﻿# 🚗 Ocean City Parking Lot Occupancy Tracker

A real-time parking lot occupancy tracking system that uses YOLO computer vision to monitor parking spots and provides a web-based dashboard for viewing current availability.

![Parking Tracker](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green)
![YOLO](https://img.shields.io/badge/YOLO-v11-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0-red)

## 🌟 Features

- **Real-time Computer Vision**: Uses YOLOv11 model to detect and track parked vehicles
- **Live Web Dashboard**: Beautiful, responsive web interface with live updates
- **REST API**: RESTful endpoints for parking status updates and retrieval
- **Visual Indicators**: Color-coded occupancy bar (green/yellow/red based on capacity)
- **Live Camera Feed**: Displays live snapshots from the parking lot camera
- **Automatic Updates**: Real-time status updates every second

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   parkinglot.py │────│     app.py      │────│   index.html    │
│  (CV Processing)│    │  (Flask API)    │    │ (Web Dashboard) │
│                 │    │                 │    │                 │
│ • YOLO Detection│    │ • REST API      │    │ • Live Updates  │
│ • Spot Tracking│    │ • Data Storage  │    │ • Progress Bar  │
│ • API Updates  │    │ • CORS Support  │    │ • Live Feed     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
parking/
├── app.py                      # Flask web server and API
├── parkinglot.py              # Computer vision processing
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── models/
│   └── yolo11n.pt            # YOLOv11 model weights
├── resources/
│   ├── background.jpg         # Dashboard background image
│   ├── bounding_boxes.json    # Parking spot annotations
│   └── screenshot_to_plot.png # Reference image
├── static/
│   └── resources/
│       └── background.jpg     # Static assets
├── templates/
│   └── index.html            # Web dashboard template
└── screenshots/
    └── tracked_spots_59.png   # Sample output
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- Virtual environment (recommended)
- Internet connection for live camera feed

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ptrpetro/ParkingLot_Occupancy.git
   cd parking
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask web server**
   ```bash
   python app.py
   ```
   The web dashboard will be available at `http://127.0.0.1:5000`

2. **Start the computer vision processor** (in a new terminal)
   ```bash
   python parkinglot.py
   ```

3. **View the dashboard**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 🖥️ Web Dashboard

The web interface provides:

- **Live Camera Feed**: Real-time snapshots from the Ocean City inlet parking lot
- **Occupancy Statistics**: Current occupied and available spots
- **Visual Progress Bar**: Color-coded occupancy indicator
  - 🟢 Green: < 50% occupied
  - 🟡 Yellow: 50-80% occupied
  - 🔴 Red: > 80% occupied
- **Last Updated**: Timestamp of the most recent data update

## 🔧 API Endpoints

### GET `/api/status`
Returns the current parking status.

**Response:**
```json
{
  "occupied": 23,
  "available": 36,
  "last_updated": "2025-07-02 14:30:15"
}
```

### POST `/api/update-parking`
Updates the parking status (used by the CV processor).

**Request Body:**
```json
{
  "occupied": 23,
  "available": 36
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "occupied": 23,
    "available": 36,
    "last_updated": "2025-07-02 14:30:15"
  }
}
```

## 🤖 Computer Vision Details

### YOLO Model
- **Model**: YOLOv11 Nano (`yolo11n.pt`)
- **Tracker**: BotSORT for improved accuracy
- **Detection**: Vehicle detection and tracking in parking spots

### Parking Spot Configuration
Parking spots are defined in `resources/bounding_boxes.json` with bounding box coordinates for each monitored parking space.

### Video Source
Currently configured to monitor the Ocean City inlet parking lot via live stream:
```python
stream_url = "https://t1.ipcamlive.com/timelapses/5aec8d9905b9a/2025-04-06/video.mp4"
```

## 📦 Dependencies

### Core Libraries
- **Flask 3.1.0**: Web framework and API
- **Flask-CORS 5.0.0**: Cross-origin resource sharing
- **OpenCV 4.11.0**: Computer vision processing
- **Ultralytics 8.3.103**: YOLO model implementation
- **Requests 2.32.3**: HTTP client for API communication

### ML/AI Libraries
- **PyTorch 2.6.0**: Deep learning framework
- **NumPy 2.1.1**: Numerical computing
- **Pandas 2.2.3**: Data manipulation

### Visualization
- **Matplotlib 3.10.1**: Plotting and visualization
- **Seaborn 0.13.2**: Statistical visualization

## 🎯 Usage Examples

### Running with Custom Video Source
Modify the `stream_url` in `parkinglot.py`:
```python
stream_url = "your_camera_stream_url_here"
```

### Testing the API
```bash
# Get current status
curl http://127.0.0.1:5000/api/status

# Update parking data
curl -X POST http://127.0.0.1:5000/api/update-parking \
  -H "Content-Type: application/json" \
  -d '{"occupied": 25, "available": 34}'
```

## 🔧 Configuration

### Parking Spot Count
Update the total number of parking spots in `parkinglot.py`:
```python
parkingSpots = 59  # Total number of parking spots
```

### Tracking Settings
Modify tracking parameters in the `ParkingManagement` initialization:
```python
parkingmanager = solutions.ParkingManagement(
    model="models/yolo11n.pt",
    json_file="resources/bounding_boxes.json",
    tracker="botsort.yaml"  # or "bytetrack.yaml" for faster processing
)
```

## 🐛 Troubleshooting

### Common Issues

1. **"Flask missing" error**
   ```bash
   pip install flask flask-cors
   ```

2. **Camera stream not accessible**
   - Check internet connection
   - Verify the stream URL is accessible
   - Try using a local video file for testing

3. **YOLO model not found**
   - Ensure `models/yolo11n.pt` exists
   - Download from Ultralytics if missing

4. **Permission errors**
   - Ensure virtual environment is activated
   - Check file permissions in the project directory

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://ultralytics.com/) for the YOLO implementation
- [Ocean City Live](https://oceancitylive.com/) for the parking lot camera feed
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Tailwind CSS](https://tailwindcss.com/) for the responsive UI

