import asyncio
from src.config import get_config
from src.common.implementations.mosquitto_broker import MosquittoProducer
from src.edge.producers.sensor_producer import SensorProducer
from src.common.utils.logging_config import setup_logging

logger = setup_logging("edge_service")

async def main():
    config = get_config()
    
    # Инициализируем MQTT producer
    producer = MosquittoProducer(
        host=config["mqtt"]["host"],
        port=config["mqtt"]["port"]
    )
    
    logger.info("Initializing MQTT producer")
    await producer.connect()
    
    # Создаем producer для сенсора
    sensor = SensorProducer(
        producer=producer,
        sensor_id=config["edge"]["device_id"],
        topic_prefix=config["edge"]["sensor_topic_prefix"]
    )
    
    logger.info("Starting telemetry sending loop")
    try:
        while True:
            await sensor.send_telemetry(
                value=23.5,
                metadata={"unit": "celsius"}
            )
            logger.debug("Telemetry data sent successfully")
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        logger.warning("Received shutdown signal")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    finally:
        logger.info("Disconnecting from MQTT broker")
        await producer.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application shutdown complete") 