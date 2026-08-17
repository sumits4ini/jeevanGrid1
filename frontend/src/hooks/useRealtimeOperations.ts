"use client";

import { useEffect, useRef, useState } from "react";
import { Alert, OperationalEvent, WebSocketMessage } from "@/types/realtime";

export type ConnectionStatus = "CONNECTED" | "RECONNECTING" | "DISCONNECTED";

export function useRealtimeOperations() {
  const [status, setStatus] = useState<ConnectionStatus>("DISCONNECTED");
  const [latestEvent, setLatestEvent] = useState<OperationalEvent | null>(null);
  const [latestAlert, setLatestAlert] = useState<Alert | null>(null);
  const [connectedClients, setConnectedClients] = useState<number>(1);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttemptsRef = useRef<number>(0);

  useEffect(() => {
    let isMounted = true;

    const getWsUrl = () => {
      if (process.env.NEXT_PUBLIC_WS_BASE_URL) {
        return process.env.NEXT_PUBLIC_WS_BASE_URL;
      }
      if (typeof window !== "undefined") {
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const host = window.location.hostname;
        return `${protocol}//${host}:8000/api/v1/ws/operations`;
      }
      return "ws://localhost:8000/api/v1/ws/operations";
    };

    const connect = () => {
      if (!isMounted) return;
      try {
        const url = getWsUrl();
        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => {
          if (!isMounted) return;
          setStatus("CONNECTED");
          reconnectAttemptsRef.current = 0;
        };

        ws.onmessage = (event) => {
          if (!isMounted) return;
          try {
            const parsed: WebSocketMessage = JSON.parse(event.data);
            if (parsed.type === "CONNECTION_ESTABLISHED") {
              setStatus("CONNECTED");
            } else if (parsed.type === "OPERATIONAL_EVENT" && parsed.data) {
              setLatestEvent(parsed.data as unknown as OperationalEvent);
            } else if (parsed.type === "TACTICAL_ALERT" && parsed.data) {
              setLatestAlert(parsed.data as unknown as Alert);
            }
          } catch {
            // Ignore non-JSON heartbeat pings
          }
        };

        ws.onclose = () => {
          if (!isMounted) return;
          setStatus("RECONNECTING");
          scheduleReconnect();
        };

        ws.onerror = () => {
          if (!isMounted) return;
          setStatus("RECONNECTING");
          ws.close();
        };
      } catch {
        if (isMounted) {
          setStatus("DISCONNECTED");
          scheduleReconnect();
        }
      }
    };

    const scheduleReconnect = () => {
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      const delay = Math.min(1000 * Math.pow(1.5, reconnectAttemptsRef.current), 15000);
      reconnectAttemptsRef.current += 1;
      reconnectTimeoutRef.current = setTimeout(() => {
        connect();
      }, delay);
    };

    connect();

    // Periodic ping to keep alive
    const interval = setInterval(() => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ type: "PING" }));
      }
    }, 30000);

    return () => {
      isMounted = false;
      clearInterval(interval);
      if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return {
    status,
    latestEvent,
    latestAlert,
    connectedClients,
  };
}
