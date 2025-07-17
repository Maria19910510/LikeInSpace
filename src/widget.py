from src.masks import get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """Функция определяет счет это или номер карты и возвращает замаскированный"""
    card_info_list = card_info.split()
    if "Счет" in card_info_list:
        return f"Счет **{card_info_list[-1][-4:]}"
    else:
        card_name = " ".join(card_info_list[:-1])
        card_number = card_info_list[-1].replace(" ", "")
        return f"{card_name} {get_mask_card_number(card_number)}"


def get_date(date_str: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ"""
    date_list = date_str.split("-", 2)
    date_list[2] = date_list[2][:2]
    date_list_reverse = ".".join(date_list[::-1])
    return date_list_reverse


print(mask_account_card("Visa Classic 1234567890123456"))
print(get_date("2023-10-23"))
