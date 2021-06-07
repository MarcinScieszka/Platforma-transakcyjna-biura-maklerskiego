class Constants:
    """Klasa zawierająca stałe, które zostały wykorzystane podczas implementacji programu"""

    # stałe konfiguracyjne
    WINDOW_SIZE = '800x600'
    TEXT_WINDOW_TITLE = 'Platforma transakcyjna'

    # stałe dotyczące warunków dokonywania wpłat/wypłat
    WITHDRAWAL_COMMISSION_THRESHOLD = 300  # próg pobierania prowizji
    WITHDRAWAL_COMMISSION_AMOUNT = 30  # kwota prowizji podczas wypłaty poniżej progu
    MINIMAL_DEPOSIT_AMOUNT = 100
    MINIMAL_WITHDRAWAL_AMOUNT = WITHDRAWAL_COMMISSION_AMOUNT + 0.5

    BUYING_SHARES_COMMISSION = 0.002 # prowizja pobierana podczas zakupu akcji

    # stałe odnoszące się do nazw pól tekstowych
    TEXT_MAIN_TITLE = 'Platforma transakcyjna Future Station'
    TEXT_MAIN_DESCRIPTION = 'Biuro maklerskie William-Scott Trade'
    TEXT_CLOSE_BUTTON = 'Wyjdź'
    TEXT_WITHDRAW_BUTTON = 'Wypłać'
    TEXT_WITHDRAW_ALL_BUTTON = 'Wypłać wszystkie środki'
    TEXT_DEPOSIT_BUTTON = 'Wpłać depozyt'
    TEXT_BUY_SHARES_BUTTON = 'Zakup akcje'
    TEXT_SELL_SHARES_BUTTON = 'Sprzedaj akcje'
    TEXT_AMOUNT = 'Kwota'
    TEXT_CURRENT_BALANCE = 'Saldo: '
    TEXT_VALUE_OF_SHARES_HELD = 'Wartość posiadanych akcji: '
    TEXT_TOTAL_ACCOUNT_VALUE = 'Wartość konta: '
    TEXT_CURRENCY = ' zł'  # waluta, w której obsługiwane są transakcje

    # stałe odnoszące się do zastosowanej palety kolorów
    COLOUR_BACKGROUND = '#2A2A2E'
    COLOUR_TEXT = '#FAFAFA'
    LISTBOX_SELECTION_BACKGROUND = '#800080'
    LISTBOX_BACKGROUND_COLOUR = '#2A2A2E'
    LISTBOX_TEXT_COLOUR = '#ffffff'
    BUTTON_BACKGROUND_COLOUR = '#f1f1f1'

    # stałe odnoszące się do właściwości tekstu
    FONT_TYPEFACE = 'Ubuntu'
    FONT_WEIGHT_TITLE = 'bold'
    FONT_SIZE_TITLE = 20
    FONT_SIZE_DESCRIPTION = 14
    FONT_SIZE_REGULAR = 12

    # stałe odnoszące się do treści komunikatów
    MESSAGE_ERROR = 'Błąd'

    MESSAGE_INSUFFICIENT_DEPOSIT_AMOUNT = 'Niewystarczająca kwota depozytu: '
    MESSAGE_MINIMAL_DEPOSIT_AMOUNT = 'Minimalna wysokość depozytu wynosi: ' + str(MINIMAL_DEPOSIT_AMOUNT) + TEXT_CURRENCY
    MESSAGE_ERROR_MINIMAL_WITHDRAWAL_AMOUNT = 'Minimalna wypłata wynosi: ' + str(MINIMAL_WITHDRAWAL_AMOUNT)

    MESSAGE_ERROR_NEGATIVE_BALANCE = 'Niewystarczający stan środków do wypłaty'

    MESSAGE_ERROR_VALUE = 'Podano nieprawidłową wartość'

    MESSAGE_ERROR_NOT_ENOUGH_FUNDS = 'Niewystarczający stan środków do zakupu akcji'
    MESSAGE_ERROR_NOT_ENOUGH_SHARES = 'Niewystarczająca liczba posiadanych akcji do sprzedaży'

    MESSAGE_CONFIRM_EXIT = 'Potwierdź wyjście'
    MESSAGE_CONFIRM_EXIT_TEXT = 'Czy na pewno chcesz opuścić platformę?'
    MESSAGE_CONFIRM_SELL_SHARES = 'Potwierdź sprzedaż akcji'
    MESSAGE_CONFIRM_BUY_SHARES = 'Potwierdź zakup akcji'

    # stałe odnoszące się do statusu transakcji gotówkowych wybranego przez użytkownika
    DEPOSIT = 0  # chęć wpłaty
    WITHDRAWAL = 1  # chęć wypłaty
    WITHDRAWAL_ALL = 2  # chęć wypłaty wszystkich wolnych środków

    # separator danych stosowany podczas tworzenia listy firm
    DATA_SEPARATOR = ','

    # stałe odnoszące się do typów zleceń akcji
    BUY_ORDER = 'Zlecenie zakupu akcji'
    SELL_ORDER = 'Zlecenie sprzedaży akcji'

    ACTIVE_CURSOR = 'hand2'  # wygląd kursora po najechaniu na przyciski/listboxa

    # konfiguracja przycisków
    BUTTON_BORDER_SIZE = 0

    # konfiguracja list
    LISTBOX_WIDTH = 18
    LISTBOX_BORDER_SIZE = 0
    LISTBOX_HIGHLIGHT_THICKNESS = 0

    # konfiguracja pola wpisowego
    ENTRY_FONT_SIZE = 10
    ENTRY_BORDER_SIZE = 0
    ENTRY_WIDTH = 10
    ENTRY_NR_OF_CHARACTERS = 8
