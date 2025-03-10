# Usa un'immagine base di Python
FROM python:3.9

# Installa le dipendenze di sistema (es. default-mysql-client e pacchetti di sviluppo MySQL)
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    libmysqlclient-dev \  # Aggiungi pacchetti necessari per mysqlclient
    && rm -rf /var/lib/apt/lists/*  # Pulisci la cache di apt per ridurre le dimensioni dell'immagine

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt
COPY requirements.txt .

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice dell'applicazione
COPY . .

# Esponi la porta 5000
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["python", "app.py"]
