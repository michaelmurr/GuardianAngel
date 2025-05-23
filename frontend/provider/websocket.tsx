

// WebSocketContext.tsx
import React, { createContext, useContext, useEffect, useMemo, useRef, useState } from "react";
import { ConnectionStatus } from "websocket/types";
import { WebSocketClient } from "websocket/WebSocketClient";


interface WebSocketContextValue {
  ws: WebSocketClient;
  connectionStatus: ConnectionStatus;
}

const WebSocketContext = createContext<WebSocketContextValue | null>(null);

export const WebSocketProvider: React.FC<{
  children: React.ReactNode;
  baseUrl: string;
  jwtToken: string;
  deviceId: string;
}> = ({ children, baseUrl, jwtToken, deviceId }) => {
  const wsClientRef = useRef<WebSocketClient>(new WebSocketClient().connect(baseUrl, jwtToken, deviceId));
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>("disconnected");

  useEffect(() => {
    const wsClient = wsClientRef.current

    const unsubscribe = wsClient.on("connectionChange", (data) => {
      setConnectionStatus(data.status)
    })

    return () => unsubscribe()
  }, [])

  const value = useMemo(
    () => ({
      ws: wsClientRef.current,
      connectionStatus,
    }),
    [connectionStatus]
  );

  return (
    <WebSocketContext.Provider value={value}>
      {connectionStatus == "connected" ? children : null}
    </WebSocketContext.Provider>
  );
};

export function useWebSocket() {
  const ctx = useContext(WebSocketContext);
  if (!ctx) {
    throw new Error("useWebSocket must be used within a WebSocketProvider");
  }
  return ctx;
}
