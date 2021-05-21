from tkinter import *
from tkinter import messagebox
from src.constants import *
from src.gui import CreateGui


class Platform:
    """Główna klasa platformy transakcyjnej"""

    def __init__(self, window):
        self.window = window
        CreateGui.create_gui_params(window)  # wywołanie klasy ustawiającej parametry gui

        # tworzenie etykiet
        self.main_title_label = Label(self.window, text=TEXT_MAIN_TITLE, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                                      font=(FONT_TYPEFACE, FONT_SIZE_TITLE, FONT_WEIGHT_TITLE), pady=20)
        self.main_description_label = Label(self.window, text=TEXT_MAIN_DESCRIPTION, bg=COLOUR_BACKGROUND,
                                            fg=COLOUR_TEXT, font=(FONT_TYPEFACE, FONT_SIZE_DESCRIPTION), pady=20)
        self.amount_label = Label(self.window, text=TEXT_AMOUNT, bg=COLOUR_BACKGROUND, fg=COLOUR_TEXT,
                                  font=(FONT_TYPEFACE, FONT_SIZE_REGULAR))

        self.account_value_label = Label(self.window, text='tymczasowe account_value', bg=COLOUR_BACKGROUND,
                                         fg=COLOUR_TEXT,
                                         font=(FONT_TYPEFACE, FONT_SIZE_REGULAR))

        # wyświetlanie etykiet
        self.main_title_label.grid(row=0, column=2, columnspan=6, sticky='ew')
        self.main_description_label.grid(row=1, column=2, columnspan=6, sticky='ew')
        self.amount_label.grid(row=3, column=0, sticky=W)

        # tworzenie pól tekstowych
        self.amount_text = StringVar()
        self.amount_entry = Entry(self.window, textvariable=TEXT_AMOUNT)

        # wyświetlanie pól tekstowych
        self.amount_entry.grid(row=3, column=1)

        # tworzenie przycisków
        self.close_button = Button(self.window, text=TEXT_CLOSE_BUTTON, command=lambda: self.quit_platfom(), padx=10)
        self.deposit_amount_button = Button(self.window, text=TEXT_DEPOSIT_BUTTON,
                                            command=lambda: Transfer(self.window,
                                                                     STATE_DEPOSIT))  # Transfer(self.window, amount, state) ))
        self.withdraw_amount_button = Button(self.window, text=TEXT_WITHDRAW_BUTTON,
                                             command=lambda: Transfer(self.window,
                                                                      STATE_WITHDRAWAL))  # self.read_amount(STATE_WITHDRAWAL))

        # wyświetlanie przycisków
        self.close_button.grid(row=10, column=1)
        self.deposit_amount_button.grid(row=3, column=2)
        self.withdraw_amount_button.grid(row=3, column=3)

    def show_error(self, error_message):
        """Metoda wyświetla okno z komunikatem błędu."""

        messagebox.showerror('Błąd', error_message)

    def quit_platfom(self):
        """Metoda zamyka główne okno aplikacji."""

        self.window.destroy()


class Transfer(Platform):
    account_value = 0
    amount = None

    def __init__(self, window, state):
        super().__init__(window)
        self.state = state
        self.handle_transfer(self.state)

    def handle_transfer(self, state):
        amount = self.get_amount()
        is_correct = self.verify(amount)

        if is_correct:
            amount = int(amount)  # wiemy, że kwota jest poprawna, możemy ją castować
            if self.state == STATE_DEPOSIT:
                print('Czy na pewno chcesz wpłacić %lf zł' % amount)

            if self.state == STATE_WITHDRAWAL:
                print('Czy na pewno chcesz wypłacić %lf zł' % amount)

    def get_amount(self):
        """Metoda odczytuje kwotę podaną przez użytkownika"""

        return self.amount_entry.get()

    def verify(self, amount):
        """Metoda weryfikuję poprawność danych wprowadzonych przez użytkownika podczas podawania kwoty"""

        try:
            amount = int(amount)
        except ValueError:
            self.show_error(ERROR_MESSAGE_VALUE)
            return False

        if amount <= 0:
            self.show_error(ERROR_MESSAGE_VALUE)
            return False

        return True
