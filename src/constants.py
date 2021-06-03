class Constants:
    """Klasa zawierająca stałe, które zostały wykorzystane podczas implementacji programu"""

    # stałe odnoszące się do nazw pól tekstowych
    TEXT_MAIN_TITLE = 'Platforma transakcyjna Future Station'
    TEXT_MAIN_DESCRIPTION = 'Biuro maklerskie William-Scott Trade'
    TEXT_CLOSE_BUTTON = 'Wyjdź'
    # TEXT_CONFIRM_BUTTON = 'Zatwierdź'
    TEXT_WITHDRAW_BUTTON = 'Wypłać'
    TEXT_WITHDRAW_ALL_BUTTON = 'Wypłać wszystkie środki'
    TEXT_DEPOSIT_BUTTON = 'Wpłać depozyt'
    TEXT_AMOUNT = 'Kwota'
    TEXT_CURRENT_BALANCE = 'Saldo: '
    # TEXT_ACCOUNT_VALUE = 'Wartość konta: '
    TEXT_CURRENCY = ' zł'  # waluta, w której obsługiwane są transakcje

    # stałe odnoszące się do zastosowanej palety kolorów
    COLOUR_BACKGROUND = '#2A2A2E'
    COLOUR_TEXT = '#FAFAFA'

    # stałe odnoszące się do właściwości tekstu
    FONT_TYPEFACE = 'Ubuntu'
    FONT_WEIGHT_TITLE = 'bold'
    FONT_SIZE_TITLE = 20
    FONT_SIZE_DESCRIPTION = 14
    FONT_SIZE_REGULAR = 12

    # stałe odnoszące się do treści komunikatów
    MESSAGE_ERROR = 'Błąd'
    MESSAGE_ERROR_VALUE = 'Podano nieprawidłową wartość'
    MESSAGE_ERROR_NEGATIVE_BALANCE = 'Niewystarczająca ilość środków do wypłaty'
    MESSAGE_CONFIRM_EXIT = 'Potwierdź wyjście'
    MESSAGE_CONFIRM_EXIT_TEXT = 'Czy na pewno chcesz opuścić platformę?'

    # stałe odnoszące się do statusu transakcji gotówkowych wybranego przez użytkownika
    DEPOSIT = 0  # chęć wpłaty
    WITHDRAWAL = 1  # chęć wypłaty
    WITHDRAWAL_ALL = 2  # chęć wypłaty wszystkich wolnych środków

    # separator danych stosowany podczas tworzenia listy firm
    DATA_SEPARATOR = ','

    # stałe odnoszące się do typów zleceń akcji
    BUY_ORDER = 'Zlecenie zakupu akcji'
    SELL_ORDER = 'Zlecenie sprzedaży akcji'

    # stałe dotyczące prowizji podczas wypłaty środków z konta
    WITHDRAWAL_COMMISSION_THRESHOLD = 300  # próg pobierania prowizji
    WITHDRAWAL_COMMISSION_AMOUNT = 30  # kwota prowizji podczas wypłaty poniżej progu
