import CameraAnalyzer from "./components/CameraAnalyzer";

function App() {
  return (
    <section className="flex flex-col items-center p-3 gap-7">
      <h1 className="text-4xl">Welcome to grocery vision!</h1>
      <CameraAnalyzer />
    </section>
  );
}

export default App;
