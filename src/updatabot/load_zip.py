from dotenv import load_dotenv
from .logger import logger
from .load_url import _ensure_cached, _load_local_path
from pathlib import Path
import pandas as pd
import zipfile


class LocalZipFile:
    def __init__(self, zip_ref: zipfile.ZipFile, unzip_to: Path):
        self.zip_ref = zip_ref
        self.unzip_to = unzip_to

    def contents(self) -> list[str]:
        """Returns a list of all files in the ZIP directory, including those in subdirectories.
        Paths are returned relative to the ZIP root."""
        return self.zip_ref.namelist()

    def load(self, path: str, file_extension: str = '', sheet_name: str = '') -> pd.DataFrame:
        """Load a file from inside the ZIP file.
        Parameters operate the same as load_url().
        """
        # Extract single file to a temporary path
        temp_path = self.unzip_to / path
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        self.zip_ref.extract(path, self.unzip_to)
        return _load_local_path(temp_path, file_extension=file_extension, sheet_name=sheet_name)


def load_zip(url: str, no_cache: bool = False) -> LocalZipFile:
    """Load a ZIP file from a URL, with caching. Returns a
    LocalZipFile to extract dataframes from the content.

    Usage:
        updatabot.load_zip('https://...zip').load('path/to/file.csv')

    Args:
        url (str): URL pointing to a ZIP file.
        no_cache (bool): If True, redownload the file every time.

    Returns:
        LocalZipFile: Loads dataframes from the zip file.
    """
    load_dotenv()
    logger.debug(f"Loading ZIP file: {url}")
    local_path = _ensure_cached(url, no_cache)

    unzip_to = local_path.parent / 'unzipped'
    zip_ref = zipfile.ZipFile(local_path, 'r')
    return LocalZipFile(zip_ref, unzip_to)
