# Pacotes nativos
import os
import random
import time

# Pacotes de terceiros
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client

# Carregamento de variáveis de ambiente do .env
load_dotenv() 

# Constantes de configuração
class Settings:
    BROKER = os.getenv("MQTT_BROKER")
    PORT = int(os.getenv("MQTT_PORT"))
    TOPIC = 'mytopic'
    CLIENT_ID = 'sensor_0'
    USERNAME = 'tenant_0'
    PASSWORD = 'password_0'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT!")
        else:
            print(f"Falha na conexão, código {rc}")

    client = mqtt_client.Client(client_id=Settings.CLIENT_ID)
    client.username_pw_set(Settings.USERNAME, Settings.PASSWORD)
    client.on_connect = on_connect
    client.connect(Settings.BROKER, Settings.PORT)
    return client


def publish(client):
    while True:
        value = random.uniform(20.0, 30.0)  # Simula valor de sensor
        result = client.publish(Settings.TOPIC, f"{value:.2f}")
        status = result[0]
        if status == 0:
            print(f"Enviado `{value:.2f}` para o tópico `{Settings.TOPIC}`")
        else:
            print(f"Falha ao enviar mensagem para o tópico {Settings.TOPIC}")
        time.sleep(1)


if __name__ == '__main__':
    mqtt_client_instance = connect_mqtt()
    mqtt_client_instance.loop_start()
    publish(mqtt_client_instance)