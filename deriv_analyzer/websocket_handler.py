import asyncio
import json
import logging
from typing import Dict, Callable, Optional, List
from datetime import datetime
import websockets
from websockets.server import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketServer:
    """WebSocket server for real-time updates"""
    
    def __init__(self, host: str = 'localhost', port: int = 8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.server = None
    
    async def register(self, websocket: WebSocketServerProtocol):
        """Register a new client"""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
    
    async def unregister(self, websocket: WebSocketServerProtocol):
        """Unregister a client"""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast_prediction(self, symbol: str, prediction: Dict):
        """Broadcast prediction to all connected clients"""
        if not self.clients:
            return
        
        message = {
            'type': 'prediction_update',
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'data': prediction
        }
        
        # Send to all clients
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle client connections"""
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                logger.info(f"Received message from client: {data}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start WebSocket server"""
        self.server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
    
    async def stop(self):
        """Stop WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("WebSocket server stopped")


class WebSocketClient:
    """WebSocket client for receiving real-time updates"""
    
    def __init__(self, uri: str = 'ws://localhost:8765'):
        self.uri = uri
        self.websocket = None
        self.callbacks = []
    
    def register_callback(self, callback: Callable):
        """Register callback for messages"""
        self.callbacks.append(callback)
    
    async def connect(self):
        """Connect to WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.uri)
            logger.info(f"Connected to {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from server"""
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected from WebSocket server")
    
    async def listen(self):
        """Listen for messages"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                for callback in self.callbacks:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(data)
                        else:
                            callback(data)
                    except Exception as e:
                        logger.error(f"Callback error: {e}")
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Listen error: {e}")
    
    async def send_message(self, message: Dict):
        """Send message to server"""
        if self.websocket:
            await self.websocket.send(json.dumps(message))
