
import sys
import tempfile
import unittest

from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "function")
)

from storage import upload_archive

class TestStorage(unittest.TestCase):

    def test_upload_archive(self):
        """Проверяем параметры загрузки ZIP в Object Storage."""

        mock_client = MagicMock()

        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "test.zip"
            archive_path.write_bytes(b"Test archive")

            upload_archive(
                archive_path=archive_path,
                bucket_name="test-bucket",
                key="test.zip",
                s3_client=mock_client,
            )

            mock_client.upload_file.assert_called_once_with(
                str(archive_path),
                "test-bucket",
                "test.zip",
                ExtraArgs={"ContentType": "application/zip"},
            )

if __name__ == "__main__":
    unittest.main()
