from tkinter import *
from src.constants import Constants
from src.platform import Account, Transfer, Auxiliary, Market, NewOrder


class CreateGui:

    def __init__(self, window):
        self.window = window

    @classmethod
    def create_gui(cls, window):
        """
        Metoda ustawia główne parametry graficznego interfejsu programu wykorzystując bibliotekę tkinter.
        """

        my_account = Account()

        cls.window = window
        cls.window.geometry(Constants.WINDOW_SIZE)  # ustawienie wymiarów okna
        cls.window.resizable(False, False)  # zablokowanie możliwości zmiany rozmiaru okna
        cls.window['bg'] = Constants.COLOUR_BACKGROUND  # wybór koloru tła
        cls.window.title(Constants.TEXT_WINDOW_TITLE)  # nadanie tytułu dla głównego okna
        # TODO: implement window.iconbitmap with .ico

        # ---------------------------------------------------------------------------------------------- #

        # --- tworzenie etykiet --- #

        # etykieta tytułowa
        cls.main_title_label = Label(cls.window,
                                     text=Constants.TEXT_MAIN_TITLE,
                                     bg=Constants.COLOUR_BACKGROUND,
                                     fg=Constants.COLOUR_TEXT,
                                     font=(
                                         Constants.FONT_TYPEFACE,
                                         Constants.FONT_SIZE_TITLE,
                                         Constants.FONT_WEIGHT_TITLE),
                                     pady=20)

        # etykieta z opisem
        cls.main_description_label = Label(cls.window,
                                           text=Constants.TEXT_MAIN_DESCRIPTION,
                                           bg=Constants.COLOUR_BACKGROUND,
                                           fg=Constants.COLOUR_TEXT,
                                           font=(Constants.FONT_TYPEFACE,
                                                 Constants.FONT_SIZE_DESCRIPTION),
                                           pady=20)

        # etykieta kwoty
        cls.amount_label = Label(cls.window,
                                 text=Constants.TEXT_AMOUNT,
                                 bg=Constants.COLOUR_BACKGROUND,
                                 fg=Constants.COLOUR_TEXT,
                                 padx=20,
                                 font=(Constants.FONT_TYPEFACE,
                                       Constants.FONT_SIZE_REGULAR))

        # eykieta wartości wolnych środków na koncie
        cls.account_balance_label_text = StringVar()
        cls.account_balance_label_text.set(my_account.get_current_account_balance_text())
        cls.account_balance_label = Label(cls.window,
                                          textvariable=cls.account_balance_label_text,
                                          padx=20,
                                          bg=Constants.COLOUR_BACKGROUND,
                                          fg=Constants.COLOUR_TEXT,
                                          font=(Constants.FONT_TYPEFACE,
                                                Constants.FONT_SIZE_REGULAR))

        # etykieta wartości zakupionych akcji
        cls.value_of_shares_held_label_text = StringVar()
        cls.value_of_shares_held_label_text.set(my_account.get_current_value_of_shares_held_text())
        cls.value_of_shares_held_label = Label(cls.window,
                                               textvariable=cls.value_of_shares_held_label_text,
                                               padx=20,
                                               bg=Constants.COLOUR_BACKGROUND,
                                               fg=Constants.COLOUR_TEXT,
                                               font=(Constants.FONT_TYPEFACE,
                                                     Constants.FONT_SIZE_REGULAR))

        # etykieta całkowitej wartości konta
        cls.total_account_value_label_text = StringVar()
        cls.total_account_value_label_text.set(my_account.get_total_account_value_text())
        cls.total_account_value_label = Label(cls.window,
                                              textvariable=cls.total_account_value_label_text,
                                              padx=20,
                                              bg=Constants.COLOUR_BACKGROUND,
                                              fg=Constants.COLOUR_TEXT,
                                              font=(Constants.FONT_TYPEFACE,
                                                    Constants.FONT_SIZE_REGULAR))

        # tworzenie pól tekstowych
        cls.amount_text = StringVar()
        cls.amount_entry = Entry(cls.window, textvariable=Constants.TEXT_AMOUNT)

        transfer = Transfer(cls.amount_entry, cls.account_balance_label_text)

        # ---tworzenie przycisków--- #

        # wciśnięcie przycisku powoduje wywołanie metody obsługującej opuszczenie platformy
        cls.close_button = Button(cls.window,
                                  text=Constants.TEXT_CLOSE_BUTTON,
                                  background=Constants.BUTTON_BACKGROUND_COLOUR,
                                  bd=Constants.BUTTON_BORDER_SIZE,
                                  cursor=Constants.ACTIVE_CURSOR,
                                  command=lambda: Auxiliary.exit_platform(cls.window),
                                  padx=10)

        # wciśnięcie przycisku wywołuje metodę obsługującą wpłatę pieniędzy na konto
        cls.deposit_amount_button = Button(cls.window,
                                           text=Constants.TEXT_DEPOSIT_BUTTON,
                                           background=Constants.BUTTON_BACKGROUND_COLOUR,
                                           bd=Constants.BUTTON_BORDER_SIZE,
                                           cursor=Constants.ACTIVE_CURSOR,
                                           command=lambda: transfer.handle_deposit())

        # wciśnięcie przycisku wywołuje metodę obsługującą wypłatę pieniędzy z konta
        cls.withdraw_amount_button = Button(cls.window,
                                            text=Constants.TEXT_WITHDRAW_BUTTON,
                                            background=Constants.BUTTON_BACKGROUND_COLOUR,
                                            bd=Constants.BUTTON_BORDER_SIZE,
                                            cursor=Constants.ACTIVE_CURSOR,
                                            command=lambda: transfer.handle_withdrawal(Constants.WITHDRAWAL))

        # wciśnięcie przycisku wywołuje metodę obsługującą wypłatę wszystkich wolnych środków z konta
        cls.withdraw_all_funds_button = Button(cls.window,
                                               text=Constants.TEXT_WITHDRAW_ALL_BUTTON,
                                               background=Constants.BUTTON_BACKGROUND_COLOUR,
                                               bd=Constants.BUTTON_BORDER_SIZE,
                                               cursor=Constants.ACTIVE_CURSOR,
                                               command=lambda: transfer.handle_withdrawal(Constants.WITHDRAWAL_ALL))

        # ---------------------------------------------------------------------------------------------- #

        # wyświetlanie etykiet
        cls.main_title_label.grid(row=0, column=0, sticky='nsew')
        cls.main_description_label.grid(row=1, column=0, sticky='new')
        cls.window.columnconfigure(0, weight=1)  # umieszczenie etykiet tytułowych na środku
        cls.window.rowconfigure(1, weight=1)  # umieszczenie etykiet tytułowych u góry okna

        cls.amount_label.place(x=0, y=500)
        cls.account_balance_label.place(x=0, y=540)
        cls.value_of_shares_held_label.place(x=150, y=540)
        cls.total_account_value_label.place(x=500, y=540)

        # wyświetlanie pól tekstowych
        cls.amount_entry.place(x=70, y=500)

        # wyświetlanie przycisków
        cls.close_button.place(x=700, y=500)
        cls.deposit_amount_button.place(x=200, y=495)
        cls.withdraw_amount_button.place(x=300, y=495)
        cls.withdraw_all_funds_button.place(x=360, y=495)

        # ---------------------------------------------------------------------------------------------- #

        # stworzenie listy dostępnych firm
        cls.companies_listbox = Listbox(cls.window,
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
        cls.companies_listbox.bind('<FocusOut>', lambda e: cls.companies_listbox.selection_clear(0, END))

        cls.companies_listbox.place(x=50, y=200)

        # ---------------------------------------------------------------------------------------------- #

        # stworzenie listy zakupionych firm
        cls.current_stock_positions_listbox = Listbox(cls.window,
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
        cls.current_stock_positions_listbox.bind('<FocusOut>', lambda e: cls.current_stock_positions_listbox.selection_clear(0, END))

        cls.current_stock_positions_listbox.place(x=500, y=200)

        # ---------------------------------------------------------------------------------------------- #

        # pole tekstowe umożliwiające wybór ilości akcji danej firmy
        cls.stock_amount_spinbox = Spinbox(cls.window, from_=1, to=10000, width=10)
        cls.stock_amount_spinbox.place(x=250, y=350)

        cls.market = Market(cls.companies_listbox)
        cls.market.insert_available_companies()

        cls.new_order = NewOrder(cls.stock_amount_spinbox, cls.account_balance_label_text, cls.value_of_shares_held_label_text, cls.companies_listbox)

        # wciśnięcie przycisku wywołuje funkcję obsługującą zakup akcji wybranej firmy
        cls.purchase_shares_button = Button(cls.window,
                                            text=Constants.TEXT_PURCHASE_SHARES_BUTTON,
                                            background=Constants.BUTTON_BACKGROUND_COLOUR,
                                            bd=Constants.BUTTON_BORDER_SIZE,
                                            cursor=Constants.ACTIVE_CURSOR,
                                            command=lambda: cls.new_order.select_company(Constants.BUY_ORDER))

        cls.purchase_shares_button.place(x=250, y=300)

        # ---------------------------------------------------------------------------------------------- #
