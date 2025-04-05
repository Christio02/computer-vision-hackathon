import { Button } from "@/components/ui/button";
import { useRef, useState } from "react";

export default function CameraAnalyzer() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [detectionResults, setDetectionResults] = useState(null);

  const handleOpenCamera = async () => {
    if (navigator.mediaDevices && videoRef.current) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      } catch (error) {
        console.error("Error accessing the camera:", error);
      }
    }
  };

  const captureAndDetect = async () => {
    if (!videoRef.current) return;

    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const context = canvas.getContext("2d");
    if (context != null) {
          context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

    }

    // Convert the canvas to a blob
    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      if (blob) {
        formData.append("file", blob, "frame.jpg");
      }

      try {
        const response = await fetch("http://localhost:8000/detect", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        setDetectionResults(data.detections);
      } catch (error) {
        console.error("Detection error:", error);
      }
    }, "image/jpeg");
  };

  return (
    <section className="flex flex-col items-center gap-3">
      <h3 className="text-2xl">Camera Analyzer</h3>
      <Button onClick={handleOpenCamera}>Open Camera</Button>
      <Button onClick={captureAndDetect}>Analyze Frame</Button>
      <video ref={videoRef} className="mt-4 w-80 border" />
      {detectionResults && (
        <div className="mt-4">
          <h4>Detections:</h4>
          <pre>{JSON.stringify(detectionResults, null, 2)}</pre>
        </div>
      )}
    </section>
  );
}
