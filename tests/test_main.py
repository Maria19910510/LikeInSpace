import pytest
from unittest.mock import patch
import src.main as main
import io


@pytest.fixture
def patch_input_and_files():
    inputs = iter([
        "1",
        "test.json"
    ])


def test_main_flow(patch_input_and_files, capsys):
    main.main()
    captured = capsys.readouterr()
    assert "транзакций" in captured.out


def test_get_transactions_from_json():
    fake_json_content = ('[{"date": "01.01.2022", "description": '
                         '"Покупка", "amount": "5000 руб.", "status": "EXECUTED"}]')
    with patch("builtins.open", return_value=io.BytesIO(fake_json_content.encode('utf-8'))):
        result = main.get_transactions_from_json("dummy_path.json")
        assert isinstance(result, list)
        assert result[0]["description"] == "Покупка"
