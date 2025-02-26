FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file requirements.txt
COPY requirements.txt .

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il contenuto della directory locale nell'immagine Docker
COPY . .

# Assicurati che il file app.py sia eseguibile
RUN chmod +x /app/app.py

# Esegui l'applicazione
CMD ["python", "app.py"]
