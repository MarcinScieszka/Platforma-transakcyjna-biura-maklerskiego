# Platforma transakcyjna biura maklerskiego
## Opis zadania
- Platforma przechowuje informację o wartości wolnych środków na koncie.
- Platforma przechowuje informację o wartości konta (saldo).
    - Saldo wynosi sumę wartości posiadanych akcji wraz z wartością wolnych środków.
- Platforma przechowuje listę firm, których akcje można zakupić wraz z ceną za jedną akcję.
- Platforma przechowuje listę firm, których akcje posiadamy, wraz z ilością posiadanych sztuk.
- Pole tekstowe pozwalające na wprowadzenie kwoty, przycisk pozwalający na wpłacenie depozytu na konto, przycisk pozwalający na wypłatę pieniędzy z konta.
- Wpłata środków
    - Możliwość wielokrotnego wpłacania środków.
    - Minimalny depozyt wynoszący 100 zł.
- Wypłata środków
    - Możliwość wielokrotnego wypłacania środków.
    - Brak pobieranej prowizji przy wypłacie wynoszącej minimum 300zł
    - Prowizja od wypłaty środków z konta dla kwoty poniżej 300zł wynosząca 30zł.
- Pole tekstowe pozwalające na wybranie wolumenu akcji do zakupu, przycisk pozwalający na zakup akcji, przycisk pozwalający na sprzedaż akcji.
- Zakup akcji
    - Możliwość wielokrotnego zakupu akcji.
    - Prowizja za transakcję zakupu akcji: 0,2%, lecz nie mniej niż 5zł.
    - Pojedyncza transakcja umożliwia zakup dowolnej ilości akcji (dowolnego wolumenu), jeżeli stan konta na to pozwala.
- Sprzedaż akcji
    - Możliwość wielokrotnej sprzedaży akcji.
    - Brak prowizji za sprzedaż akcji.
    - Pojedyncza transakcja umożliwia sprzedanie więcej niż jednej akcji - nie więcej niż posiadana ilość.

## Testy
1. próba wpłaty na konto kwoty poniżej 100zł - oczekiwana informacja o błędzie
2. próba wypłaty z konta kwoty większej niż stan wolnych środków - oczekiwana informacja o błędzie
3. próba sprzedaży akcji w ilości większej niż aktualnie posiadana - oczekiwana informacja o błędzie
4. próba zakupu akcji za kwotę większą niż stan wolnych środków - oczekiwana informacja o błędzie
5. wpłata 500zł na konto - oczekiwane zwiększenie wartości wolnych środków o 500zł
6. wypłata z konta 200zł - oczekiwane pobranie 30zł prowizji oraz zmniejszenie wartości wolnych środków o 170zł
7. zakup 10 akcji jednej firmy kosztujących 100zł za sztukę - oczekiwane zwiększenie ilości posiadanych akcji danej firmy o 10 oraz zmniejszenie wartości wolnych środków o 1005zł (10 * 100zł + prowizja 5zł, ponieważ 1000zł * 0,2% = 2zł, 2zł < 5zł)
8. sprzedaż 4 akcji akcji jednej firmy kosztujących 100zł za sztukę - oczekiwane zmniejszenie ilości posiadanych akcji danej firmy o 4 oraz zwiększenie wartości wolnych środków o 400zł
