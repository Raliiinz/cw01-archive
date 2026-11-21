
import io
import sys
import tempfile
import unittest
import uuid

from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile


# Подключаем модуль из папки function.
sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "function")
)

from archiver import create_archive, validate_task


class TestArchiver(unittest.TestCase):

    def test_create_archive(self):
        """Проверяем создание ZIP и корректность UUID v7."""

        file_content = b"Hello from archiver!"

        # Подменяем HTTP-запрос, чтобы тест не зависел от интернета.
        with patch("archiver.urlopen", return_value=io.BytesIO(file_content)):
            with tempfile.TemporaryDirectory() as directory:
                key, archive_path = create_archive(
                    name="document.txt",
                    url="https://example.com/document.txt",
                    output_dir=Path(directory),
                )

                # Проверяем формат ключа.
                self.assertTrue(key.endswith(".zip"))
                self.assertEqual(uuid.UUID(key[:-4]).version, 7)

                # Проверяем содержимое ZIP.
                with ZipFile(archive_path) as archive:
                    self.assertEqual(archive.namelist(), ["document.txt"])
                    self.assertEqual(
                        archive.read("document.txt"),
                        file_content,
                    )

    def test_invalid_name(self):
        """Путь к файлу не должен подменять его название."""

        with self.assertRaises(ValueError):
            validate_task("../secret.txt", "https://example.com/file")

    def test_invalid_url(self):
        """Запрещаем URL с неподдерживаемой схемой."""

        with self.assertRaises(ValueError):
            validate_task("file.txt", "file:///etc/passwd")


if __name__ == "__main__":
    unittest.main()
