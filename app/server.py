# Import asyncio to handle asynchronous WebSocket connections without blocking the main thread.
import asyncio
# Import json to parse incoming messages from the tablet which are sent as JSON strings.
import json
# Import threading to run the HTTP server in a separate thread so it doesn't block the WebSocket loop.
import threading
# Import http.server and socketserver to quickly create a local web server to serve the index.html file.
import http.server
import socketserver
# Import ctypes to interact with Windows API for DPI awareness and screen resolution.
import ctypes
# Import os and sys to interact with the file system and exit the program if dependencies are missing.
import os
import sys
# Import socket to get the local IP address of the computer to show to the user.
import socket

# Try importing the required third-party packages. If they are missing, exit gracefully with an instruction.
try:
    import websockets
    import pynput
except ImportError:
    print("Missing packages. Please run: pip install websockets pynput")
    sys.exit(1)

# Ensure the terminal prints UTF-8 characters correctly, which is useful if there are any non-English characters.
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize the pynput mouse controller. This object is used to simulate physical mouse movements and clicks.
mouse = pynput.mouse.Controller()
Button = pynput.mouse.Button

# Get the actual screen resolution. We need this to map the tablet's 0.0-1.0 coordinates to real screen pixels.
if os.name == 'nt':
    try:
        # Tell Windows that this script is DPI aware. This prevents Windows from falsely reporting 
        # a smaller screen resolution when Display Scaling (e.g., 150%) is enabled in Windows settings.
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
else:
    # Fallback for non-Windows systems, though this script is primarily designed for Windows.
    screen_width = 1920
    screen_height = 1080

async def handle_tablet(websocket, *args, **kwargs):
    """
    This function handles the WebSocket connection for a single tablet client.
    It receives drawing coordinates and scroll events, translating them into physical mouse actions.
    """
    print("[+] Tablet connected via WebSocket!")
    try:
        # As soon as the tablet connects, send the PC's screen dimensions to it.
        # The tablet uses this to calculate the exact aspect ratio so circles don't stretch into ovals.
        await websocket.send(json.dumps({
            'type': 'init',
            'width': screen_width,
            'height': screen_height
        }))
        
        # Continuously listen for incoming messages from the tablet.
        async for message in websocket:
            data = json.loads(message)
            
            # If the tablet sends a scroll event (from two-finger pinch gesture).
            if data['type'] == 'scroll':
                # dy = 1 is scroll up (zoom in), dy = -1 is scroll down (zoom out).
                # We apply this directly to the mouse wheel.
                mouse.scroll(0, data['dy'])
                continue
            
            # The tablet sends normalized coordinates (0.0 to 1.0). 
            # We multiply by the screen resolution to get the exact pixel location on the PC monitor.
            mapped_x = int(data['x'] * screen_width)
            mapped_y = int(data['y'] * screen_height)

            # When the pen touches the tablet screen.
            if data['type'] == 'down':
                mouse.position = (mapped_x, mapped_y)
                mouse.press(Button.left)
            # When the pen moves across the tablet screen (either hovering or dragging).
            elif data['type'] == 'move':
                mouse.position = (mapped_x, mapped_y)
            # When the pen is lifted from the tablet screen.
            elif data['type'] == 'up':
                mouse.position = (mapped_x, mapped_y)
                mouse.release(Button.left)
                
    except websockets.exceptions.ConnectionClosed:
        # Triggered when the user closes the browser or the tablet disconnects.
        print("[-] Tablet disconnected.")

async def main():
    """
    Starts the WebSocket server on port 8765. This server listens for incoming connections 
    from the tablet browser to receive real-time mouse data.
    """
    async with websockets.serve(handle_tablet, "0.0.0.0", 8765):
        await asyncio.Future()

def start_http_server():
    """
    Starts a simple HTTP server on port 8080. This allows the tablet to load the index.html 
    interface without needing any complicated web server software like Apache or Nginx.
    """
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Change the working directory to the folder containing this script or the PyInstaller extracted folder.
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_path)
    socketserver.TCPServer.allow_reuse_address = True
    
    # Attempt to get all IP addresses assigned to this PC so we can print them out for the user to type.
    hostname = socket.gethostname()
    try:
        _, _, ips = socket.gethostbyname_ex(hostname)
    except Exception:
        ips = ['127.0.0.1']
        
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print("\n" + "="*60)
        print("[*] Server is running!")
        print("[*] For USB Connection (Low Latency):")
        print("   1. Connect Tablet to PC via USB cable")
        print("   2. On Tablet, go to Settings > Connections > Mobile Hotspot and Tethering")
        print("   3. Enable 'USB Tethering'")
        print("   4. Open any Browser (e.g., Zen, Chrome) OR use your App Shortcut on the Tablet")
        print("      and go to one of these URLs:")
        for ip in ips:
            if not ip.startswith("127."):
                print(f"      -> http://{ip}:{PORT}")
        print("\n[*] For Wi-Fi Connection:")
        print("   Open your Browser or App Shortcut on the Tablet and go to the URL above (using your Wi-Fi IP)")
        print("="*60 + "\n")
        httpd.serve_forever()

if __name__ == "__main__":
    print(f"[*] Screen resolution detected: {screen_width}x{screen_height}")
    
    # We run the HTTP server in a daemon thread so it runs in the background.
    # This allows the main thread to focus entirely on the WebSocket asyncio event loop.
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    try:
        # Start the WebSocket server loop.
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user.")
