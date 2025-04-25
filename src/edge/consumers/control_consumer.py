from typing import Dict, Any, Callable

from src.common.interfaces.message_broker import MessageConsumer
from src.common.models.telemetry import ControlCommand

class ControlConsumer:
    def __init__(
        self,
        consumer: MessageConsumer,
        device_id: str,
        control_callback: Callable[[ControlCommand], None],
        topic: str = "control"
    ):
        self.consumer = consumer
        self.device_id = device_id
        self.control_callback = control_callback
        self.topic = f"{topic}/{device_id}"

    async def start(self) -> None:
        await self.consumer.connect()
        await self.consumer.subscribe(self.topic, self.handle_control_message)

    async def stop(self) -> None:
        await self.consumer.unsubscribe(self.topic)
        await self.consumer.disconnect()

    async def handle_control_message(self, topic: str, message: Dict[str, Any]) -> None:
        command = ControlCommand(**message)
        if command.device_id == self.device_id:
            await self.control_callback(command) 