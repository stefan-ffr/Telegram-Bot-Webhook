# Telegram-Bot-Webhook


### Gesamtübersicht der Schritte
1. Projekt lokal vorbereiten.
2. Repository auf GitHub erstellen.
3. Projekt auf GitHub hochladen.
4. Docker-Setup erstellen (`Dockerfile`, `requirements.txt`).
5. GitHub Actions Workflow für automatischen Docker-Build erstellen.
6. Docker-Container automatisch veröffentlichen.
7. Secrets zu GitHub hinzufügen.
8. Container von Docker Hub oder GitHub Container Registry ausführen.

### Schritt 1: Projekt lokal vorbereiten
Zuerst bereitest du das Projekt lokal auf deinem Rechner vor. Du benötigst die folgenden Dateien:
- `bot_webhook.py`: Die eigentliche Python-Anwendung, die den Telegram-Bot-Webserver implementiert.
- `requirements.txt`: Eine Datei, die die Python-Abhängigkeiten enthält.
- `Dockerfile`: Ein Docker-Setup, das dein Projekt als Docker-Image erstellt.

#### `bot_webhook.py` (Python Script)
Erstelle die Datei `bot_webhook.py`:

```python
from flask import Flask, request, abort
import telegram

TOKEN = 'DEIN_BOT_TOKEN_HIER'
SECRET = 'YOUR_SECRET_HERE'  # Verwende hier dein generiertes Secret
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    secret_from_request = request.args.get('secret')
    if secret_from_request != SECRET:
        abort(403)  # Abweisung, falls das Secret nicht übereinstimmt

    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    bot.sendMessage(chat_id=chat_id, text=f"Du hast gesendet: {message_text}")

    return 'ok'

if __name__ == '__main__':
    app.run(port=5000)
```

#### `requirements.txt` (Python-Abhängigkeiten)
Erstelle eine Datei namens `requirements.txt`, die die benötigten Abhängigkeiten auflistet:

```
Flask
python-telegram-bot
```

### Schritt 2: Repository auf GitHub erstellen
- Gehe zu [GitHub](https://github.com).
- Klicke auf **New Repository**.
- Gib deinem Repository einen Namen, z.B. `telegram-bot-docker`.
- Erstelle das Repository.

### Schritt 3: Projekt auf GitHub hochladen
Füge dein Projekt zu GitHub hinzu:

```bash
# Initialisiere ein lokales Git-Repository
git init

# Füge alle Dateien hinzu
git add .

# Committe die Änderungen
git commit -m "Initial commit"

# Füge das Remote-Repository hinzu (ändere die URL entsprechend deinem Repo)
git remote add origin https://github.com/DEIN_USERNAME/telegram-bot-docker.git

# Pushe die Dateien auf GitHub
git push -u origin main
```

### Schritt 4: Docker-Setup erstellen
Erstelle eine `Dockerfile`, die den Docker-Build-Prozess definiert:

#### `Dockerfile`
```Dockerfile
# Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Benötigte Dateien kopieren
COPY bot_webhook.py /app/bot_webhook.py
COPY requirements.txt /app/requirements.txt

# Benötigte Pakete installieren
RUN pip install --no-cache-dir -r requirements.txt

# Port für Flask öffnen
EXPOSE 5000

# Befehl zum Starten der Flask-Anwendung
CMD ["python", "bot_webhook.py"]
```

### Schritt 5: GitHub Actions Workflow für automatischen Docker-Build erstellen
Erstelle den Workflow, damit GitHub den Docker-Container automatisch baut. Dies erfolgt in der Datei `.github/workflows/docker-image.yml`.

- Erstelle im Root-Verzeichnis einen Ordner `.github/workflows/`.
- Erstelle darin die Datei `docker-image.yml`:

```yaml
name: Docker Image CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      # 1. Check out the repository
      - name: Check out the repository
        uses: actions/checkout@v4

      # 2. Set up Docker Buildx (for building Docker images)
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      # 3. Log in to GitHub Container Registry (GHCR)
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      # 4. Build and push the Docker image
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository_owner }}/telegram-bot-webhook:latest
```

### Schritt 6: Docker-Container automatisch veröffentlichen
GitHub Actions verwendet **GitHub Container Registry (GHCR)**, um das Docker-Image zu veröffentlichen. Die veröffentlichte URL für das Docker-Image wird `ghcr.io/<GitHub-Benutzername>/telegram-bot-webhook:latest` sein.

### Schritt 7: Secrets zu GitHub hinzufügen (Optional für Docker Hub)
Falls du das Docker-Image zu Docker Hub pushen möchtest, musst du Zugangsdaten als Secrets speichern:

- Gehe zu deinem GitHub-Repository.
- Gehe auf **Settings**.
- Wähle **Secrets and variables** -> **Actions**.
- Füge neue Repository-Secrets hinzu (`DOCKER_USERNAME` und `DOCKER_PASSWORD`).

### Schritt 8: Container von der Container Registry ausführen
Sobald der Workflow erfolgreich ausgeführt wird, kannst du den Docker-Container auf jedem Server ausführen:

```bash
# Ausführung des Containers von GitHub Container Registry
docker run -d -p 5000:5000 ghcr.io/<GitHub-Benutzername>/telegram-bot-webhook:latest
```

Falls du Docker Hub verwendet hast, passe den Tag entsprechend an.

### Zusammenfassung
1. **Projekt vorbereiten**: Erstelle die notwendigen Dateien (`bot_webhook.py`, `requirements.txt`, `Dockerfile`).
2. **Repository erstellen und Projekt pushen**: Lade dein Projekt auf GitHub hoch.
3. **GitHub Actions Workflow**: Richte eine GitHub Actions Workflow-Datei ein, um das Docker-Image automatisch zu erstellen.
4. **Container Registry nutzen**: Der Workflow erstellt und veröffentlicht automatisch ein Docker-Image in der **GitHub Container Registry**.
5. **Deployment**: Starte den Container auf einem beliebigen Server mit `docker run`.

Mit dieser Anleitung kannst du deinen Telegram-Bot einfach und automatisiert in einem Docker-Container bereitstellen.
