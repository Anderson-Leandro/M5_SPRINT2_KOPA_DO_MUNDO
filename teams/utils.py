from datetime import datetime, timedelta
from math import floor
from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError


def data_processing(data):
    if data["titles"] < 0:
        raise NegativeTitlesError

    DATE_FORMATER = "%Y-%m-%d"

    first_cup = datetime.strptime(data["first_cup"], DATE_FORMATER)

    check_year = first_cup.year - 1930

    if check_year != 0:
        if check_year < 0 or check_year % 4 != 0:
            raise InvalidYearCupError

    now = datetime.now()

    if data["titles"] > (floor((now.year - first_cup.year) / 4) + 1):
        raise ImpossibleTitlesError

    return data
