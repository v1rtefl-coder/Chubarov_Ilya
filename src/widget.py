def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    parts = account_info.split()
    # Определяем тип - карта или счет
    if "счет" in account_info.lower():
        # Маскировка счета
        account_number = parts[-1]
        masked_number = f"**{account_number[-4:]}"
        return " ".join(parts[:-1] + [masked_number])
    else:
        # Маскировка карты
        card_number = parts[-1]
        masked_number = (f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}")
        return " ".join(parts[:-1] + [masked_number])


def get_date(date_str: str) -> str:
    """Преобразует дату из формата 'YYYY-MM-DDTHH:MM:SS.ssssss' в 'DD.MM.YYYY'."""
    date_part = date_str.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
