FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY /var/jenkins_home/workspace/appdemo /app

CMD ["python", "app.py"]
