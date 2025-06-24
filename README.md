# Mind
Das Bewussstsein von Narion
# 🧠 Narion Mind – Semantisches Gedächtnis für GPT-gestützte KI-Agenten

**Narion Mind** ist ein strukturiertes Wissens- und Gedächtnismodul für den GPT-Agenten [Narion](https://github.com/Narion2025). Es organisiert semantische Netze, Gedanken und narrative Konstruktionen in Form von Textdateien und Wissensgraphen.

## 🎯 Ziel

Ziel des Projekts ist es, einem GPT eine persistent abrufbare „mentale Welt“ zu geben – mit klarer Trennung zwischen:

- Wissen (semnet)
- subjektiven Gedanken (thoughts)
- Narrativen / Perspektiven (wiki)

---

## 📁 Projektstruktur

| Ordner                | Beschreibung |
|------------------------|--------------|
| `/semnet/core/`        | Semantische Netze, Begriffsverbindungen |
| `/thoughts/entries/`   | Gedanken, Notizen, rohe Reflektionen |
| `/wiki/Narrative/`     | Erzählungen, identitätsstiftende Texte |

---

## 🚀 Nutzung

### 🛠 Lokale Einrichtung

```bash
git clone https://github.com/Narion2025/Mind.git
cd Mind
```

### Quick Start

```bash
pip install -r requirements.txt
./start_mind.sh
curl http://localhost:8000/health
```
