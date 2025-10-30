import asyncio
import json
from typing import Callable, Optional
import websockets
from websockets.server import serve

class SubtitleServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8765):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        self.on_subtitle_callback: Optional[Callable] = None
        self.running = False
    
    def set_subtitle_callback(self, callback: Callable):
        """Set callback function to handle received subtitles"""
        self.on_subtitle_callback = callback
    
    async def handler(self, websocket):
        """Handle WebSocket connections"""
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('type') == 'subtitle' and self.on_subtitle_callback:
                        subtitle_text = data.get('text', '')
                        # Call the callback in a thread-safe way
                        if subtitle_text:
                            self.on_subtitle_callback(subtitle_text)
                except json.JSONDecodeError:
                    print(f"Invalid JSON received: {message}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def start(self):
        """Start the WebSocket server"""
        self.running = True
        try:
            self.server = await serve(self.handler, self.host, self.port)
            print(f"WebSocket server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever
        except OSError as e:
            if e.errno == 10048:  # Windows: Address already in use
                print(f"\n⚠ ERROR: Port {self.port} is already in use!")
                print("Another instance of this application may be running.")
                print("Please close it or use a different port in the config.\n")
                raise
            else:
                raise
    
    def get_client_count(self) -> int:
        """Return number of connected clients"""
        return len(self.clients)
    
    async def stop(self):
        """Stop the WebSocket server"""
        self.running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()