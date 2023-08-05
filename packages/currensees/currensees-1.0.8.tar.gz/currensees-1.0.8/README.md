# Currency API Python Package

The package provides convenient access to the [Currency API](https://moatsystems.com/currency-api/) functionality from applications written in the Python language.

## Requirements

Python 2.7 and later.

## Setup

You can install this package by using the pip tool and installing:

```python
pip install currensees
## OR
easy_install currensees
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

Usage Example
-------------

```python
from currensees.auth import Auth
from currensees.currencies import Currencies
from currensees.historical import Historical
from currensees.convert import Convert
from currensees.convert_all import ConvertAll
from currensees.daily_average import DailyAverage
from currensees.weekly_average import WeeklyAverage
from currensees.margins_spreads import MarginsSpreads

# Authenticate and log in
auth = Auth()
username = "your_username"
password = "your_password"

result = auth.login(username, password)
print("Login successful:", result)

currencies = Currencies(auth.headers)
result = currencies.get_currencies(username, "19", "04", "2023")
print("Currencies:", result)

uuid = "currency_uuid"
result = currencies.get_currency(uuid, username, "19", "04", "2023")
print("Currency:", result)

historical = Historical(auth.headers)
result = historical.get_historical(username, "2023_04_19", "19", "04", "2023")
print("Historical data:", result)

uuid = "historical_uuid"
result = historical.get_historical_currency(uuid, username, "19", "04", "2023", "2023_04_19")
print("Historical currency:", result)

convert = Convert(auth.headers)
result = convert.convert_currency("2023_04_19", "GBP", "EUR", "500")
print("Converted amount:", result)

convert_all = ConvertAll(auth.headers)
result = convert_all.convert_all_currencies("GBP", 120, "2023_04_19")
print("Converted amounts:", result)

daily_average = DailyAverage(auth.headers)
result = daily_average.get_daily_average("2023_04_19")
print("Daily average:", result)

weekly_average = WeeklyAverage(auth.headers)
result = weekly_average.get_weekly_average("2023_04_03", "2023_04_07")
print("Weekly average:", result)

margins_spreads = MarginsSpreads(auth.headers)
result = margins_spreads.get_margins_spreads(username, "19", "04", "2023")
print("Margins and spreads:", result)

uuid = "margins_spreads_uuid"
result = margins_spreads.get_margins_spreads_currency(uuid, username, "19", "04", "2023")
print("Margins and spreads for currency:", result)
```

## Setting up Currency API Account

Subscribe here for a [user account](https://moatsystems.com/currency-api/).


## Using the Currency API

You can read the [API documentation](https://docs.currensees.com/) to understand what's possible with the Currency API. If you need further assistance, don't hesitate to [contact us](https://moatsystems.com/contact/).


## License

This project is licensed under the [BSD 3-Clause License](https://moatsystems.com/assets/license/BSD_3_Clause.txt).


## Copyright

(c) 2023 [Moat Systems Limited](https://moatsystems.com/). All Rights Reserved.
