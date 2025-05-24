

// WebSocketContext.tsx
import React, { createContext, useContext, useEffect, useMemo, useRef, useState } from "react";
import { SafeAreaView } from "react-native";
import { Text } from "tamagui";
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
  const [wsClient, setWsClient] = useState<WebSocketClient | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>("disconnected");

  useEffect(() => {
    if (!jwtToken) return;

    const client = new WebSocketClient();
    const connectedClient = client.connect(baseUrl, jwtToken, deviceId);
    setWsClient(connectedClient);

    const unsubscribe = connectedClient.on("connectionChange", (data) => {
      setConnectionStatus(data.status);
    });

    return () => {
      unsubscribe();
      connectedClient.disconnect(); // if you have a disconnect method
    };
  }, [jwtToken]);

  const value = useMemo(() => {
    if (!wsClient) return null;
    return {
      ws: wsClient,
      connectionStatus,
    };
  }, [wsClient, connectionStatus]);

  if (!value || connectionStatus !== "connected") {
    return (
      <SafeAreaView>
        <Text>🔌 Not connected</Text>
      </SafeAreaView>
    );
  }

  return (
    <WebSocketContext.Provider value={value}>
      {children}
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
