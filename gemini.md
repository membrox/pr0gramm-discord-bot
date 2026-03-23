# pr0gramm Discord Bot – Projektkontext für Antigravity

## Projektübersicht

Ein Discord-Bot, der den neuesten Top-Beitrag von [pr0gramm.com](https://pr0gramm.com/top) per Slash-Command `/pr0gramm` in einen Discord-Channel postet. Der Bot zeigt Bilder als Embed und Videos als direkten Link an.

## Technologie-Stack

| Komponente | Details |
|---|---|
| Sprache | Python 3.10+ |
| Discord-Bibliothek | `discord.py >= 2.3.0` (app_commands / Slash-Commands) |
| HTTP-Client | `aiohttp >= 3.9.0` (async) |
| Config | `python-dotenv >= 1.0.0` – lädt `.env` |
| Deployment | Läuft als dauerhafter Prozess auf einem Linux-Server |

## Projektstruktur

```
Pro bot/
├── bot.py            # Hauptdatei: Bot-Logik und /pr0gramm Command
├── requirements.txt  # Python-Abhängigkeiten
├── .env              # ⛔ NICHT ins Git! Enthält DISCORD_TOKEN
├── .env.example      # Vorlage ohne echte Werte – wird committed
├── .gitignore        # .env und andere sensible Dateien ausgeschlossen
├── README.md         # Setup-Anleitung
└── gemini.md         # Diese Datei – Kontext für KI-Assistenten
```

## Wichtige Umgebungsvariablen

| Variable | Beschreibung |
|---|---|
| `DISCORD_TOKEN` | Discord Bot-Token aus dem Developer Portal |

➡️ Die `.env`-Datei wird **niemals** ins Git committed. Stattdessen gibt es `.env.example` als Vorlage.

## Kernlogik (`bot.py`)

- `Pr0Bot(discord.Client)` – Bot-Klasse mit Slash-Command-Tree
- `setup_hook()` – Synchronisiert Slash-Commands beim Start mit Discord
- `on_ready()` – Setzt Status auf „Watching pr0gramm.com/top"
- `/pr0gramm` Command – ruft `https://pr0gramm.com/api/items/get?promoted=1&flags=1` ab, überspringt gepinnte Posts, und sendet Embed (Bild) oder direkten Link (Video)

**Content-Filter:** `flags=1` = nur SFW. Für NSFW: `flags=7` in `bot.py` ändern.

## Deployment auf Server

```bash
# 1. Repo klonen
git clone <repo-url>
cd "Pro bot"

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. .env anlegen
cp .env.example .env
nano .env  # DISCORD_TOKEN eintragen

# 4. Bot starten (im Hintergrund mit systemd oder screen)
python bot.py

# Mit screen (empfohlen für einfaches Deployment):
screen -S pr0bot python bot.py
# Detach: Ctrl+A, dann D
# Wieder verbinden: screen -r pr0bot
```

## Bekannte Eigenheiten

- Videos (`.mp4`, `.webm`) können in Discord-Embeds nicht direkt eingebettet werden → werden als direkter Link gesendet
- Die pr0gramm-API gibt manchmal gepinnte Beiträge zurück – diese werden übersprungen
- Slash-Commands müssen beim ersten Start ca. 1 Stunde warten, bis sie bei Discord global registriert sind

## Nächste mögliche Features

- `[x]` Zufälligen statt neuesten Top-Post zeigen (`/pr0gramm random`)
- `[x]` Systemd-Service-Datei für Auto-Start nach Server-Neustart

---

### 🐧 Linux Deployment (Ready)
Der Bot ist nun für den Linux-Server optimiert:
1. `pr0bot.service` liegt bereit – einfach nach `/etc/systemd/system/` kopieren und anpassen.
2. Der Code läuft stabil als Hintergrunddienst.
3. Slash-Commands sind für globale Nutzung synchronisiert.
