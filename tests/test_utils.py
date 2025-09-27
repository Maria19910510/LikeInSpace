import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions


@pytest.fixture
def mock_logger():
    with patch('src.utils.logger') as mock_log:
        yield mock_log


def test_load_transactions_success(mock_logger):
    data = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200}
    ]
    m = mock_open(read_data=json.dumps(data))
    with patch('builtins.open', m):
        result = load_transactions('fake_path.json')
        assert result == data
        m.assert_called_once_with('fake_path.json', 'r', encoding='utf-8')
        mock_logger.info.assert_called_with('Загружено 2 транзакций из fake_path.json')


def test_load_transactions_file_not_found(mock_logger):
    with patch('builtins.open', side_effect=FileNotFoundError):
        result = load_transactions('bad_path.json')
        assert result == []
        mock_logger.error.assert_called()
        args, _ = mock_logger.error.call_args
        assert 'Ошибка при загрузке файла' in args[0]


def test_load_transactions_json_decode_error(mock_logger):
    with patch('builtins.open', mock_open(read_data='{ invalid json }')):
        with patch('json.load', side_effect=json.JSONDecodeError('error', '', 0)):
            result = load_transactions('bad_json.json')
            assert result == []
            mock_logger.error.assert_called()


def test_load_transactions_data_not_list(mock_logger):
    with patch('builtins.open', mock_open(read_data=json.dumps({"not": "list"}))):
        with patch('json.load', return_value={"not": "list"}):
            result = load_transactions('not_list.json')
            assert result == []
            mock_logger.warning.assert_called_with('Некорректные данные в not_list.json')
