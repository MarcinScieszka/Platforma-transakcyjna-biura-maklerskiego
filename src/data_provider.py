from src.constants import Constants
from src.data import Data
from src.company import Company


class DataProvider:

    __companies = []

    @classmethod
    def receive_companies(cls):
        """Na podstawie listy firm zamieszczonej w data.companies_list tworzymy listę firm.
        companies_list zawiera nazwę firmy, jej symbol oraz cenę za jedną akcję.
        Na podstawie powyższej tablicy tworzona zostaje lista obiektów klasy Company."""

        companies_list = Data.companies_list

        for company in companies_list:
            company_name, company_share_price, company_symbol = cls.separate_company_values(company)

            cls.__companies.append(Company(company_name, company_symbol, company_share_price))

    @staticmethod
    def separate_company_values(company):
        """Metoda oddziela poszczególne parametry separowane przecinkiem,
        elementy zwracane to nazwa, cena za akcję oraz symbol danej firmy"""

        separate = company.split(Constants.DATA_SEPARATOR)
        company_name = separate[0]
        company_symbol = separate[1]
        company_share_price_str = separate[2]
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
