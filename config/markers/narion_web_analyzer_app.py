
import streamlit as st
import yaml
import re
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Narion Web Analyzer", layout="wide")

st.title("🧠 Narion Analyzer – Web Interface")

uploaded_file = st.file_uploader("Lade eine Textdatei hoch (.txt)", type="txt")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8").lower()
    st.subheader("🔍 Textauszug")
    st.text(text[:1000] + "..." if len(text) > 1000 else text)

    col1, col2 = st.columns(2)

    # Load and evaluate Emergenzphänomen Marion
    with col1.expander("🌌 Marion-Analyse"):
        try:
            with open("Emergenzphänomen_Marion.yaml", "r", encoding="utf-8") as f:
                marion_data = yaml.safe_load(f)["Emergenzphänomen_Marion"]["conditions"]

            results = {}
            for cluster, entry in marion_data.items():
                matches = [t for t in entry["tokens"] if re.search(r"\b" + re.escape(t) + r"\b", text)]
                results[cluster] = len(matches) / len(entry["tokens"])

            st.bar_chart(results)

            for cluster, score in results.items():
                st.markdown(f"**{cluster}**: {score:.2f}" + (" ✅" if score >= 0.8 else ""))

        except Exception as e:
            st.warning("Fehler beim Laden der Marion-Markerdatei.")

    # MetaOverlay
    with col2.expander("🧩 Metamarker Overlay"):
        try:
            with open("o3_text_markers.yaml", "r", encoding="utf-8") as f:
                meta_data = yaml.safe_load(f)

            meta_scores = {}
            for overlay, tokens in meta_data.items():
                matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text)]
                meta_scores[overlay] = len(matches) / len(tokens)

            st.bar_chart(meta_scores)

        except:
            st.warning("Metamarker-Datei nicht gefunden.")

    # EmotionGuard
    with col1.expander("❤️ EmotionGuard"):
        try:
            with open("emotion_guard.yaml", "r", encoding="utf-8") as f:
                emo_data = yaml.safe_load(f)

            emo_scores = {}
            for cat, tokens in emo_data.items():
                matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text)]
                emo_scores[cat] = len(matches) / len(tokens)

            st.bar_chart(emo_scores)
        except:
            st.warning("EmotionGuard YAML fehlt.")

    # Levelmatrix
    with col2.expander("🌀 Spiral Dynamics Levels"):
        try:
            with open("enhanced_marker_config.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            levels = {}
            current = None
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    current = line[1:].strip()
                    levels[current] = []
                elif line:
                    levels[current].append(line)

            level_scores = {}
            for lvl, tokens in levels.items():
                matches = [t for t in tokens if re.search(r"\b" + re.escape(t) + r"\b", text)]
                level_scores[lvl] = len(matches) / len(tokens)

            st.bar_chart(level_scores)
        except:
            st.warning("Levelmatrix-Konfig nicht gefunden.")
