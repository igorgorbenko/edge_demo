import asyncio
from src.config import get_config
from src.common.implementations.mosquitto_broker import MosquittoConsumer
from src.aws.consumers.telemetry_consumer import TelemetryConsumer
from src.aws.services.storage_service import StorageService
from src.aws.services.inference_service import InferenceService
from src.common.utils.logging_config import setup_logging

logger = setup_logging("aws_service")

async def main():
    config = get_config()
    
    logger.info("Initializing AWS services")
    storage_service = StorageService(config)
    inference_service = InferenceService(config["inference"])
    
    logger.info("Initializing MQTT consumer")
    consumer = MosquittoConsumer(
        host=config["mqtt"]["host"],
        port=config["mqtt"]["port"]
    )
    
    telemetry_consumer = TelemetryConsumer(
        consumer=consumer,
        storage_service=storage_service,
        inference_service=inference_service,
        topics=[f"{config['edge']['sensor_topic_prefix']}/#"]
    )
    
    try:
        await telemetry_consumer.start()
        logger.info("Telemetry consumer started successfully")
        
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.warning("Received shutdown signal")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    finally:
        logger.info("Disconnecting from MQTT broker")
        await consumer.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application shutdown complete") 