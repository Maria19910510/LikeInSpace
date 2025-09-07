import json
from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_load_transactions_success():
    mock_data = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200}
    ]
    m = mock_open(read_data=json.dumps(mock_data))
    with patch("builtins.open", m):
        result = load_transactions("fake_path.json")
        assert result == mock_data
        m.assert_called_once_with("fake_path.json", "r", encoding="utf-8")


def test_load_transactions_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions("nonexistent.json")
        assert result == []


def test_load_transactions_json_decode_error():
    # Передаем некорректный JSON, чтобы вызвать json.JSONDecodeError
    m = mock_open(read_data="{ invalid json }")
    with patch("builtins.open", m):
        # На случай, если функция вызовет json.loads, она выбросит исключение
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            result = load_transactions("bad_json.json")
            assert result == []


def test_load_transactions_data_not_list():
    # Передать JSON, который не является списком
    m = mock_open(read_data=json.dumps({"not": "a list"}))
    with patch("builtins.open", m):
        result = load_transactions("dict_instead_list.json")
        assert result == []
