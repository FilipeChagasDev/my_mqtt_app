# Pacotes nativos
import os

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
    CLIENT_ID = 'listener'
    USERNAME = os.getenv("MQTT_LISTENER_USERNAME")
    PASSWORD = os.getenv("MQTT_LISTENER_PASSWORD")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT!")
        client.subscribe(Settings.TOPIC)
    else:
        print(f"Falha na conexão, código de retorno {rc}")
        client.disconnect()


def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")


def main():
    client = mqtt_client.Client(client_id=Settings.CLIENT_ID)
    client.username_pw_set(Settings.USERNAME, Settings.PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(Settings.BROKER, Settings.PORT)
    client.loop_forever()


if __name__ == "__main__":
    main()
