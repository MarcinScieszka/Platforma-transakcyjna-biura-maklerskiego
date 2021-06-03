from tkinter import *
from src.constants import Constants
from src.platform import Account, Transfer, Auxiliary, Market


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
        cls.window.geometry("800x600")  # ustawienie wymiarów okna na 800 na 600 pikseli
        cls.window.resizable(False, False)  # zablokowanie możliwości zmiany rozmiaru okna
        cls.window['bg'] = Constants.COLOUR_BACKGROUND  # wybór koloru tła
        cls.window.title("Platforma transakcyjna")  # nadanie tytułu dla głównego okna
        # TODO: implement window.iconbitmap with .ico

        # TODO: separate widgets by functionality?
        # ---------------------------------------------------------------------------------------------- #

        # --- tworzenie etykiet --- #
        cls.main_title_label = Label(cls.window,
                                     text=Constants.TEXT_MAIN_TITLE,
                                     bg=Constants.COLOUR_BACKGROUND,
                                     fg=Constants.COLOUR_TEXT,
                                     font=(
                                         Constants.FONT_TYPEFACE,
                                         Constants.FONT_SIZE_TITLE,
                                         Constants.FONT_WEIGHT_TITLE),
                                     pady=20)
        cls.main_description_label = Label(cls.window,
                                           text=Constants.TEXT_MAIN_DESCRIPTION,
                                           bg=Constants.COLOUR_BACKGROUND,
                                           fg=Constants.COLOUR_TEXT,
                                           font=(Constants.FONT_TYPEFACE,
                                                 Constants.FONT_SIZE_DESCRIPTION),
                                           pady=20)
        cls.amount_label = Label(cls.window,
                                 text=Constants.TEXT_AMOUNT,
                                 bg=Constants.COLOUR_BACKGROUND,
                                 fg=Constants.COLOUR_TEXT,
                                 padx=20,
                                 font=(Constants.FONT_TYPEFACE,
                                       Constants.FONT_SIZE_REGULAR))

        cls.account_balance_label_text = StringVar()
        cls.account_balance_label_text.set(my_account.get_current_account_balance_text())
        cls.account_balance_label = Label(cls.window,
                                          textvariable=cls.account_balance_label_text,
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
                                  cursor="hand2",
                                  command=lambda: Auxiliary.exit_platform(cls.window),
                                  padx=10)

        # wciśnięcie przycisku wywołuje metodę obsługującą wpłatę pieniędzy na konto
        cls.deposit_amount_button = Button(cls.window,
                                           text=Constants.TEXT_DEPOSIT_BUTTON,
                                           cursor="hand2",
                                           command=lambda: transfer.handle_transfer(Constants.DEPOSIT))

        # wciśnięcie przycisku wywołuje metodę obsługującą wypłatę pieniędzy z konta
        cls.withdraw_amount_button = Button(cls.window,
                                            text=Constants.TEXT_WITHDRAW_BUTTON,
                                            cursor="hand2",
                                            command=lambda: transfer.handle_transfer(Constants.WITHDRAWAL))

        # wciśnięcie przycisku wywołuje metodę obsługującą wypłatę wszystkich wolnych środków z konta
        cls.withdraw_all_funds_button = Button(cls.window,
                                               text=Constants.TEXT_WITHDRAW_ALL_BUTTON,
                                               cursor="hand2",
                                               command=lambda: transfer.handle_transfer(Constants.WITHDRAWAL_ALL))

        # ---------------------------------------------------------------------------------------------- #

        # wyświetlanie etykiet
        cls.main_title_label.grid(row=0, column=0, sticky='nsew')
        cls.main_description_label.grid(row=1, column=0, sticky='new')
        cls.window.columnconfigure(0, weight=1)  # umieszczenie etykiet tytułowych na środku
        cls.window.rowconfigure(1, weight=1)  # umieszczenie etykiet tytułowych u góry okna

        cls.amount_label.place(x=0, y=500)
        cls.account_balance_label.place(x=0, y=540)

        # wyświetlanie pól tekstowych
        cls.amount_entry.place(x=70, y=500)

        # wyświetlanie przycisków
        cls.close_button.place(x=700, y=500)
        cls.deposit_amount_button.place(x=200, y=495)
        cls.withdraw_amount_button.place(x=300, y=495)
        cls.withdraw_all_funds_button.place(x=200, y=530)

        # ---------------------------------------------------------------------------------------------- #

        # stworzenie listboxa, który przechowuje listę dostępnych firm
        cls.companies_listbox = Listbox(cls.window,
                                        bg=Constants.COLOUR_BACKGROUND,
                                        selectbackground='purple',
                                        fg='white',
                                        width=40,
                                        font=Constants.FONT_TYPEFACE,
                                        cursor='hand2',
                                        bd=0,
                                        highlightthickness=0)

        # odznaczenie elementu z listy, w momencie utraty skupienia
        cls.companies_listbox.bind('<FocusOut>', lambda e: cls.companies_listbox.selection_clear(0, END))

        cls.companies_listbox.place(x=150, y=250)

        # ---------------------------------------------------------------------------------------------- #

        # pole tekstowe umożliwiające wybór ilości akcji danej firmy
        cls.stock_amount_spinbox = Spinbox(cls.window, from_=1, to=10000)
        cls.stock_amount_spinbox.place(x=400, y=350)

        cls.market = Market(cls.stock_amount_spinbox, cls.companies_listbox)
        cls.market.insert_available_companies()

        # wciśnięcie przycisku wywołuje metodę obsługującą wybranie firmy spośród dostępnych
        cls.buy_shares_button = Button(cls.window,
                                       background='#f1f1f1',
                                       fg='black',
                                       bd=0,
                                       # relief=RAISED, # relief can be flat, groove, raised, ridge, solid, or sunken
                                       cursor="hand2",
                                       text="Zakup akcje",
                                       command=lambda: cls.market.select_company(Constants.BUY_ORDER))

        cls.buy_shares_button.place(x=20, y=200)

        # ---------------------------------------------------------------------------------------------- #
