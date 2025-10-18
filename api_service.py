import requests
import os
import time

class FootballAPIService:
    def __init__(self):
        # Usa tu token de Football-Data.org desde las variables secretas
        self.api_key = os.getenv("FOOTBALL_DATA_TOKEN", "aqui-va-tu-token")
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_key}

    def get_live_matches(self):
        """Obtiene todos los partidos en vivo."""
        try:
            response = requests.get(f"{self.base_url}/matches?status=LIVE", headers=self.headers, timeout=20)
            response.raise_for_status()
            data = response.json()
            matches = data.get("matches", [])
            if not matches:
                return ["⚽ No hay partidos en vivo actualmente."]
            mensajes = []
            for match in matches:
                comp = match["competition"]["name"]
                home = match["homeTeam"]["name"]
                away = match["awayTeam"]["name"]
                score = match["score"]["fullTime"]
                mensajes.append(f"🏆 {comp}\n{home} {score['home']} - {score['away']} {away}")
            return mensajes
        except Exception as e:
            return [f"❌ Error al obtener datos: {e}"]

# Ejemplo rápido si ejecutas este archivo directamente:
if __name__ == "__main__":
    api = FootballAPIService()
    while True:
        for m in api.get_live_matches():
            print(m)
        print("Actualizado...\n")
        time.sleep(60)
