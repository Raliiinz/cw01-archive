
import json
import logging
import os
import tempfile

from pathlib import Path

from archiver import create_archive, validate_task
from database import save_archive_metadata
from storage import upload_archive


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    """Обрабатывает задание из Yandex Message Queue."""

    messages = event.get("messages")

    if not isinstance(messages, list) or len(messages) != 1:
        raise ValueError("Ожидалось одно сообщение из очереди")

    message = messages[0]["details"]["message"]
    task = json.loads(message["body"])

    if not isinstance(task, dict):
        raise ValueError("Задание должно быть JSON-объектом")

    name = task.get("name")
    url = task.get("url")

    validate_task(name, url)

    bucket_name = os.environ["BUCKET_NAME"]
    ydb_endpoint = os.environ["YDB_DOCUMENT_ENDPOINT"]

    logger.info("Начинаем архивирование файла: %s", name)

    with tempfile.TemporaryDirectory() as directory:
        key, archive_path = create_archive(
            name=name,
            url=url,
            output_dir=Path(directory),
        )

        upload_archive(
            archive_path=archive_path,
            bucket_name=bucket_name,
            key=key,
        )

        save_archive_metadata(
            name=name,
            url=url,
            key=key,
            endpoint=ydb_endpoint,
        )

    logger.info("Архив успешно создан: %s", key)

    return {"status": "success", "key": key}
