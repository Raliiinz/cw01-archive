
from pathlib import Path

import boto3

S3_ENDPOINT = "https://storage.yandexcloud.net"

def upload_archive(
    archive_path: Path,
    bucket_name: str,
    key: str,
    s3_client=None,
) -> None:
    """Загружает ZIP-архив в Yandex Object Storage."""

    archive_path = Path(archive_path)

    if not archive_path.is_file():
        raise FileNotFoundError(f"Архив не найден: {archive_path}")

    if not bucket_name:
        raise ValueError("Не указано имя бакета")

    if s3_client is None:
        s3_client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            region_name="ru-central1",
        )

    s3_client.upload_file(
        str(archive_path),
        bucket_name,
        key,
        ExtraArgs={"ContentType": "application/zip"},
    )
