# Minimal Tablet Mouse

Turn your Android tablet (or iPad) into a low-latency, absolute-positioning drawing tablet for your PC over Wi-Fi or USB tethering. 
Optimized for pixel art in Aseprite with Palm Rejection, Pinch-to-Zoom, and Active Area mapping.

## Features
- **Ultra-Low Latency:** Works seamlessly over USB tethering or local Wi-Fi.
- **Absolute Positioning:** Maps the tablet screen exactly to your PC monitor.
- **Palm Rejection:** Differentiates between S-Pen/Apple Pencil (drawing) and Fingers (zooming).
- **Active Area Mapping:** Adjust the drawing area size (Sensitivity) to reduce arm movement.
- **Pinch-to-Zoom:** Use two fingers on the tablet to zoom in/out on Aseprite.
- **Jitter Smoothing:** Built-in intelligent smoothing (EMA filter) to stabilize your strokes when the active area is small.

## Download & Installation

### Option 1: Direct Download (Ready to use)
The easiest way to use Tablet Mouse. No Python installation required!
1. [📥 Download TabletMouse.exe](https://github.com/Oak04K/TABLET-MOUSE/raw/main/TabletMouse.exe)
2. Double-click the downloaded `TabletMouse.exe` to start the server.

### Option 2: Run from Source Code (For developers)
If you want to view or modify the code:
1. Ensure **Python 3** is installed on your PC.
2. Open Command Prompt (`cmd`) and run:
   ```cmd
   python -m pip install websockets pynput
   ```
3. Open the `app` folder and double-click `Start_Tablet_Mouse.bat`.

## Usage
1. Run the application (either `TabletMouse.exe` or `Start_Tablet_Mouse.bat`).
2. A command prompt window will appear displaying your local IP URL (e.g., `http://192.168.x.x:8080`).
3. Connect your tablet to the same Wi-Fi network (or use USB Tethering for a zero-latency experience).
4. Open a web browser (Chrome, Safari, etc.) on your tablet and navigate to the displayed URL.
5. Draw!
