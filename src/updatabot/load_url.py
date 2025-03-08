import pandas as pd
import hashlib
import os
import time
import urllib.parse
import requests
from pathlib import Path
from dotenv import load_dotenv
from .logger import logger

UPDATABOT_USER_AGENT = 'updatabot/0.1 (https://github.com/updatabot/python-updatabot)'


def _get_cache_dir() -> Path:
    default_cache_dir = os.path.expanduser('~/.cache/updatabot')
    outpath = os.environ.get('UPDATABOT_CACHE_DIR', default_cache_dir)
    return Path(outpath)


def _get_url_filename(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    # Special handling for ONS downloads
    if parsed.hostname == 'www.ons.gov.uk' and parsed.path == '/file' and 'uri' in query:
        querystring = urllib.parse.urlencode(query)
        logger.debug(f"ONS download detected: {querystring}")
        uripath = query['uri'][0]
    else:
        uripath = parsed.path
    # Decode the path
    uripath = urllib.parse.unquote(uripath)
    # Get the filename
    return os.path.basename(uripath)


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
            logger.debug(f"Cache hit for {url} at {local_path}")
            return True
        else:
            os.remove(local_path)
            os.rmdir(os.path.dirname(local_path))
            logger.info(
                f"Removed cached file {local_path} because it was {ageMins:.1f} minutes old")
            return False
    logger.debug(f"Cache miss for {url}")
    return False


def _ensure_cached(url: str, no_cache: bool = False) -> str:
    """Ensure that a URL is cached locally.

    Args:
        url (str): URL to cache
        no_cache (bool): If True, redownload the file every time.

    Returns:
        str: Local path to the cached file
    """
    if _is_cached(url) and not no_cache:
        logger.debug(f"Using cached file {_get_cache_path(url)}")
        return _get_cache_path(url)
    cache_path = _get_cache_path(url)
    # create the cache directory if it doesn't exist:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    # download the file:
    logger.info(f"Downloading {url} to {cache_path}")
    response = requests.get(url, headers={'User-Agent': UPDATABOT_USER_AGENT})
    response.raise_for_status()
    cache_path.write_bytes(response.content)
    return cache_path


def _load_as_excel(local_path: Path, sheet_name: str = '') -> pd.DataFrame:
    """Load an Excel file into a pandas DataFrame.

    Args:
        local_path (Path): Local path to the Excel file
        sheet_name (str): Name of the sheet to load, or the sole sheet if empty.
        If the sheet is not found, or if there are multiple sheets, an error is raised.

    Returns:
        pd.DataFrame: Loaded data
    Raises:
        ValueError: If the sheet is not found, or if there are multiple sheets.
        Error: If the file is not an Excel file.
    """
    excel_file = pd.ExcelFile(local_path)
    if sheet_name == '':
        if len(excel_file.sheet_names) > 1:
            sheet_list = ", ".join(
                f"'{name}'" for name in excel_file.sheet_names)
            raise ValueError(
                f"Multiple sheets found in Excel file. Please specify one of: {sheet_list}"
            )
        logger.debug(f"Loading single sheet from {local_path}")
        return pd.read_excel(local_path)
    if not sheet_name in excel_file.sheet_names:
        raise ValueError(
            f"Sheet '{sheet_name}' not found in Excel file. Please specify one of: {excel_file.sheet_names}"
        )
    logger.debug(f"Loading sheet '{sheet_name}' from {local_path}")
    return pd.read_excel(local_path, sheet_name=sheet_name)


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
    logger.debug(
        f"Loading URL: {url} (sheet_name='{sheet_name}', no_cache={no_cache})")

    local_path = _ensure_cached(url, no_cache)

    if local_path.suffix == '.csv':
        logger.debug(f"Loading as CSV: {local_path}")
        return pd.read_csv(local_path)
    elif local_path.suffix in ('.xlsx', '.xls'):
        logger.debug(f"Loading as Excel: {local_path}")
        return _load_as_excel(local_path, sheet_name)
    elif local_path.suffix == '.json':
        logger.debug(f"Loading as JSON: {local_path}")
        return pd.read_json(local_path)

    # Try different formats if extension doesn't match content
    logger.warning(
        f"No recognized file extension for {url}, attempting to detect format")
    try:
        logger.debug("Attempting CSV format")
        return pd.read_csv(local_path)
    except Exception as e:
        logger.debug(f"CSV parsing failed: {str(e)}")

    try:
        logger.debug("Attempting JSON format")
        return pd.read_json(local_path)
    except Exception as e:
        logger.debug(f"JSON parsing failed: {str(e)}")

    try:
        logger.debug("Attempting Excel format")
        return _load_as_excel(local_path, sheet_name)
    except Exception as e:
        logger.debug(f"Excel parsing failed: {str(e)}")

    logger.error(f"Failed to parse {url} in any supported format")
    raise ValueError(f"Could not parse {url} as CSV, XLSX or JSON data")
