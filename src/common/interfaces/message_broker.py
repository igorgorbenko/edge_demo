from abc import ABC, abstractmethod
from typing import Callable, Any

class MessageProducer(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def publish(self, topic: str, message: Any) -> None:
        pass

class MessageConsumer(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback: Callable[[str, Any], None]) -> None:
        pass

    @abstractmethod
    async def unsubscribe(self, topic: str) -> None:
        pass 
