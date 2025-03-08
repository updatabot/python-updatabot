import pandas as pd
import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save(df: pd.DataFrame, name: str = "output", meta: dict = None) -> str:
    """
    Save a DataFrame as a CSV artifact with optional metadata.

    Args:
        df: DataFrame to save
        name: Base name for the file (without extension)
        meta: Optional metadata dictionary

    Returns:
        Path to the saved file
    """
    # Setup
    output_dir = os.environ.get('UPDATABOT_ARTIFACTS_DIR', './artifacts')
    logger.debug(f"Using artifacts directory: {output_dir}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Ensure name has no extension
    base_name = os.path.splitext(name)[0]
    logger.debug(f"Using base name: {base_name}")

    # Save DataFrame
    csv_path = os.path.join(output_dir, f"{base_name}.csv")
    logger.debug(f"Saving DataFrame with shape {df.shape} to {csv_path}")
    df.to_csv(csv_path, index=False)

    # Save metadata if provided
    if meta:
        meta_path = os.path.join(output_dir, f"{base_name}.json")
        logger.debug(f"Saving metadata to {meta_path}")
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)

    logger.info(f"Successfully saved DataFrame to {csv_path}")
    return csv_path
