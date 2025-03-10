FROM python:3.10-slim

# Installa i pacchetti di sistema necessari
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia i file
WORKDIR /app
COPY . /app

# Installa i requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
