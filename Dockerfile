FROM python:3.10-slim

# Installa librerie di sistema necessarie
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file principali
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto (app.py)
COPY app.py .

# Comando di default
CMD ["python", "app.py"]
