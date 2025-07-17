def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер карты"""
    if len(card_number) < 16:
        raise ValueError("Номер карты слишком короткий")
    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер счета"""
    if len(account_number) < 4:
        raise ValueError("Номер счета слишком короткий")
    masked = "**" + account_number[-4:]
    return masked
