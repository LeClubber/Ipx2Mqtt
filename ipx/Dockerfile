FROM python:3-alpine
ENV HTTP_PORT 8080
ENV MQTT_PORT 1883
ENV MQTT_HOST mqtt
ENV MQTT_TOPIC ipx
ENV IPX_HOST 192.168.1.1
ENV IPX_API_KEY apiKey
ENV IPX_PULL_STATUS 0
WORKDIR /usr/src/ipx
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-u", "server.py"]