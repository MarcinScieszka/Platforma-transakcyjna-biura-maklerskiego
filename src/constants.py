class Constants:
    """Klasa zawierająca stałe, które zostały wykorzystane podczas implementacji programu"""

    TEXT_MAIN_TITLE = 'Platforma transakcyjna Future Station'
    TEXT_MAIN_DESCRIPTION = 'Biuro maklerskie William-Scott Trade'
    TEXT_CLOSE_BUTTON = 'Wyjdź'
    # TEXT_CONFIRM_BUTTON = 'Zatwierdź'
    TEXT_WITHDRAW_BUTTON = 'Wypłać'
    TEXT_WITHDRAW_ALL_BUTTON = 'Wypłać dostępne środki'
    TEXT_DEPOSIT_BUTTON = 'Wpłać depozyt'
    TEXT_AMOUNT = 'Kwota'
    TEXT_CURRENT_BALANCE = 'Saldo: '
    # TEXT_ACCOUNT_VALUE = 'Wartość konta: '
    TEXT_CURRENCY = ' zł'

    COLOUR_BACKGROUND = '#2A2A2E'
    COLOUR_TEXT = '#FAFAFA'

    FONT_TYPEFACE = 'Arial'
    FONT_WEIGHT_TITLE = 'bold'
    FONT_SIZE_TITLE = 20
    FONT_SIZE_DESCRIPTION = 14
    FONT_SIZE_REGULAR = 12

    MESSAGE_ERROR = 'Błąd'
    MESSAGE_ERROR_VALUE = 'Podano nieprawidłową wartość'
    MESSAGE_ERROR_NEGATIVE_BALANCE = 'Niewystarczająca ilość środków do wypłaty'

    STATE_DEPOSIT = 0  # chęć wpłaty
    STATE_WITHDRAWAL = 1  # chęć wypłaty
    STATE_WITHDRAWAL_ALL = 2  # chęć wypłaty wszystkich wolnych środków

    MESSAGE_CONFIRM_EXIT = 'Potwierdź wyjście'
    MESSAGE_CONFIRM_EXIT_TEXT = 'Czy na pewno chcesz opuścić platformę?'

    DATA_SEPARATOR = ','
