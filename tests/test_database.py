
import sys
import unittest

from pathlib import Path
from unittest.mock import MagicMock


sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "function")
)

from database import save_archive_metadata


class TestDatabase(unittest.TestCase):

    def test_save_archive_metadata(self):
        """Проверяем сохранение правильных полей в YDB."""

        # Подменяем реальную базу данных имитацией.
        mock_resource = MagicMock()

        save_archive_metadata(
            name="document.pdf",
            url="https://example.com/document.pdf",
            key="test-archive.zip",
            dynamodb_resource=mock_resource,
        )

        # Проверяем выбор нужной таблицы.
        mock_resource.Table.assert_called_once_with("archives")

        # Проверяем содержимое записи.
        mock_table = mock_resource.Table.return_value

        mock_table.put_item.assert_called_once_with(
            Item={
                "key": "test-archive.zip",
                "name": "document.pdf",
                "url": "https://example.com/document.pdf",
            }
        )

    def test_missing_endpoint(self):
        """Без адреса базы и тестового клиента запись невозможна."""

        with self.assertRaises(ValueError):
            save_archive_metadata(
                name="document.pdf",
                url="https://example.com/document.pdf",
                key="test-archive.zip",
            )


if __name__ == "__main__":
    unittest.main()
