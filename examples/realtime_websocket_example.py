#!/usr/bin/env python3
"""
Real-time analysis with WebSocket streaming
"""

import asyncio
from deriv_analyzer import RealtimeDerivAnalyzer
from deriv_analyzer.websocket_handler import WebSocketServer, WebSocketClient
from deriv_analyzer.visualization import AnalysisReporter
import json


ws_server = None
analyzer = None


async def prediction_callback(symbol: str, prediction: dict):
    """Callback to broadcast predictions via WebSocket"""
    print(f"Broadcasting prediction for {symbol}")
    if ws_server:
        await ws_server.broadcast_prediction(symbol, prediction)


async def client_message_handler(message: dict):
    """Handle incoming client messages"""
    msg_type = message.get('type')
    print(f"Client message: {msg_type}")
    
    if msg_type == 'get_prediction':
        symbol = message.get('symbol')
        prediction = analyzer.get_latest_prediction(symbol)
        if prediction:
            print(f"Latest prediction for {symbol}:")
            print(json.dumps(prediction, indent=2, default=str))


async def run_server():
    """Run WebSocket server"""
    global ws_server, analyzer
    
    # Initialize analyzer
    analyzer = RealtimeDerivAnalyzer()
    analyzer.register_callback(prediction_callback)
    
    # Setup WebSocket server
    ws_server = WebSocketServer('localhost', 8765)
    await ws_server.start()
    
    print("WebSocket server running on ws://localhost:8765")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Keep server running
        await asyncio.sleep(float('inf'))
    except KeyboardInterrupt:
        print("\nShutting down server...")
        await ws_server.stop()
        await analyzer.disconnect_all()


async def run_client():
    """Run WebSocket client"""
    client = WebSocketClient('ws://localhost:8765')
    
    # Register callback
    client.register_callback(client_message_handler)
    
    try:
        await client.connect()
        
        # Request prediction
        await client.send_message({
            'type': 'get_prediction',
            'symbol': 'BTC/USD'
        })
        
        # Listen for messages
        await client.listen()
    
    except KeyboardInterrupt:
        print("\nDisconnecting client...")
        await client.disconnect()
    except Exception as e:
        print(f"Client error: {e}")
        await client.disconnect()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'client':
        print("Starting WebSocket client...")
        asyncio.run(run_client())
    else:
        print("Starting WebSocket server...")
        asyncio.run(run_server())
