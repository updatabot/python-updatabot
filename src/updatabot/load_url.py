import pandas as pd
import hashlib
import os
import time
import urllib.parse
import requests
from pathlib import Path
from dotenv import load_dotenv

UPDATABOT_USER_AGENT = 'updatabot/0.1 (https://github.com/updatabot/python-updatabot)'


def _get_cache_dir() -> Path:
    default_cache_dir = os.path.expanduser('~/.cache/updatabot')
    outpath = os.environ.get('UPDATABOT_CACHE_DIR', default_cache_dir)
    return Path(outpath)


def _get_url_filename(url: str) -> str:
    urlpath = urllib.parse.urlparse(url).path
    urlpath = urllib.parse.unquote(urlpath)
    return os.path.basename(urlpath)


def _get_cache_path(url: str) -> str:
    """Invent a URL-specific subdirectory in the cache folder
    """
    subdir = hashlib.sha256(url.encode()).hexdigest()
    return _get_cache_dir() / subdir / _get_url_filename(url)


def _is_cached(url: str, timeoutMins: int = 60) -> bool:
    local_path = _get_cache_path(url)
    if os.path.exists(local_path):
        ageMins = (time.time() - os.path.getmtime(local_path)) / 60
        if ageMins < timeoutMins:
            return True
        else:
            os.remove(local_path)
            os.rmdir(os.path.dirname(local_path))
            print(
                f"Removed cached file {local_path} because it was {ageMins} minutes old")
            return False
    return False


def _ensure_cached(url: str, no_cache: bool = False) -> str:
    """Get the local path to a cached file, downloading it if necessary.
    """
    if _is_cached(url) and not no_cache:
        print(f"Using cached file {_get_cache_path(url)}")
        return _get_cache_path(url)
    cache_path = _get_cache_path(url)
    # create the cache directory if it doesn't exist:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    # download the file:
    print(f"Downloading {url} to {cache_path}")
    response = requests.get(url, headers={'User-Agent': UPDATABOT_USER_AGENT})
    response.raise_for_status()
    cache_path.write_bytes(response.content)
    return cache_path


def load_url(url: str, sheet_name: str = '', no_cache: bool = False) -> pd.DataFrame:
    """Load data from a URL into a pandas DataFrame, with caching.

    Args:
        url (str): URL pointing to a CSV, Excel, or JSON file.
        no_cache (bool): If True, redownload the file every time.

    Returns:
        pd.DataFrame: Loaded data

    Raises:
        ValueError: If the data cannot be parsed as CSV, Excel, or JSON
    """
    load_dotenv()

    local_path = _ensure_cached(url)

    if local_path.suffix == '.csv':
        return pd.read_csv(local_path)
    elif local_path.suffix in ('.xlsx', '.xls'):
        excel_file = pd.ExcelFile(local_path)
        if sheet_name == '':
            excel_file = pd.ExcelFile(local_path)
            if len(excel_file.sheet_names) > 1:
                sheet_list = ", ".join(
                    f"'{name}'" for name in excel_file.sheet_names)
                raise ValueError(
                    f"Multiple sheets found in Excel file. Please specify one of: {sheet_list}"
                )
            return pd.read_excel(local_path)
        if not sheet_name in excel_file.sheet_names:
            raise ValueError(
                f"Sheet '{sheet_name}' not found in Excel file. Please specify one of: {excel_file.sheet_names}"
            )
        return pd.read_excel(local_path, sheet_name=sheet_name)
    elif local_path.suffix == '.json':
        return pd.read_json(local_path)
    # Try CSV first, then JSON if that fails
    try:
        return pd.read_csv(local_path)
    except:
        try:
            return pd.read_json(local_path)
        except:
            raise ValueError(
                f"Could not parse {url} as CSV or JSON data")
