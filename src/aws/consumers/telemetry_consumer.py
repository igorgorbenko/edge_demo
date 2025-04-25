import asyncio
from typing import List
import json

from src.common.interfaces.message_broker import MessageConsumer
from src.common.models.telemetry import TelemetryData
from src.aws.services.storage_service import StorageService
from src.aws.services.inference_service import InferenceService

class TelemetryConsumer:
    def __init__(
        self, 
        consumer: MessageConsumer,
        storage_service: StorageService,
        inference_service: InferenceService,
        topics: List[str]
    ):
        self.consumer = consumer
        self.storage_service = storage_service
        self.inference_service = inference_service
        self.topics = topics

    async def start(self):
        await self.consumer.connect()
        for topic in self.topics:
            await self.consumer.subscribe(topic, self.handle_message)

    async def handle_message(self, topic: str, message: dict):
        # Сохраняем данные
        await self.storage_service.store(message)
        
        # Отправляем на инференс
        inference_result = await self.inference_service.process(message)
        if inference_result.needs_action:
            # Здесь будет логика отправки управляющего воздействия
            pass 