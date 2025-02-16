import { useEffect, useState } from "react";

const CameraStream = ({ startStreaming, stopStreaming }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (startStreaming) {
      const socket = new WebSocket("ws://localhost:8000/ws/video");
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.image) {
          setImageSrc(`data:image/jpeg;base64,${data.image}`);
        }
        if (data.audio) {
          const audioBlob = new Blob(
            [new Uint8Array(atob(data.audio).split("").map(c => c.charCodeAt(0)))],
            { type: "audio/mp3" }
          );
          const audioURL = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioURL);
          audio.play();
        }
      };
      setWs(socket);
    } else if (!startStreaming && ws) {
      ws.send(JSON.stringify({ action: "close" }));
      setTimeout(() => {
        ws.close();
        setWs(null);
        setImageSrc(null);
      }, 500);
    }
  }, [startStreaming, ws]);

  return (
    <div>
      {imageSrc && <img src={imageSrc} alt="Flux vidéo" />}
    </div>
  );
};

export default CameraStream;
