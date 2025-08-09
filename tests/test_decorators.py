import pytest

from src.decorators import log


def successful_func(x):
    return x + 10


def error_func():
    raise RuntimeError("Некорректное выполнение функции")


# Тест для логирования в консоль при успешном вызове
def test_log_console_success(capsys):
    decorated = log()(successful_func)
    result = decorated(5)
    captured = capsys.readouterr()
    assert result == 15
    # Проверка, что сообщение для начала выполнения есть в выводе
    assert "successful_func started." in captured.out
    # Проверка, что сообщение о завершении успеха есть в выводе
    assert "successful_func ok" in captured.out


# Тест для логирования в консоль при возникновении исключения
def test_log_console_error(capsys):
    decorated = log()(error_func)
    with pytest.raises(RuntimeError):
        decorated()
    captured = capsys.readouterr()
    # Проверка, что сообщения о начале и ошибке есть в выводе
    assert "error_func started." in captured.out
    assert "error_func error:" in captured.out
    assert "RuntimeError" in captured.out
    assert "Traceback (most recent call last):" in captured.out


# Тест для логирования в файл при успешном вызове
def test_log_file_success(tmp_path):
    log_file = tmp_path / "logfile.txt"
    decorated = log(str(log_file))(successful_func)
    result = decorated(7)
    assert result == 17
    log_contents = log_file.read_text()
    assert "successful_func started." in log_contents
    assert "successful_func ok" in log_contents


# Тест для логирования в файл при ошибке
def test_log_file_error(tmp_path):
    log_file = tmp_path / "logfile.txt"
    decorated = log(str(log_file))(error_func)
    with pytest.raises(RuntimeError):
        decorated()
    log_contents = log_file.read_text()
    assert "error_func started." in log_contents
    assert "error_func error:" in log_contents
    assert "RuntimeError" in log_contents


# Дополнительный тест: несколько вызовов с разными результатами
def test_multiple_calls_with_mixed_results(tmp_path):
    log_file = tmp_path / "multi_log.txt"
    decorated_success = log(str(log_file))(successful_func)

    # Первый вызов успешно
    assert decorated_success(1) == 11
    # Второй вызов с ошибкой
    decorated_error = log(str(log_file))(error_func)
    with pytest.raises(RuntimeError):
        decorated_error()

    contents = log_file.read_text()
    # Проверяем, что лог содержит нужные сообщения
    assert contents.count("started.") == 2
    assert contents.count("ok") == 1
    assert "error" in contents
