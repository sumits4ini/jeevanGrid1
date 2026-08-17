"""
Integration Tests for Operations WebSocket Stream
"""

from fastapi.testclient import TestClient


def test_websocket_operations_connection_and_heartbeat(client: TestClient):
    """Verifies connecting to /api/v1/ws/operations and exchanging ping/pong."""
    with client.websocket_connect("/api/v1/ws/operations") as websocket:
        # Receive welcome / connection established message
        data = websocket.receive_json()
        assert data["type"] == "CONNECTION_ESTABLISHED"
        assert data["status"] == "CONNECTED"

        # Send ping heartbeat
        websocket.send_text("PING")
        pong_response = websocket.receive_json()
        assert pong_response["type"] == "PONG"
        assert pong_response["status"] == "ALIVE"
