"""
Thread-safe Async WebSocket Connection Manager for Dashboard Telemetry
"""

import asyncio
from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect

from backend.app.core.logging import logger


class ConnectionManager:
    """
    Manages active dashboard WebSocket connections, broadcasting
    operational events, alerts, and periodic heartbeats.
    """

    def __init__(self):
        self._active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def client_count(self) -> int:
        return len(self._active_connections)

    async def connect(self, websocket: WebSocket) -> None:
        """Accepts and registers a new WebSocket client."""
        await websocket.accept()
        async with self._lock:
            self._active_connections.add(websocket)
        logger.info(f"WebSocket client connected. Total active clients: {self.client_count}")

        # Send initial welcome / state synchronization event
        welcome_payload = {
            "type": "CONNECTION_ESTABLISHED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "CONNECTED",
            "client_count": self.client_count,
            "message": "Connected to JeevanGrid Real-Time Operations Telemetry Stream.",
        }
        await websocket.send_text(json.dumps(welcome_payload))

    async def disconnect(self, websocket: WebSocket) -> None:
        """Unregisters a disconnected WebSocket client."""
        async with self._lock:
            self._active_connections.discard(websocket)
        logger.info(f"WebSocket client disconnected. Total active clients: {self.client_count}")

    async def broadcast(self, message: Dict[str, Any]) -> None:
        """Broadcasts a JSON-serializable message to all active clients."""
        if not self._active_connections:
            return

        payload_str = json.dumps(message)
        dead_connections: List[WebSocket] = []

        for connection in list(self._active_connections):
            try:
                await connection.send_text(payload_str)
            except Exception as exc:
                logger.debug(f"Failed to send to client ({exc}). Marking for cleanup.")
                dead_connections.append(connection)

        if dead_connections:
            async with self._lock:
                for dead_conn in dead_connections:
                    self._active_connections.discard(dead_conn)

    async def broadcast_event(self, event_data: Dict[str, Any]) -> None:
        """Convenience wrapper for broadcasting operational events."""
        message = {
            "type": "OPERATIONAL_EVENT",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": event_data,
        }
        await self.broadcast(message)

    async def broadcast_alert(self, alert_data: Dict[str, Any]) -> None:
        """Convenience wrapper for broadcasting tactical alerts."""
        message = {
            "type": "TACTICAL_ALERT",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": alert_data,
        }
        await self.broadcast(message)

    async def broadcast_notification(self, notif_data: Dict[str, Any]) -> None:
        """Convenience wrapper for broadcasting in-app notifications."""
        message = {
            "type": "NOTIFICATION",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": notif_data,
        }
        await self.broadcast(message)


# Global singleton instance
connection_manager = ConnectionManager()
