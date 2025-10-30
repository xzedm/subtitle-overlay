# Create test_connection.py
import asyncio
import websockets
import json

async def test():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        # Send test subtitle
        await websocket.send(json.dumps({
            "type": "subtitle",
            "text": "This is a test subtitle!"
        }))
        print("Test subtitle sent!")
        await asyncio.sleep(1)

asyncio.run(test())