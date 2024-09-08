from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from loguru import logger


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def put_file(
            self,
            file_name: str,
            data: bytes
    ):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_name,
                    Body=data,
                )
                logger.debug(
                    f"File {file_name} uploaded to {self.bucket_name} ({len(data) / 1024**2:.4} MB)")
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")

    async def delete_file(self, file_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=file_name)
                logger.info(
                    f"File {file_name} deleted from {self.bucket_name}")
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")

    async def get_file(self, file_name: str) -> bytes:
        try:
            async with self.get_client() as client:
                response: dict = await client.get_object(Bucket=self.bucket_name, Key=file_name)
                logger.info(
                    f"File {file_name} downloaded from {self.bucket_name}")
                return await response.get("Body").read()
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            return bytes(0)
