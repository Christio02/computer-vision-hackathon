import { Button } from "@/components/ui/button";
import { useRef, useState } from "react";

export default function CameraAnalyzer() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [output, setOutput] = useState<string | null>(null);

  const handleStopCamera = async () => {
    if (videoRef.current && videoRef.current.srcObject) {
      try {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach((track) => track.stop());
        videoRef.current.srcObject = null;
      } catch (error) {
        console.error("Error stopping camera", error);
      }
    }
  };

  const handleOpenCamera = async () => {
    if (navigator.mediaDevices && videoRef.current) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
        setTimeout(captureFrameAndAnalyze, 3000);
      } catch (error) {
        console.error("Error accessing camera", error);
      }
    }
  };

  const captureFrameAndAnalyze = async () => {
    if (!videoRef.current) return;
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.width;
    canvas.height = videoRef.current.height;
    const context = canvas.getContext("2d");

    if (context) {
      context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      // analyze frame, send to model and get prediction back
      const groceryItem = await analyzeFrame(canvas);
      setOutput(groceryItem);
    }
  };

  // dummy model
  const analyzeFrame = async (canvas: HTMLCanvasElement): Promise<string> => {
    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 1000));
    // Replace this with your model's inference result
    return "Banana";
  };

  return (
    <section className="flex flex-col items-center gap-3">
      <h3 className="text-2xl">Click to start camera</h3>
      <Button onClick={handleOpenCamera}>Open camera</Button>
      <video ref={videoRef} className="mt-4 w-80 border" />
      {output && (
        <div className="mt-4 text-xl">
          Model Output: <strong>{output}</strong>
        </div>
      )}
      <Button onClick={handleStopCamera}>Close camera</Button>
    </section>
  );
}
