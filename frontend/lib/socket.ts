let socket: WebSocket | null = null;

export const connectSocket = (token: string) => {
  socket = new WebSocket(`wss://your-server.com/?token=${token}`);

  socket.onopen = () => {
    // socket?.send(JSON.stringify({ type: "auth", token })); probalby not needed because of query param
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Message:", data);
  };

  socket.onerror = (error) => {
    console.error("WebSocket Error:", error);
  };

  socket.onclose = () => {
    console.log("WebSocket closed");
  };
};

export const sendMessage = (msg: object) => {
  if (socket?.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(msg));
  }
};
