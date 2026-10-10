import json
import urllib.request
from deep_translator import GoogleTranslator

app_ids = {
    "7_days_to_die": "252490",
    "war_thunder": "236390",
    "dead_by_daylight": "381210",
    "conan_exiles": "440900",
    "palworld": "1623730",
}

translator = GoogleTranslator(source='auto', target='de')
news_data = {}

for game, app_id in app_ids.items():
  url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={app_id}&count=6&maxlength=400&format=json"
  try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
      data = json.loads(response.read().decode())
      items = data.get("appnews", {}).get("newsitems", [])

      # Texte ins Deutsche übersetzen
      for item in items:
        try:
          if item.get("title"):
            item["title"] = translator.translate(item["title"])
          if item.get("contents"):
            item["contents"] = translator.translate(item["contents"])
        except Exception as trans_err:
          print(f"Übersetzungsfehler bei {game}: {trans_err}")

      news_data[game] = items
  except Exception as e:
    print(f"Fehler bei {game}: {e}")
    news_data[game] = []

with open("steam_news.json", "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=2)

print("Steam News erfolgreich auf Deutsch aktualisiert!")
