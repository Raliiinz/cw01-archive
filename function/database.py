
import boto3


TABLE_NAME = "archives"
REGION = "ru-central1"


def save_archive_metadata(
    name: str,
    url: str,
    key: str,
    endpoint: str | None = None,
    dynamodb_resource=None,
) -> None:
    """Сохраняет информацию об архиве в документной таблице YDB."""

    if not all(isinstance(value, str) and value for value in (name, url, key)):
        raise ValueError("Поля name, url и key должны быть непустыми строками")

    if dynamodb_resource is None:
        if not endpoint:
            raise ValueError("Не указан Document API endpoint базы данных")

        dynamodb_resource = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint,
            region_name=REGION,
        )

    table = dynamodb_resource.Table(TABLE_NAME)

    table.put_item(
        Item={
            "key": key,
            "name": name,
            "url": url,
        }
    )
