FROM python:3.9

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia solo il file dei requisiti e installa le dipendenze
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il contenuto del progetto nella cartella /app
COPY . /app

# Assicurati che app.py sia eseguibile
RUN chmod +x /app/app.py

# Comando per avviare l'app
CMD ["python", "/app/app.py"]
