import functools
from tkinter import *

from src.Repository.data_provider import DataProvider
from src.Utilities.constants import Constants
from src.trading_platform import Account, Transfer, Auxiliary, NewOrder


class CreateGui:
    """Klasa odpowiedzialna za obsługę graficznego interfejsu programu"""

    def __init__(self, window):
        self.account = Account()
        self.transfer = Transfer()
        self.new_order = NewOrder()
        self.window = window
        self.set_up_gui()
        self.create_widgets()

    def set_up_gui(self):
        """Ustawienie parametrów początkowych okna platformy"""

        self.window.geometry(Constants.WINDOW_SIZE)  # ustawienie wymiarów okna
        self.window.resizable(False, False)  # zablokowanie możliwości zmiany rozmiaru okna
        self.window['bg'] = Constants.COLOUR_BACKGROUND  # wybór koloru tła
        self.window.title(Constants.TEXT_WINDOW_TITLE)  # nadanie tytułu dla głównego okna
        # TODO: implement window.iconbitmap with .ico

    def create_widgets(self):
        """Stworzenie, wyświetlenie, przypisanie funkcjonalności widżetów"""

        # --- tworzenie etykiet --- #

        # etykieta tytułowa
        self.main_title_label = Label(self.window,
                                      text=Constants.TEXT_MAIN_TITLE,
                                      bg=Constants.COLOUR_BACKGROUND,
                                      fg=Constants.COLOUR_TEXT,
                                      font=(
                                          Constants.FONT_TYPEFACE,
                                          Constants.FONT_SIZE_TITLE,
                                          Constants.FONT_WEIGHT_TITLE),
                                      pady=20)

        # etykieta z opisem
        self.main_description_label = Label(self.window,
                                            text=Constants.TEXT_MAIN_DESCRIPTION,
                                            bg=Constants.COLOUR_BACKGROUND,
                                            fg=Constants.COLOUR_TEXT,
                                            font=(Constants.FONT_TYPEFACE,
                                                  Constants.FONT_SIZE_DESCRIPTION),
                                            pady=20)

        # etykieta kwoty
        self.amount_label = Label(self.window,
                                  text=Constants.TEXT_AMOUNT,
                                  bg=Constants.COLOUR_BACKGROUND,
                                  fg=Constants.COLOUR_TEXT,
                                  padx=20,
                                  font=(Constants.FONT_TYPEFACE,
                                        Constants.FONT_SIZE_REGULAR))

        # etykieta wartości wolnych środków na koncie
        self.account_balance_label_text = StringVar()
        self.account_balance_label_text.set(self.account.get_current_account_balance_text())
        self.account_balance_label = Label(self.window,
                                           textvariable=self.account_balance_label_text,
                                           padx=20,
                                           bg=Constants.COLOUR_BACKGROUND,
                                           fg=Constants.COLOUR_TEXT,
                                           font=(Constants.FONT_TYPEFACE,
                                                 Constants.FONT_SIZE_REGULAR))

        # etykieta wartości zakupionych akcji
        self.value_of_shares_held_label_text = StringVar()
        self.value_of_shares_held_label_text.set(self.account.get_value_of_shares_held_text())
        self.value_of_shares_held_label = Label(self.window,
                                                textvariable=self.value_of_shares_held_label_text,
                                                padx=20,
                                                bg=Constants.COLOUR_BACKGROUND,
                                                fg=Constants.COLOUR_TEXT,
                                                font=(Constants.FONT_TYPEFACE,
                                                      Constants.FONT_SIZE_REGULAR))

        # etykieta całkowitej wartości konta
        self.total_account_value_label_text = StringVar()
        self.total_account_value_label_text.set(self.account.get_total_account_value_text())
        self.total_account_value_label = Label(self.window,
                                               textvariable=self.total_account_value_label_text,
                                               padx=20,
                                               bg=Constants.COLOUR_BACKGROUND,
                                               fg=Constants.COLOUR_TEXT,
                                               font=(Constants.FONT_TYPEFACE,
                                                     Constants.FONT_SIZE_REGULAR))

        # tworzenie pól tekstowych
        self.amount_entry_text = StringVar()
        self.limit_entry(self.amount_entry_text, Constants.ENTRY_NR_OF_CHARACTERS) # ograniczenie długości kwoty
        self.amount_entry = Entry(self.window,
                                  textvariable=self.amount_entry_text,  # Constants.TEXT_AMOUNT,
                                  bd=Constants.ENTRY_BORDER_SIZE,
                                  font=(Constants.FONT_TYPEFACE, Constants.ENTRY_FONT_SIZE),
                                  justify=CENTER,
                                  width=Constants.ENTRY_WIDTH)

        # ---tworzenie przycisków--- #

        # wciśnięcie przycisku powoduje wywołanie metody obsługującej opuszczenie platformy
        self.close_button = Button(self.window,
                                   text=Constants.TEXT_CLOSE_BUTTON,
                                   background=Constants.BUTTON_BACKGROUND_COLOUR,
                                   bd=Constants.BUTTON_BORDER_SIZE,
                                   cursor=Constants.ACTIVE_CURSOR,
                                   command=lambda: Auxiliary.exit_platform(self.window),
                                   padx=10)

        # wciśnięcie przycisku wywołuje metodę obsługującą wpłatę pieniędzy na konto
        self.deposit_amount_button = Button(self.window,
                                            text=Constants.TEXT_DEPOSIT_BUTTON,
                                            background=Constants.BUTTON_BACKGROUND_COLOUR,
                                            bd=Constants.BUTTON_BORDER_SIZE,
                                            cursor=Constants.ACTIVE_CURSOR,
                                            command=lambda: self.command_handle_transfer(Constants.DEPOSIT))

        # wciśnięcie przycisku wywołuje metodę obsługującą wypłatę pieniędzy z konta
        self.withdraw_amount_button = Button(self.window,
                                             text=Constants.TEXT_WITHDRAW_BUTTON,
                                             background=Constants.BUTTON_BACKGROUND_COLOUR,
                                             bd=Constants.BUTTON_BORDER_SIZE,
                                             cursor=Constants.ACTIVE_CURSOR,
                                             command=lambda: self.command_handle_transfer(Constants.WITHDRAWAL))

        # wciśnięcie przycisku wywołuje metodę obsługującą wypłatę wszystkich wolnych środków z konta
        self.withdraw_all_funds_button = Button(self.window,
                                                text=Constants.TEXT_WITHDRAW_ALL_BUTTON,
                                                background=Constants.BUTTON_BACKGROUND_COLOUR,
                                                bd=Constants.BUTTON_BORDER_SIZE,
                                                cursor=Constants.ACTIVE_CURSOR,
                                                command=lambda: self.command_handle_transfer(Constants.WITHDRAWAL_ALL))

        # wciśnięcie przycisku wywołuje funkcję obsługującą zakup akcji wybranej firmy
        self.buy_shares_button = Button(self.window,
                                        text=Constants.TEXT_BUY_SHARES_BUTTON,
                                        background=Constants.BUTTON_BACKGROUND_COLOUR,
                                        bd=Constants.BUTTON_BORDER_SIZE,
                                        cursor=Constants.ACTIVE_CURSOR,
                                        command=lambda: self.command_handle_new_order(Constants.BUY_ORDER))

        # wciśnięcie przycisku wywołuje funkcję obsługującą sprzedaż akcji wybranej firmy
        self.sell_shares_button = Button(self.window,
                                         text=Constants.TEXT_SELL_SHARES_BUTTON,
                                         background=Constants.BUTTON_BACKGROUND_COLOUR,
                                         bd=Constants.BUTTON_BORDER_SIZE,
                                         cursor=Constants.ACTIVE_CURSOR,
                                         command=lambda: self.command_handle_new_order(Constants.SELL_ORDER))

        # ---------------------------------------------------------------------------------------------- #

        # --- wyświetlanie etykiet --- #
        self.main_title_label.grid(row=0, column=0, sticky='nsew')
        self.main_description_label.grid(row=1, column=0, sticky='new')
        self.window.columnconfigure(0, weight=1)  # umieszczenie etykiet tytułowych na środku
        self.window.rowconfigure(1, weight=1)  # umieszczenie etykiet tytułowych u góry okna

        self.amount_label.place(x=0, y=500)
        self.account_balance_label.place(x=0, y=540)
        self.value_of_shares_held_label.place(x=180, y=540)
        self.total_account_value_label.place(x=500, y=540)

        # --- wyświetlanie pól tekstowych --- #
        self.amount_entry.place(x=70, y=500)

        # --- wyświetlanie przycisków --- #
        self.close_button.place(x=700, y=500)
        self.deposit_amount_button.place(x=200, y=495)
        self.withdraw_amount_button.place(x=300, y=495)
        self.withdraw_all_funds_button.place(x=360, y=495)
        self.buy_shares_button.place(x=50, y=400)
        self.sell_shares_button.place(x=150, y=400)

        # ---------------------------------------------------------------------------------------------- #

        # stworzenie listy dostępnych firm
        self.companies_listbox = Listbox(self.window,
                                         bg=Constants.COLOUR_BACKGROUND,
                                         selectbackground=Constants.LISTBOX_SELECTION_BACKGROUND,
                                         fg=Constants.LISTBOX_TEXT_COLOUR,
                                         width=Constants.LISTBOX_WIDTH,
                                         font=Constants.FONT_TYPEFACE,
                                         cursor=Constants.ACTIVE_CURSOR,
                                         bd=Constants.LISTBOX_BORDER_SIZE,
                                         justify=RIGHT,
                                         highlightthickness=Constants.LISTBOX_HIGHLIGHT_THICKNESS)

        # odznaczenie elementu z listy, w momencie utraty skupienia
        self.companies_listbox.bind('<FocusOut>', lambda e: self.companies_listbox.selection_clear(0, END))

        self.companies_listbox.place(x=50, y=175)

        # ---------------------------------------------------------------------------------------------- #

        # stworzenie listy zakupionych firm
        self.current_stock_positions_listbox = Listbox(self.window,
                                                       bg=Constants.COLOUR_BACKGROUND,
                                                       selectbackground=Constants.LISTBOX_SELECTION_BACKGROUND,
                                                       fg=Constants.LISTBOX_TEXT_COLOUR,
                                                       width=Constants.LISTBOX_WIDTH,
                                                       font=Constants.FONT_TYPEFACE,
                                                       cursor=Constants.ACTIVE_CURSOR,
                                                       bd=Constants.LISTBOX_BORDER_SIZE,
                                                       justify=CENTER,
                                                       highlightthickness=Constants.LISTBOX_HIGHLIGHT_THICKNESS)

        # odznaczenie elementu z listy, w momencie utraty skupienia
        self.current_stock_positions_listbox.bind('<FocusOut>',
                                                  lambda e: self.current_stock_positions_listbox.selection_clear(0,
                                                                                                                 END))

        self.current_stock_positions_listbox.place(x=500, y=200)

        # ---------------------------------------------------------------------------------------------- #

        # pole tekstowe umożliwiające wybór ilości akcji danej firmy
        self.stock_amount_spinbox = Spinbox(self.window, from_=1, to=10000, width=8)
        self.stock_amount_spinbox.place(x=100, y=360)

        self.insert_available_companies()

    def command_handle_new_order(self, order_type):
        """Metoda obsługuje nowe zlecenie złożone przez użytkownika"""

        # odczytujemy indeks wybranego elementu z listy firm - wynik jest w postaci jednoelementowej krotki
        selection_tuple = self.companies_listbox.curselection()

        if len(selection_tuple) == 0:
            # żaden element z listy nie został zaznaczony
            return

        # konwersja typu tuple na int
        company_index = functools.reduce(lambda a: a, selection_tuple)

        # odczytanie ilość akcji wybranych przez użytkownika do zlecenia
        stock_amount = self.stock_amount_spinbox.get()

        # wybór firmy, weryfikacja oraz ewentualna realizacja zlecenia
        successful_transaction = self.new_order.select_company(order_type, company_index, stock_amount)

        if not successful_transaction:
            return

        company = DataProvider.get_company(company_index)
        company_symbol = company.get_symbol()

        if not self.account.check_if_company_is_already_bought(company_symbol):
            # akcje firmy zostały zakupione po raz pierwszy - indeks nowej pozycji zostaje przypisany do słownika
            self.account.append_bought_company_to_listbox(company_symbol)

        bought_company_listbox_index = self.account.get_bought_company_listbox_index(company_symbol)

        self.current_stock_positions_listbox.delete(bought_company_listbox_index)
        company_position_size = self.account.get_nr_of_shares_owned(company_symbol)

        self.current_stock_positions_listbox.insert(bought_company_listbox_index,
                                                    "{}: {}".format(company_symbol, company_position_size))

        # aktualizacja etykiety informującej o wysokości wolnych środków na konice
        value_of_shares_held_text = self.account.get_value_of_shares_held_text()
        self.update_label(self.value_of_shares_held_label_text, value_of_shares_held_text)

        # aktualizacja etykiety informującej o wartości posiadanych akcji
        account_balance_text = self.account.get_current_account_balance_text()
        self.update_label(self.account_balance_label_text, account_balance_text)

        # po dokonaniu transakcji, odznaczamy element z listy
        self.companies_listbox.selection_clear(0, 'end')

    def command_handle_transfer(self, transfer_type):
        """Metoda zarządza transferem pieniężnym, po wciśnięciu przycisku w zależności od rodzaju transferu podanego przez użytkownika"""

        # odczytanie kwoty podanej przez użytkownika
        amount = self.amount_entry.get()

        if transfer_type == Constants.DEPOSIT:
            self.transfer.handle_deposit(amount)
        elif transfer_type == Constants.WITHDRAWAL:
            self.transfer.handle_withdrawal(amount, Constants.WITHDRAWAL)
        else:
            self.transfer.handle_withdrawal(amount, Constants.WITHDRAWAL_ALL)

        # aktualizacja etykiety informującej o wysokości wolnych środków na koncie
        current_account_balance_text = self.account.get_current_account_balance_text()
        self.update_label(self.account_balance_label_text, current_account_balance_text)

        # aktualizacja etykiety informującej o całkowitej wartości konta
        total_account_value_text = self.account.get_total_account_value_text()
        self.update_label(self.total_account_value_label_text, total_account_value_text)

        # usunięcie zawartości pola tekstowego
        self.amount_entry.delete(0, END)

    def insert_available_companies(self):
        """Metoda wypełnia listę firm dostępnych na rynku."""

        # odczytanie listy firm, których akcje można zakupić
        available_companies = DataProvider.get_all_companies()

        for company in available_companies:
            share_price = company.get_price()
            company_symbol = company.get_symbol()

            # odpowiednie formatowanie zależnie od ceny pojedynczej akcji
            if share_price < 10:
                self.companies_listbox.insert(END, "   {:>}    {:>8}   ".format(company_symbol, share_price))
            elif share_price < 100:
                self.companies_listbox.insert(END, "   {:>}   {:>8}   ".format(company_symbol, share_price))
            elif share_price < 1000:
                self.companies_listbox.insert(END, "   {:>}  {:>8}   ".format(company_symbol, share_price))
            else:
                self.companies_listbox.insert(END, "   {:>} {:>8}   ".format(company_symbol, share_price))

    @classmethod
    def update_label(cls, label_text_var, label_text):
        """Aktualizacja treści wyświetlanej przez zadaną etykietę"""

        label_text_var.set(label_text)

    @staticmethod
    def limit_entry(str_var, length):
        """Metoda ogranicza możliwość wpisywania znaków w polu tekstowym do długości otrzymanej w argumencie"""

        def callback(str_var):
            c = str_var.get()[0:length]
            str_var.set(c)

        str_var.trace("w", lambda name, index, mode, str_var=str_var: callback(str_var))
