# pr0gramm Discord Bot 🤖

Postet das neueste Top-Bild von [pr0gramm.com](https://pr0gramm.com/top) mit dem Slash-Command `/pr0gramm`.

## Setup

### 1. Discord Bot erstellen
1. Gehe zu [discord.com/developers/applications](https://discord.com/developers/applications)
2. Klicke „New Application" → gib einen Namen ein
3. Klicke links auf „Bot" → „Add Bot"
4. Aktiviere unter „Privileged Gateway Intents": **keine** zusätzlichen Intents nötig
5. Kopiere den **Token** (Reset Token → kopieren)
6. Unter „OAuth2 → URL Generator":
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Attach Files`
   - Generierte URL im Browser öffnen → Bot zu deinem Server einladen

### 2. Projekt einrichten

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# .env Datei anlegen
copy .env.example .env
# Öffne .env und trage deinen Token ein: DISCORD_TOKEN=dein_token
```

### 3. Bot starten

```bash
python bot.py
```

### 4. Benutzen

Schreibe in einem Discord-Channel:
```
/pr0gramm
```

Der Bot postet das neueste Top-Bild (SFW) als Embed inklusive Upvotes, Username und Link.

## Konfiguration

| Variable | Beschreibung |
|---|---|
| `DISCORD_TOKEN` | Dein Discord Bot Token |

**Content-Filter:** Standardmäßig werden nur SFW-Inhalte gepostet (`flags=1`).  
Um alle Inhalte zu erlauben (NSFW), ändere in `bot.py`:
```python
PR0GRAMM_API = "https://pr0gramm.com/api/items/get?promoted=1&flags=7"
```
⚠️ Stelle sicher, dass der Channel als NSFW markiert ist!
