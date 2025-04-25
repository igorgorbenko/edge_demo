import os
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import boto3
from typing import Dict, Any


class StorageService:
    def __init__(self, config: Dict[str, Any]):
        self.bucket_name = config["aws"]["s3"]["bucket_name"]
        self.base_path = config["aws"]["s3"]["base_path"]
        self.buffer_size = config["aws"]["s3"]["buffer_size"]
        
        # Инициализируем S3 клиент с credentials
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config["aws"]["credentials"]["aws_access_key_id"],
            aws_secret_access_key=config["aws"]["credentials"]["aws_secret_access_key"],
            region_name=config["aws"]["region"]
        )
        self.buffer = []

    def _get_partition_path(self, timestamp: datetime) -> str:
        return f"{self.base_path}/year={timestamp.year}/month={timestamp.month}/day={timestamp.day}"

    async def store(self, message: Dict[str, Any]) -> None:
        self.buffer.append(message)
        
        if len(self.buffer) >= self.buffer_size:
            await self.flush()

    async def flush(self) -> None:
        if not self.buffer:
            return

        # Конвертируем данные в DataFrame и затем в Parquet
        table = pa.Table.from_pylist(self.buffer)
        
        # Создаем временный файл
        timestamp = datetime.utcnow()
        partition_path = self._get_partition_path(timestamp)
        file_name = f"telemetry_{timestamp.timestamp()}.parquet"
        local_path = f"/tmp/{file_name}"

        # Сохраняем во временный файл
        pq.write_table(table, local_path)

        # Загружаем в S3
        s3_path = f"{partition_path}/{file_name}"
        self.s3_client.upload_file(local_path, self.bucket_name, s3_path)

        # Очищаем буфер и удаляем временный файл
        self.buffer = []
        os.remove(local_path) 