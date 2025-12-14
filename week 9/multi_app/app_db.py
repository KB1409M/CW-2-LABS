
import pandas as pd
from pathlib import Path

# Define the base data folder relative to project root
BASE_PATH = Path(__file__).parent.parent.parent / "week 8" / "DATA"

def get_table_from_csv(filename):
    file_path = BASE_PATH / f"{filename}.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    return pd.read_csv(file_path)




