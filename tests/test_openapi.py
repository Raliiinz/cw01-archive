
import re
import unittest
from pathlib import Path

import yaml
from openapi_spec_validator import validate


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "openapi.yaml"


class TestOpenAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Загружаем спецификацию для всех тестов."""
        cls.source = SPEC_PATH.read_text(encoding="utf-8")
        cls.spec = yaml.safe_load(cls.source)

    def test_openapi_specification(self):
        """Проверяем соответствие стандарту OpenAPI."""
        validate(self.spec)

    def test_routes_and_integrations(self):
        """Проверяем маршруты и облачные интеграции."""
        expected = [
            ("/tasks", "post", "cloud_ymq", "SendMessage"),
            ("/archives", "get", "cloud_ydb", "Scan"),
            ("/archives/{key}", "get", "cloud_ydb", "GetItem"),
            ("/download/{key}", "get", "object_storage", None),
        ]

        for path, method, integration_type, action in expected:
            with self.subTest(path=path, method=method):
                integration = self.spec["paths"][path][method][
                    "x-yc-apigateway-integration"
                ]

                self.assertEqual(integration["type"], integration_type)

                if action is not None:
                    self.assertEqual(integration["action"], action)

    def test_task_validation(self):
        """Проверяем обязательные поля задания."""
        task = self.spec["components"]["schemas"]["Task"]

        self.assertEqual(set(task["required"]), {"name", "url"})
        self.assertFalse(task["additionalProperties"])

        validator = self.spec["paths"]["/tasks"]["post"][
            "x-yc-apigateway-validator"
        ]
        self.assertTrue(validator["validateRequestBody"])

    def test_terraform_placeholders(self):
        """Проверяем отсутствие жёстко заданных ID ресурсов."""
        placeholders = set(
            re.findall(r"\$\{([a-z_]+)\}", self.source)
        )

        self.assertEqual(
            placeholders,
            {
                "queue_url",
                "folder_id",
                "service_account_id",
                "database_path",
                "bucket_name",
            },
        )


if __name__ == "__main__":
    unittest.main()
