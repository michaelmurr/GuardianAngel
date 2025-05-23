interface WebSocketBaseMessage<TType extends string, TPayload> {
  type: TType;
  payload: TPayload;
}

export interface Location {
  longitude: number;
  latitude: number;
}


// INBOUND MESSAGES
export interface InboundMessage {
  type: "emergency_nearby"
}

export type InboundMessageEmergencyNearby = WebSocketBaseMessage<"emergency_nearby", ErmegencyNearbyPayload>

export interface ErmegencyNearbyPayload {
  user_id: string
  location: Location
}

export type WebSocketInboundMessage =
  | InboundMessageEmergencyNearby

interface UserRealtimeData {
  location: Location;
  battery: number;
  speed: number;
}

// OUTBOUND MESSAGES
export type WebSocketOutboundMessage =
  | WebSocketBaseMessage<"status", UserRealtimeData>

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error'

export interface ConnectionEvent {
  connected: boolean
  status: ConnectionStatus
}

export type EventCallback<T = any> = (data: T) => void

export type EventMap = {
  connectionChange: ConnectionEvent
  emergencyNearby: ErmegencyNearbyPayload
  error: Event | Error
}
