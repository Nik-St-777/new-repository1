"""Тесты загрузки финансовых транзакций из CSV и Excel-файлов."""

import csv
from unittest.mock import patch

import pandas as pd
import pytest

from src.finance_loader import load_transactions_from_csv, load_transactions_from_excel


class TestLoadTransactionsFromCsv:
    def test_returns_list_of_dicts(self, tmp_path):
        """Успешное чтение CSV с запятой в качестве разделителя."""
        file = tmp_path / "transactions.csv"
        file.write_text(
            "date,amount,category\n2024-01-01,100,food\n2024-01-02,200,transport",
            encoding="utf-8",
        )

        result = load_transactions_from_csv(str(file))

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(row, dict) for row in result)
        assert result[0] == {"date": "2024-01-01", "amount": "100", "category": "food"}
        assert result[1]["amount"] == "200"

    def test_semicolon_delimiter(self, tmp_path):
        """CSV с разделителем «точка с запятой» тоже разбирается корректно."""
        file = tmp_path / "data.csv"
        file.write_text(
            "id;state;amount\n1;EXECUTED;100\n2;CANCELED;200",
            encoding="utf-8",
        )

        result = load_transactions_from_csv(str(file))

        assert len(result) == 2
        assert result[0]["state"] == "EXECUTED"
        assert result[1]["id"] == "2"

    def test_returns_empty_list_for_empty_file(self, tmp_path):
        """Пустой CSV-файл возвращает пустой список, а не падает."""
        file = tmp_path / "empty.csv"
        file.write_text("", encoding="utf-8")

        result = load_transactions_from_csv(str(file))

        assert result == []

    def test_raises_file_not_found(self):
        """Отсутствующий файл вызывает FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_transactions_from_csv("nonexistent.csv")


class TestLoadTransactionsFromExcel:
    @patch("pandas.read_excel")
    def test_returns_list_of_dicts(self, mock_read_excel):
        """Успешное чтение Excel через замоканный read_excel."""
        mock_df = pd.DataFrame(
            [
                {"date": "2024-01-01", "amount": "100", "category": "food"},
                {"date": "2024-01-02", "amount": "200", "category": "transport"},
            ]
        )
        mock_read_excel.return_value = mock_df

        result = load_transactions_from_excel("dummy.xlsx")

        mock_read_excel.assert_called_once_with("dummy.xlsx")
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(row, dict) for row in result)
        assert result[0]["category"] == "food"

    @patch("pandas.read_excel", side_effect=FileNotFoundError)
    def test_raises_file_not_found(self, _):
        """Ошибка отсутствующего файла прокидывается наружу."""
        with pytest.raises(FileNotFoundError):
            load_transactions_from_excel("nonexistent.xlsx")
