import json
from typing import Callable, Any
import paho.mqtt.client as mqtt

from src.common.interfaces.message_broker import MessageProducer, MessageConsumer

class MosquittoProducer(MessageProducer):
    def __init__(self, host: str, port: int = 1883, username: str = None, password: str = None):
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        if username and password:
            self.client.username_pw_set(username, password)

    async def connect(self) -> None:
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    async def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    async def publish(self, topic: str, message: Any) -> None:
        if isinstance(message, (dict, list)):
            message = json.dumps(message)
        self.client.publish(topic, message)

class MosquittoConsumer(MessageConsumer):
    def __init__(self, host: str, port: int = 1883, username: str = None, password: str = None):
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        if username and password:
            self.client.username_pw_set(username, password)
        self.callbacks = {}

    async def connect(self) -> None:
        self.client.on_message = self._on_message
        self.client.connect(self.host, self.port)
        self.client.loop_start()

    async def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    async def subscribe(self, topic: str, callback: Callable[[str, Any], None]) -> None:
        self.callbacks[topic] = callback
        self.client.subscribe(topic)

    async def unsubscribe(self, topic: str) -> None:
        self.client.unsubscribe(topic)
        self.callbacks.pop(topic, None)

    def _on_message(self, client, userdata, message):
        topic = message.topic
        if topic in self.callbacks:
            try:
                payload = json.loads(message.payload.decode())
            except json.JSONDecodeError:
                payload = message.payload.decode()
            self.callbacks[topic](topic, payload) 