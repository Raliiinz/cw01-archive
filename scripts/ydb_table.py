
import os
import sys
import time

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


TABLE_NAME = "archives"

# YDB Document API может быть недоступен сразу после создания базы.
MAX_CREATE_ATTEMPTS = 30
RETRY_DELAY_SECONDS = 10

# Повторяем только ошибки, указывающие на временную недоступность.
RETRYABLE_ERRORS = {
    "ServiceUnavailable",
    "ServiceUnavailableException",
}


def create_table(client):
    """Создаёт таблицу после готовности YDB Document API."""

    for attempt in range(1, MAX_CREATE_ATTEMPTS + 1):
        try:
            client.create_table(
                TableName=TABLE_NAME,
                AttributeDefinitions=[
                    {"AttributeName": "key", "AttributeType": "S"}
                ],
                KeySchema=[
                    {"AttributeName": "key", "KeyType": "HASH"}
                ],
                BillingMode="PAY_PER_REQUEST",
            )

            print("Document table creation requested")
            break

        except ClientError as error:
            code = error.response["Error"]["Code"]

            # Таблица могла быть создана при предыдущей попытке.
            if code == "ResourceInUseException":
                print("Document table already exists")
                break

            # Ошибки доступа и конфигурации не скрываем.
            if code not in RETRYABLE_ERRORS:
                raise

            # После последней попытки возвращаем настоящую ошибку.
            if attempt == MAX_CREATE_ATTEMPTS:
                raise

            print(
                f"YDB is not ready ({code}). "
                f"Attempt {attempt}/{MAX_CREATE_ATTEMPTS}. "
                f"Retrying..."
            )
            time.sleep(RETRY_DELAY_SECONDS)

    # Ожидаем появления таблицы и при первом создании,
    # и при повторном запуске после частичной ошибки.
    client.get_waiter("table_exists").wait(
        TableName=TABLE_NAME,
        WaiterConfig={"Delay": 3, "MaxAttempts": 50},
    )

    print("Document table archives is ready")


def delete_table(client):
    """Удаляет документную таблицу, если она существует."""

    try:
        client.delete_table(TableName=TABLE_NAME)
    except ClientError as error:
        code = error.response["Error"]["Code"]

        if code == "ResourceNotFoundException":
            print("Document table already deleted")
            return

        raise

    client.get_waiter("table_not_exists").wait(
        TableName=TABLE_NAME,
        WaiterConfig={"Delay": 3, "MaxAttempts": 50},
    )

    print("Document table archives deleted")


def main():
    """Создаёт или удаляет документную таблицу YDB."""

    if len(sys.argv) != 2 or sys.argv[1] not in ("create", "delete"):
        raise ValueError("Использование: ydb_table.py create|delete")

    action = sys.argv[1]

    # Endpoint и ключи предоставляет Terraform через окружение.
    client = boto3.client(
        "dynamodb",
        endpoint_url=os.environ["YDB_DOCUMENT_ENDPOINT"],
        region_name="ru-central1",
        config=Config(
            retries={
                "mode": "standard",
                "total_max_attempts": 2,
            },
        ),
    )

    if action == "create":
        create_table(client)
    else:
        delete_table(client)


if __name__ == "__main__":
    main()
