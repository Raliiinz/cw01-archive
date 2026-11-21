
import shutil
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from zipfile import ZIP_DEFLATED, ZipFile

from uuid6 import uuid7

def validate_task(name: str, url: str) -> None:
    """Проверяет корректность задания на архивирование."""

    if not isinstance(name, str) or not name:
        raise ValueError("Название файла не должно быть пустым")

    if name in (".", "..") or "/" in name or "\\" in name:
        raise ValueError("Недопустимое название файла")

    if not isinstance(url, str):
        raise ValueError("URL должен быть строкой")

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
        raise ValueError("Некорректный URL файла")

def create_archive(name: str, url: str, output_dir: Path) -> tuple[str, Path]:
    """Скачивает файл по URL и сохраняет его в ZIP-архив.

    Возвращает ключ архива и путь к созданному ZIP-файлу.
    """

    validate_task(name, url)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    key = f"{uuid7()}.zip"
    archive_path = output_dir / key

    try:
        request = Request(url, headers={"User-Agent": "cw01-archiver/1.0"})

        # Скачиваем данные потоком, а не загружаем весь файл в память.
        with urlopen(request, timeout=30) as response:
            with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as zip_file:
                with zip_file.open(name, "w") as destination:
                    shutil.copyfileobj(response, destination, length=64 * 1024)

    except Exception:
        # Не оставляем повреждённый ZIP, если скачивание завершилось ошибкой.
        archive_path.unlink(missing_ok=True)
        raise

    return key, archive_path
