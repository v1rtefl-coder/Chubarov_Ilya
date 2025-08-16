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
