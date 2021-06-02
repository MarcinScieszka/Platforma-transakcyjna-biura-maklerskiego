from src.constants import Constants
from tkinter import *
from platform import Auxiliary, Transfer, Account


def execute_transfer(transfer_type, amount_entry, account_balance_label_text):
    """Metoda wywołuje klasę obsługującą transfer pieniężny"""

    transfer = Transfer(amount_entry, account_balance_label_text)
    transfer.handle_transfer(transfer_type)


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

        # ---------------------------------------------------------------------------------------------- #

        # tworzenie etykiet
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

        # tworzenie przycisków
        cls.close_button = Button(cls.window,
                                  text=Constants.TEXT_CLOSE_BUTTON,
                                  cursor="hand2",
                                  command=lambda: Auxiliary.exit_platform(cls.window),
                                  padx=10)

        cls.deposit_amount_button = Button(cls.window,
                                           text=Constants.TEXT_DEPOSIT_BUTTON,
                                           cursor="hand2",
                                           command=lambda: execute_transfer(Constants.DEPOSIT, cls.amount_entry, cls.account_balance_label_text))
        cls.withdraw_amount_button = Button(cls.window,
                                            text=Constants.TEXT_WITHDRAW_BUTTON,
                                            cursor="hand2",
                                            command=lambda: execute_transfer(Constants.WITHDRAWAL, cls.amount_entry, cls.account_balance_label_text))
        cls.withdraw_all_funds_button = Button(cls.window,
                                               text=Constants.TEXT_WITHDRAW_ALL_BUTTON,
                                               cursor="hand2",
                                               command=lambda: execute_transfer(Constants.WITHDRAWAL_ALL, cls.amount_entry, cls.account_balance_label_text))

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

# def show_widgets(self):
#     """Metoda wyświetla na ekranie zdefiniowane widżety"""
