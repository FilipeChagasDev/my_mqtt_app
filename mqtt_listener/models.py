# Pacotes internos
from datetime import datetime

# Pacotes de terceiros
from sqlmodel import SQLModel, Field


# Modelos
class MQTTData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime
    sensor: str
    value: float

    __tablename__ = 'mqtt_data'