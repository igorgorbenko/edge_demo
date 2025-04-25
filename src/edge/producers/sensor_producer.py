from datetime import datetime

from src.common.interfaces.message_broker import MessageProducer
from src.common.models.telemetry import TelemetryData


class SensorProducer:
    def __init__(self, producer: MessageProducer, sensor_id: str, topic_prefix: str = "telemetry"):
        self.producer = producer
        self.sensor_id = sensor_id
        self.topic = f"{topic_prefix}/{sensor_id}"

    async def send_telemetry(self, value: any, metadata: dict = None) -> None:
        telemetry = TelemetryData(
            sensor_id=self.sensor_id,
            timestamp=datetime.utcnow(),
            value=value,
            metadata=metadata
        )
        await self.producer.publish(self.topic, telemetry.to_dict()) 