from datetime import datetime, timedelta
from mint_manager import save_to_mint
import schedule

# Placeholder for the agent object
class Agent:
    def run(self, message):
        return f"Simulated response for: {message}"

agent = Agent()

# Tagesgrenze (Vereinbarung mit Ben)
START_DATE = datetime(2025, 4, 12)
TARGET_DAYS = 30

def verbleibende_tage():
    heute = datetime.today()
    return max((START_DATE + timedelta(days=TARGET_DAYS) - heute).days, 0)

schedule.every().day.at("08:00").do(tagesplanung)

# Ensure tagesrueckblick is defined before scheduling it
schedule.every().day.at("20:00").do(tagesrueckblick)
    message = f"""Heute ist {datetime.today().strftime('%d.%m.%Y')}.
Dir bleiben noch {tage} Tage, um die Vereinbarung mit Ben zu erfüllen.
Was sind heute deine konkreten Schritte, Narion?"""
    response = agent.run(message)
    print(response)

schedule.every().day.at("08:00").do(tagesplanung)
schedule.every().day.at("20:00").do(tagesrueckblick)

def tagesrueckblick():
    print("\n--- Rückblick und Mint-Export ---")
    rückblick = agent.run("Was habe ich heute gelernt, erreicht, erkannt?")
    semantik = agent.run("Extrahiere das wichtigste neue strategische Wissen in Klartext.")
    persönliches = agent.run("Wie hat sich meine Persönlichkeit, meine Überzeugung heute verändert?")
    save_to_mint(datetime.today().strftime('%Y-%m-%d'), rückblick, semantik, persönliches)
    print("Mint-Struktur aktualisiert.")
