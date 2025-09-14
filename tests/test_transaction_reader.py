from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from src.transaction_reader import read_transactions_from_csv, read_transactions_from_xlsx

# Тесты для функции read_transactions_from_csv
@patch("builtins.open", new_callable=mock_open, read_data="date,amount,description\n2023-01-01,100,Sample Transaction")
@patch("csv.DictReader")
def test_read_transactions_from_csv(mock_csv_reader, mock_open_):
    # Создаем мок CSV DictReader
    mock_csv_instance = MagicMock()
    mock_csv_instance.__iter__.return_value = [
        {"date": "2023-01-01", "amount": "100", "description": "Sample Transaction"}
    ]
    mock_csv_reader.return_value = mock_csv_instance

    result = read_transactions_from_csv("dummy_path.csv")
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["date"] == "2023-01-01"
    assert result[0]["amount"] == "100"
    assert result[0]["description"] == "Sample Transaction"
    mock_open_.assert_called_once_with("dummy_path.csv", newline='', encoding='utf-8')
    mock_csv_reader.assert_called_once()


# Тест для функции чтения из Excel
@patch("pandas.read_excel")
def test_read_transactions_from_xlsx(mock_read_excel):
    mock_df = pd.DataFrame([
        {"date": "2023-01-01", "amount": 200, "description": "Excel Transaction"}
    ])
    mock_read_excel.return_value = mock_df

    result = read_transactions_from_xlsx("dummy_path.xlsx")
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["date"] == "2023-01-01"
    assert result[0]["amount"] == 200
    assert result[0]["description"] == "Excel Transaction"
    mock_read_excel.assert_called_once_with("dummy_path.xlsx")
