import { useWebSocket } from "provider/websocket";
import { useEffect, useRef } from "react";
import { EventCallback, EventMap } from "websocket/types";


export function useWebSocketEvent<K extends keyof EventMap>(
  event: K,
  callback: EventCallback<EventMap[K]>
) {
  const { ws } = useWebSocket();
  const callbackRef = useRef(callback)

  useEffect(() => {
    const unsubscribe = ws.on(event, callbackRef.current);
    return () => unsubscribe();
  }, [event, callback, ws]);
}
