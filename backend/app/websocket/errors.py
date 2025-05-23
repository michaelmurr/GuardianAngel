class WebSocketError(Exception):
    def to_message(self):
        return {"type": "error", "error": self.__class__.__name__, "message": str(self)}


class UnknownMessageFormat(WebSocketError):
    def __init__(self, message="Unknown message format"):
        super().__init__(message)
