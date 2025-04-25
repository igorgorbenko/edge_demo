import os
from typing import Dict, Any
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

MQTT_CONFIG = {
    "host": os.getenv("MQTT_HOST", "localhost"),
    "port": int(os.getenv("MQTT_PORT", 1883)),
    "username": os.getenv("MQTT_USERNAME"),
    "password": os.getenv("MQTT_PASSWORD"),
}

AWS_CONFIG = {
    "region": os.getenv("AWS_REGION", "us-east-1"),
    "credentials": {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    },
    "s3": {
        "bucket_name": os.getenv("S3_BUCKET_NAME", "telemetry-data"),
        "base_path": os.getenv("PARQUET_BASE_PATH", "telemetry"),
        "buffer_size": int(os.getenv("TELEMETRY_BUFFER_SIZE", 100)),
    }
}

EDGE_CONFIG = {
    "device_id": os.getenv("DEVICE_ID", "edge-device-001"),
    "sensor_topic_prefix": os.getenv("SENSOR_TOPIC_PREFIX", "telemetry"),
    "control_topic_prefix": os.getenv("CONTROL_TOPIC_PREFIX", "control"),
}

INFERENCE_CONFIG = {
    "sensor1": {"threshold": 100},
    "sensor2": {"threshold": 50},
    # Добавьте другие сенсоры и их конфигурации
}

def get_config() -> Dict[str, Any]:
    return {
        "mqtt": MQTT_CONFIG,
        "aws": AWS_CONFIG,
        "edge": EDGE_CONFIG,
        "inference": INFERENCE_CONFIG,
    } 