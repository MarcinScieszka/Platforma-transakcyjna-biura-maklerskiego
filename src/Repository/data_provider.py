from src.Utilities.constants import Constants
from src.Repository.data import Data
from src.Repository.company import Company


class DataProvider(Data):
    __companies = []

    @classmethod
    def instantiate_companies(cls):
        """Na podstawie listy firm zamieszczonej w data.companies_list zostaje utworzona listę firm.
        companies_list zawiera nazwę firmy, jej symbol oraz cenę za jedną akcję.
        Na podstawie powyższej tablicy tworzona zostaje lista obiektów klasy Company."""

        companies_list = Data._companies_list
        cls.__companies = [cls.create_company_objects(company) for company in companies_list]

    @staticmethod
    def create_company_objects(company):
        """Metoda oddziela poszczególne parametry separowane przecinkiem,
        białe znaki z początku i końca parametrów zostają usunięte,
        Metoda zwraca obiekt Company z argumentami: nazwa, cena za akcję oraz symbol danej firmy"""

        separate = company.split(Constants.DATA_SEPARATOR)
        company_name = separate[0].strip()
        company_symbol = separate[1].strip()
        company_share_price_str = separate[2].strip()
        company_share_price = float(company_share_price_str)

        return Company(company_name, company_symbol, company_share_price)

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

        # tworzenie listy symboli wszystkich firm
        company_symbols = [company.get_symbol() for company in cls.__companies]

        owned_companies = {company_symbol: 0 for company_symbol in company_symbols}

        return owned_companies
