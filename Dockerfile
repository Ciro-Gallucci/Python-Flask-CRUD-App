FROM python:3.8-slim

WORKDIR /app

# Copia i file del progetto
COPY . /app

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta per Flask
EXPOSE 5000

# Esegui l'applicazione Flask
CMD ["python", "app.py"]
