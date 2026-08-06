import asyncio
import json
import threading
import http.server
import socketserver
import ctypes
import os
import sys
import socket

try:
    import websockets
    import pynput
except ImportError:
    print("Missing packages. Please run: pip install websockets pynput")
    sys.exit(1)

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

mouse = pynput.mouse.Controller()
Button = pynput.mouse.Button

if os.name == 'nt':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
else:
    screen_width = 1920
    screen_height = 1080

async def handle_tablet(websocket, *args, **kwargs):
    print("[+] Tablet connected via WebSocket!")
    try:
        # Send screen dimensions to the tablet to maintain aspect ratio
        await websocket.send(json.dumps({
            'type': 'init',
            'width': screen_width,
            'height': screen_height
        }))
        
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'scroll':
                # dy = 1 is scroll up (zoom in), dy = -1 is scroll down (zoom out)
                mouse.scroll(0, data['dy'])
                continue
            
            mapped_x = int(data['x'] * screen_width)
            mapped_y = int(data['y'] * screen_height)

            if data['type'] == 'down':
                mouse.position = (mapped_x, mapped_y)
                mouse.press(Button.left)
            elif data['type'] == 'move':
                mouse.position = (mapped_x, mapped_y)
            elif data['type'] == 'up':
                mouse.position = (mapped_x, mapped_y)
                mouse.release(Button.left)
                
    except websockets.exceptions.ConnectionClosed:
        print("[-] Tablet disconnected.")

async def main():
    async with websockets.serve(handle_tablet, "0.0.0.0", 8765):
        await asyncio.Future()

def start_http_server():
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    
    # Get all IP addresses
    hostname = socket.gethostname()
    try:
        _, _, ips = socket.gethostbyname_ex(hostname)
    except Exception:
        ips = ['127.0.0.1']
        
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print("\n" + "="*60)
        print(f"[*] Server is running!")
        print(f"[*] For USB Connection (Low Latency):")
        print(f"   1. Connect Tablet to PC via USB cable")
        print(f"   2. On Tablet, go to Settings > Connections > Mobile Hotspot and Tethering")
        print(f"   3. Enable 'USB Tethering'")
        print(f"   4. Open any Browser (e.g., Zen, Chrome) OR use your App Shortcut on the Tablet")
        print(f"      and go to one of these URLs:")
        for ip in ips:
            if not ip.startswith("127."):
                print(f"      -> http://{ip}:{PORT}")
        print("\n[*] For Wi-Fi Connection:")
        print(f"   Open your Browser or App Shortcut on the Tablet and go to the URL above (using your Wi-Fi IP)")
        print("="*60 + "\n")
        httpd.serve_forever()

if __name__ == "__main__":
    print(f"[*] Screen resolution detected: {screen_width}x{screen_height}")
    
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user.")
