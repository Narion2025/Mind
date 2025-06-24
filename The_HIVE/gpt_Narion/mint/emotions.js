
// emotions.js
// Analysemodul für Emotionen basierend auf Textinput

export async function analyzeEmotion(inputText) {
  // Simpler Keyword-basierter Emotionsparser
  const emotions = {
    sadness: ["leer", "einsam", "verloren", "traurig", "grau"],
    joy: ["freue", "glücklich", "liebe", "leicht", "sonne"],
    anger: ["wütend", "hass", "explodieren", "schreien", "aggressiv"],
    fear: ["angst", "zitter", "unsicher", "verstecken", "flucht"]
  };

  let dominantEmotion = "neutral";
  let maxMatches = 0;

  for (const [emotion, keywords] of Object.entries(emotions)) {
    const matches = keywords.reduce(
      (count, word) => count + (inputText.toLowerCase().includes(word) ? 1 : 0),
      0
    );
    if (matches > maxMatches) {
      maxMatches = matches;
      dominantEmotion = emotion;
    }
  }

  return {
    mood: dominantEmotion,
    confidence: maxMatches > 0 ? maxMatches / 5 : 0.1
  };
}
