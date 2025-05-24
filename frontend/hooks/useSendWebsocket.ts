import { useWebSocket } from "provider/websocket";
import { useCallback } from "react";
import { WebSocketOutboundMessage } from "websocket/types";

export function useSendWebSocket() {
  const { ws, connectionStatus } = useWebSocket();

  const sendMessage = useCallback(
    (message: WebSocketOutboundMessage): boolean => {
      if (connectionStatus !== "connected") {
        console.warn("WebSocket not connected. Message not sent:", message);
        return false;
      }
      return ws.send(message);
    },
    [ws, connectionStatus]
  );

  return sendMessage;
}
