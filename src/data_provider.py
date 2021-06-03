from src.constants import Constants
from src.data import Data
from src.company import Company


class DataProvider:

    @classmethod
    def get_companies(cls):
        """Na podstawie listy firm zamieszczonej w data.companies_list tworzymy listę firm.
        companies_list zawiera nazwę firmy, jej symbol oraz cenę za jedną akcję.
        Na podstawie powyższej tablicy tworzona zostaje lista obiektów klasy Company."""

        companies_list = Data.companies_list
        companies = []

        for company in companies_list:
            # oddzielamy parametry separowane przecinkiem
            separate = company.split(Constants.DATA_SEPARATOR)

            company_name = separate[0]
            company_symbol = separate[1]
            company_share_price_str = separate[2]
            company_share_price = float(company_share_price_str)

            companies.append(Company(company_name, company_symbol, company_share_price))

        return companies
