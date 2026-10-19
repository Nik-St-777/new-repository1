from unittest.mock import mock_open, patch

import pytest
from src.finance_loader import load_transactions_from_csv, load_transactions_from_excel


class TestLoadTransactionsFromCsv:
    def test_returns_list_of_dicts(self):
        csv_data = "date,amount,category\n2024-01-01,100,food\n2024-01-02,200,transport"
        m = mock_open(read_data=csv_data)

        with patch("builtins.open", m):
            result = load_transactions_from_csv("dummy.csv")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(row, dict) for row in result)
        assert result[0]["amount"] == "100"

    def test_raises_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_transactions_from_csv("nonexistent.csv")


class TestLoadTransactionsFromExcel:
    @patch("pandas.read_excel")
    def test_returns_list_of_dicts(self, mock_read_excel):
        import pandas as pd
        mock_df = pd.DataFrame(
            [
                {"date": "2024-01-01", "amount": "100", "category": "food"},
                {"date": "2024-01-02", "amount": "200", "category": "transport"},
            ]
        )
        mock_read_excel.return_value = mock_df

        result = load_transactions_from_excel("dummy.xlsx")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(row, dict) for row in result)

    @patch("pandas.read_excel", side_effect=FileNotFoundError)
    def test_raises_file_not_found(self, _):
        with pytest.raises(FileNotFoundError):
            load_transactions_from_excel("nonexistent.xlsx")
