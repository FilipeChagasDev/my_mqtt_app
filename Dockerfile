FROM python:3.11-slim
WORKDIR /app
COPY mqtt_listener/requirements.txt ./requirements.txt
COPY mqtt_listener/app.py ./app.py
COPY mqtt_listener/db.py ./db.py
COPY mqtt_listener/models.py ./models.py

#COPY .env .env
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
