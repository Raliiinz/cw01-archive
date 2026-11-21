
import os
import sys
import unittest

from pathlib import Path
from unittest.mock import ANY, patch


sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "function")
)

from handler import handler


class TestHandler(unittest.TestCase):

    def setUp(self):
        """Подготавливаем сообщение, которое отправляет YMQ."""

        self.event = {
            "messages": [
                {
                    "details": {
                        "message": {
                            "body": (
                                '{"name": "document.pdf", '
                                '"url": "https://example.com/document.pdf"}'
                            )
                        }
                    }
                }
            ]
        }

    @patch.dict(
        os.environ,
        {
            "BUCKET_NAME": "test-bucket",
            "YDB_DOCUMENT_ENDPOINT": "https://example.com/ydb",
        },
    )
    @patch("handler.save_archive_metadata")
    @patch("handler.upload_archive")
    @patch("handler.create_archive")
    def test_success(
        self,
        mock_create,
        mock_upload,
        mock_save,
    ):
        """Проверяем успешное выполнение всех этапов."""

        key = "test-archive.zip"
        archive_path = Path("/tmp/test-archive.zip")

        mock_create.return_value = (key, archive_path)

        result = handler(self.event, None)

        self.assertEqual(
            result,
            {"status": "success", "key": key},
        )

        mock_create.assert_called_once_with(
            name="document.pdf",
            url="https://example.com/document.pdf",
            output_dir=ANY,
        )

        mock_upload.assert_called_once_with(
            archive_path=archive_path,
            bucket_name="test-bucket",
            key=key,
        )

        mock_save.assert_called_once_with(
            name="document.pdf",
            url="https://example.com/document.pdf",
            key=key,
            endpoint="https://example.com/ydb",
        )

    def test_invalid_message(self):
        """Некорректное сообщение вызывает исключение."""

        with self.assertRaises(ValueError):
            handler({"messages": []}, None)

    @patch.dict(
        os.environ,
        {
            "BUCKET_NAME": "test-bucket",
            "YDB_DOCUMENT_ENDPOINT": "https://example.com/ydb",
        },
    )
    @patch("handler.save_archive_metadata")
    @patch("handler.upload_archive")
    @patch("handler.create_archive")
    def test_upload_error(
        self,
        mock_create,
        mock_upload,
        mock_save,
    ):
        """Ошибка загрузки должна прерывать обработку."""

        mock_create.return_value = (
            "test-archive.zip",
            Path("/tmp/test-archive.zip"),
        )
        mock_upload.side_effect = RuntimeError("Upload failed")

        with self.assertRaises(RuntimeError):
            handler(self.event, None)

        # Если ZIP не загрузился, в YDB ничего не записываем.
        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
