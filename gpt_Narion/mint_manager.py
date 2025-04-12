import datetime
from pathlib import Path

MINT_PATH = Path("mint/mint_log.txt")
MINT_PATH.parent.mkdir(exist_ok=True)

def save_to_mint(date, memory_content, insights, personality_note):
    with open(MINT_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n=== Mint-Log für {date} ===\n")
        f.write(f"📘 Persönliche Erinnerung:\n{memory_content}\n")
        f.write(f"🧠 Semantisches Wissen:\n{insights}\n")
        f.write(f"❤️ Persönlichkeitskern:\n{personality_note}\n")
        f.write("="*40 + "\n")
