import json
import re
import urllib.request
from mtranslate import translate

app_ids = {
    "7_days_to_die": "252490",
    "war_thunder": "236390",
    "dead_by_daylight": "381210",
    "conan_exiles": "440900",
    "palworld": "1623730",
}


def clean_bbcode(text):
  if not text:
    return ""
  # Entfernt BBCode [url=...], [b], etc. für eine saubere Übersetzung
  text = re.sub(r"\[.*?\]", "", text)
  return text.strip()


news_data = {}

for game, app_id in app_ids.items():
  url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={app_id}&count=6&maxlength=400&format=json"
  try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
      data = json.loads(response.read().decode())
      items = data.get("appnews", {}).get("newsitems", [])

      for item in items:
        # 1. BBCode bereinigen
        raw_title = clean_bbcode(item.get("title", ""))
        raw_contents = clean_bbcode(item.get("contents", ""))

        # 2. Automatisch ins Deutsche übersetzen
        try:
          if raw_title:
            item["title"] = translate(raw_title, "de", "auto")
          if raw_contents:
            item["contents"] = translate(raw_contents, "de", "auto")
        except Exception as trans_err:
          print(f"Übersetzungsfehler bei {game}: {trans_err}")

      news_data[game] = items
  except Exception as e:
    print(f"Fehler beim Abrufen von {game}: {e}")
    news_data[game] = []

with open("steam_news.json", "w", encoding="utf-8") as f:
  json.dump(news_data, f, ensure_ascii=False, indent=2)

print("Steam News erfolgreich bereinigt und auf Deutsch übersetzt!")
