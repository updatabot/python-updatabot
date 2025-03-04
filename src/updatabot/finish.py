import pandas as pd
import os


def finish(df: pd.DataFrame, meta: dict = None):
    """
    Called at the end of a datascript. The last block is always:
    # %% Finish
    helpers.finish(df, meta=meta)

    Args:
        df: The DataFrame to save
        meta: Optional metadata dictionary to save as JSON
    """
    output_dir = os.environ.get('UPDATABOT_ARTIFACTS_DIR', './artifacts')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the DataFrame
    filename = str(meta.get('filename', 'output.csv'))
    output_file = os.path.join(output_dir, filename)
    df.to_csv(output_file, index=False, header=True)

    # Save the metadata if provided
    if meta is not None:
        import json
        meta_file = os.path.join(output_dir, 'meta.json')
        with open(meta_file, 'w') as f:
            json.dump(meta, f, indent=2)
