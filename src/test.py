class Func:
    def __init__(self, window):
        self.window = window

    def quit(self):
        """Metoda zamyka główne okno aplikacji."""

        self.window.destroy()
