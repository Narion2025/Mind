import React, { useState } from "react";

export default function HumanAIVoiceUI() {
  const [text, setText] = useState("");
  const [user, setUser] = useState("Eloise");
  const [emotion, setEmotion] = useState("joy");
  const [isPlaying, setIsPlaying] = useState(false);

  const handleSpeak = async () => {
    setIsPlaying(true);
    const response = await fetch("http://localhost:8080/speak", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user, text, emotion })
    });

    const blob = await response.blob();
    const audioUrl = URL.createObjectURL(blob);
    const audio = new Audio(audioUrl);
    audio.play();
    audio.onended = () => setIsPlaying(false);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🧠 Human.AI Voice</h1>
      <textarea
        rows="3"
        className="w-full p-2 border mb-2"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Was soll gesagt werden?"
      />
      <div className="flex gap-2 mb-2">
        <select value={user} onChange={(e) => setUser(e.target.value)} className="p-2 border">
          <option value="Eloise">Eloise</option>
          <option value="Sam">Sam</option>
          <option value="Narion">Narion</option>
        </select>
        <select value={emotion} onChange={(e) => setEmotion(e.target.value)} className="p-2 border">
          <option value="joy">Freude</option>
          <option value="sadness">Trauer</option>
          <option value="anger">Wut</option>
          <option value="fear">Angst</option>
          <option value="neutral">Neutral</option>
        </select>
      </div>
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        onClick={handleSpeak}
        disabled={!text || isPlaying}
      >
        🎤 Sprechen lassen
      </button>
    </div>
  );
}
