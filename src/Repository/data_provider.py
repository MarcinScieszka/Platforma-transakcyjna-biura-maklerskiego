from src.Utilities.constants import Constants
from src.Repository.data import Data
from src.Repository.company import Company


class DataProvider:
    __companies = []

    @classmethod
    def instantiate_companies(cls):
        """Na podstawie listy firm zamieszczonej w data.companies_list zostaje utworzona listę firm.
        companies_list zawiera nazwę firmy, jej symbol oraz cenę za jedną akcję.
        Na podstawie powyższej tablicy tworzona zostaje lista obiektów klasy Company."""

        companies_list = Data.companies_list

        for company in companies_list:
            company_name, company_share_price, company_symbol = cls.separate_company_values(company)

            cls.__companies.append(Company(company_name, company_symbol, company_share_price))

    @staticmethod
    def separate_company_values(company):
        """Metoda oddziela poszczególne parametry separowane przecinkiem,
        białe znaki z początku i końca parametrów zostają usunięte,
        zwracane wartości: nazwa, cena za akcję, symbol danej firmy"""

        separate = company.split(Constants.DATA_SEPARATOR)
        company_name = separate[0].strip()
        company_symbol = separate[1].strip()
        company_share_price_str = separate[2].strip()
        company_share_price = float(company_share_price_str)

        return company_name, company_share_price, company_symbol

    @classmethod
    def get_company(cls, company_index):
        """Metoda zwraca obiekt klasy Company"""

        return cls.__companies[company_index]

    @classmethod
    def get_all_companies(cls):
        """Metoda zwraca wszystkie obiekty klasy Company"""

        return cls.__companies

    @classmethod
    def make_companies_dict(cls):
        """Metoda tworzy i zwraca słownik o wielkości wszystkich dostępnych do zakupu firm.
        klucze to symbole firm
        wartości są zerami - domyślnie użytkownik nie posiada akcji żadnej firmy"""

        company_symbols = []
        for company in cls.__companies:
            # tworzenie listy symboli wszystkich firm
            company_symbols.append(company.get_symbol())

        owned_companies = {company_symbol: 0 for company_symbol in company_symbols}

        return owned_companies
