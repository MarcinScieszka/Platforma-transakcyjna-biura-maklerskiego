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
            separate = company.split(Constants.DATA_SEPARATOR)  # oddzielamy parametry separowane przecinkiem
            companies.append(Company(separate[0], separate[1], separate[2]))

        return companies
