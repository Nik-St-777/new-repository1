import csv
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(path)
    return df.to_dict(orient="records")




