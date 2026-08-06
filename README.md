# Tablet Mouse for Aseprite 🎨

Turn your Android tablet (or iPad) into a low-latency, absolute-positioning drawing tablet for your PC over Wi-Fi or USB tethering! 
Optimized for pixel art in Aseprite with Palm Rejection, Pinch-to-Zoom, and Active Area mapping.

## Features
- **Ultra-Low Latency:** Works seamlessly over USB tethering or local Wi-Fi.
- **Absolute Positioning:** Maps the tablet screen exactly to your PC monitor.
- **Palm Rejection:** Differentiates between S-Pen/Apple Pencil (drawing) and Fingers (zooming).
- **Active Area Mapping:** Adjust the drawing area size (Sensitivity) to reduce arm movement.
- **Pinch-to-Zoom:** Use two fingers on the tablet to zoom in/out on Aseprite.
- **Jitter Smoothing:** Built-in intelligent smoothing (EMA filter) to stabilize your strokes when the active area is small.

## Requirements (PC)
- **Python 3** (Download from python.org or Microsoft Store)
- Required Python packages: `websockets`, `pynput`

## Installation
1. Open Command Prompt (`cmd`) on your Windows PC.
2. Run the following command to install dependencies:
   ```cmd
   python -m pip install websockets pynput
   ```

## Usage
1. Open the `app` folder and double-click `Start_Tablet_Mouse.bat`.
2. A command prompt window will appear displaying your local IP URL (e.g., `http://192.168.x.x:8000`).
3. Connect your tablet to the same Wi-Fi network (or use USB Tethering for a zero-latency experience).
4. Open a web browser (Chrome, Safari, etc.) on your tablet and navigate to the displayed URL.
5. Draw!

*(Tip: You can right-click `Start_Tablet_Mouse.bat` and select `Send to -> Desktop (create shortcut)` for quick access from your Desktop!)*
