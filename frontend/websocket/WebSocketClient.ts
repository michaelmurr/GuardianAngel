import {
  ConnectionStatus,
  EventCallback,
  EventMap,
  WebSocketInboundMessage,
  WebSocketOutboundMessage,
} from "./types";

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private listeners = new Map<keyof EventMap, Set<EventCallback>>();
  private reconnectAttempts = 0;
  private readonly maxReconnectAttempts = 5;
  private readonly reconnectInterval = 3000;
  private reconnectIntervalId: NodeJS.Timeout | null = null;
  private url: string | null = null;

  public isConnected = false;
  public connectionStatus: ConnectionStatus = "disconnected";

  private _connect() {
    if (!this.url) {
      console.log("WebSocket URL is not set");
      return;
    }

    if (this.connectionStatus === "connected") {
      return;
    }

    try {
      this.setConnectionStatus("connecting");
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.setConnectionStatus("connected");
        if (this.reconnectIntervalId) {
          clearInterval(this.reconnectIntervalId);
          this.reconnectIntervalId = null;
        }
      };

      this.ws.onmessage = (event: MessageEvent) => {
        try {
          const data: WebSocketInboundMessage = JSON.parse(event.data);
          if (!data.type) {
            console.log("Invalid message type")
          }
          switch (data.type) {
            case "emergency_nearby":
              this.emit("emergencyNearby", data.payload)
            default:
              console.log(`Invalid message type ${data.type}`)
          }
        } catch (error) {
          console.error("Failed to parse message:", error);
          this.emit("error", error as Error);
        }
      };

      this.ws.onclose = (event: CloseEvent) => {
        this.isConnected = false;
        this.setConnectionStatus("disconnected");
        this.attemptReconnect();
      };

      this.ws.onerror = (error: Event) => {
        this.setConnectionStatus("error");
        this.emit("error", error);
      };
    } catch (error) {
      console.error("WebSocket connection failed:", error);
      this.setConnectionStatus("error");
      this.attemptReconnect();
    }
  }

  connect(base_url: string, jwtToken: string, device_id: string): WebSocketClient {
    this.url = `${base_url}/ws/live?token=${jwtToken}&device_id=${device_id}`;
    this._connect();
    return this
  }

  private setConnectionStatus(status: ConnectionStatus): void {
    this.connectionStatus = status;
    this.emit("connectionChange", {
      connected: status === "connected",
      status,
    });
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      if (!this.reconnectIntervalId) {
        this.reconnectIntervalId = setInterval(() => {
          if (this.connectionStatus !== "connected") {
            this.reconnectAttempts++;
            console.log(
              `Reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}`,
            );
            this._connect();
          } else {
            if (this.reconnectIntervalId) {
              clearInterval(this.reconnectIntervalId);
              this.reconnectIntervalId = null;
            }
          }
        }, this.reconnectInterval);
      }
    } else {
      console.error("Max reconnection attempts reached");
      this.emit(
        "error",
        new Error("Connection failed after maximum retry attempts"),
      );
      if (this.reconnectIntervalId) {
        clearInterval(this.reconnectIntervalId);
        this.reconnectIntervalId = null;
      }
    }
  }

  send(data: WebSocketOutboundMessage): boolean {
    console.log(`SENDING ${data}`)
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
      return true;
    }
    console.warn("WebSocket not connected, message not sent:", data);
    return false;
  }

  on<K extends keyof EventMap>(
    event: K,
    callback: EventCallback<EventMap[K]>,
  ): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);

    return () => {
      this.listeners.get(event)?.delete(callback);
    };
  }

  private emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    this.listeners.get(event)?.forEach((callback) => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Event callback error for ${String(event)}:`, error);
      }
    });
  }

  disconnect(): void {
    if (this.reconnectIntervalId) {
      clearInterval(this.reconnectIntervalId);
      this.reconnectIntervalId = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.isConnected = false;
    this.connectionStatus = "disconnected";
  }

  getConnectionInfo() {
    return {
      isConnected: this.isConnected,
      status: this.connectionStatus,
      reconnectAttempts: this.reconnectAttempts,
    };
  }
}
