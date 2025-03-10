FROM python:3.9-slim

# Installa le dipendenze di sistema
RUN apt-get update && apt-get install -y \
    default-mysql-client \  # Oppure mariadb-client
    && rm -rf /var/lib/apt/lists/*

# Copia il codice dell'applicazione
COPY . /app
WORKDIR /app

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta 5000
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["python", "app.py"]
