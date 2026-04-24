import { useState } from "react";

function ReviewInput({ onAnalyze }) {
  const [text, setText] = useState("");

  return (
    <div>
      <input
        type="text"
        placeholder="Enter review..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        className="analyze-btn"
        onClick={() => onAnalyze(text)}
      >
        Analyze
      </button>
    </div>
  );
}

export default ReviewInput;