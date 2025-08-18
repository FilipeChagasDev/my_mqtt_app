"""
app.py
Este arquivo implementa um listener MQTT que se conecta a um broker, escuta mensagens em um tópico específico,
decodifica o payload recebido e salva os dados em um banco de dados utilizando SQLModel. O listener é configurado
por variáveis de ambiente e utiliza callbacks para gerenciar eventos de conexão e recebimento de mensagens.
Principais funcionalidades:
- Carregamento de configurações via .env
- Inicialização do banco de dados
- Conexão ao broker MQTT com autenticação
- Inscrição em tópico e processamento de mensagens recebidas
- Persistência dos dados recebidos no banco de dados
"""

# Pacotes nativos
import os
import json
from datetime import datetime

# Pacotes de terceiros
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client
from sqlmodel import Session

from models import MQTTData
from db import engine, init_db


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


def save_to_database(data):
    """
    Salva os dados recebidos no banco de dados usando uma sessão SQLAlchemy.

    Parâmetros:
        data (dict): Um dicionário contendo os dados a serem salvos, compatível com o modelo MQTTData.

    Retorna:
        None
    """
    with Session(engine) as session:
        mqtt_data = MQTTData(**data)
        session.add(mqtt_data)
        session.commit()


def on_connect(client, userdata, flags, rc):
    """
    Função de callback chamada quando o cliente MQTT tenta se conectar ao broker.

    Args:
        client: Instância do cliente MQTT.
        userdata: Dados definidos pelo usuário, se houver.
        flags: Dicionário de flags de resposta do broker.
        rc: Código de retorno da tentativa de conexão.

    Comportamento:
        - Se a conexão for bem-sucedida (rc == 0), exibe mensagem de sucesso e realiza inscrição no tópico definido em Settings.TOPIC.
        - Caso contrário, exibe mensagem de erro com o código de retorno e desconecta o cliente.
    """
    if rc == 0:
        print("Conectado ao broker MQTT!")
        client.subscribe(Settings.TOPIC)
    else:
        print(f"Falha na conexão, código de retorno {rc}")
        client.disconnect()


def on_message(client, userdata, msg):
    """
    Função de callback chamada quando uma mensagem é recebida em um tópico MQTT.

    Args:
        client: Instância do cliente MQTT.
        userdata: Dados definidos pelo usuário.
        msg: Mensagem recebida, contendo o tópico e o payload.

    Esta função imprime a mensagem recebida, decodifica o payload como JSON
    e salva os dados no banco de dados.
    """
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    save_to_database(data)


def main():
    """
    Função principal que inicializa o banco de dados, configura o cliente MQTT com as credenciais e callbacks apropriados,
    conecta ao broker MQTT e inicia o loop de escuta de mensagens indefinidamente.
    Esta função realiza as seguintes etapas:
    1. Inicializa o banco de dados.
    2. Cria e configura o cliente MQTT.
    3. Define funções de callback para conexão e recebimento de mensagens.
    4. Conecta ao broker MQTT.
    5. Inicia o loop para escutar mensagens continuamente.
    """
    init_db()
    client = mqtt_client.Client(client_id=Settings.CLIENT_ID)
    client.username_pw_set(Settings.USERNAME, Settings.PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(Settings.BROKER, Settings.PORT)
    client.loop_forever()


if __name__ == "__main__":
    main()
