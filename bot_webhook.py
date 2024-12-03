# 1. Basis-Image
FROM python:3.9-slim

# 2. Arbeitsverzeichnis erstellen
WORKDIR /app

# 3. Benötigte Dateien kopieren
COPY bot_webhook.py /app/bot_webhook.py
COPY requirements.txt /app/requirements.txt

# 4. Benötigte Pakete installieren
RUN pip install --no-cache-dir -r requirements.txt

# 5. Port für Flask öffnen
EXPOSE 5000

# 6. Befehl zum Starten der Flask-Anwendung
CMD ["python", "bot_webhook.py"]
