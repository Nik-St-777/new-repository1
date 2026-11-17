"""Загрузка финансовых транзакций из CSV и Excel-файлов."""

import csv
from typing import Any, Dict, List

import pandas as pd


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из CSV-файла и возвращает список словарей."""
    with open(file_path, encoding="utf-8") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel  # разделитель по умолчанию — запятая
        reader = csv.DictReader(f, dialect=dialect)
        return list(reader)


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из Excel-файла и возвращает список словарей."""
    df = pd.read_excel(file_path)
    return df.to_dict(orient="records")
