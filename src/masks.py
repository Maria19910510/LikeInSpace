from logger_config import setup_module_logger

logger = setup_module_logger(__name__)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер карты"""
    try:
        if len(card_number) < 16:
            raise ValueError("Номер карты слишком короткий")
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info(f"Маскировка номера карты: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Ошибка при маскировке номера карты: {e}")
        raise


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер счета"""
    try:
        if len(account_number) < 4:
            raise ValueError("Номер счета слишком короткий")
        masked = "**" + account_number[-4:]
        logger.info(f"Маскировка номера счета: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Ошибка при маскировке номера счета: {e}")
        raise
