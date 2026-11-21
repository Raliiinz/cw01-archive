
import os
import sys

import boto3
from botocore.exceptions import ClientError


TABLE_NAME = "archives"


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
    )

    try:
        if action == "create":
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

            client.get_waiter("table_exists").wait(
                TableName=TABLE_NAME,
                WaiterConfig={"Delay": 3, "MaxAttempts": 50},
            )
            print("Document table archives created")

        else:
            client.delete_table(TableName=TABLE_NAME)

            client.get_waiter("table_not_exists").wait(
                TableName=TABLE_NAME,
                WaiterConfig={"Delay": 3, "MaxAttempts": 50},
            )
            print("Document table archives deleted")

    except ClientError as error:
        code = error.response["Error"]["Code"]

        # Повторное создание или удаление не считается ошибкой.
        if action == "create" and code == "ResourceInUseException":
            print("Document table already exists")
        elif action == "delete" and code == "ResourceNotFoundException":
            print("Document table already deleted")
        else:
            raise


if __name__ == "__main__":
    main()
