import os

from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

# Carregamento de variáveis de ambiente do .env
load_dotenv() 

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas no metadata do SQLModel.
    Esta função utiliza o objeto 'engine' para criar as tabelas no banco de dados conforme os modelos definidos.
    """
    SQLModel.metadata.create_all(engine)