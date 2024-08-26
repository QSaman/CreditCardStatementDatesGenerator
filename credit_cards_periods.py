#!/bin/python

from datetime import date
from datetime import datetime
from datetime import timedelta
import holidays

current_year = 2024
province = 'QC'
country = 'CA'
first_date = datetime(2024, 1, 1)

local_holidays = holidays.country_holidays(country, prov=province, years=current_year)

def print_holidays():
    for date, name in sorted(local_holidays.items()):
        print(date, name)

def is_work_day(date):
    if date.weekday() in holidays.WEEKEND or date in local_holidays:
        return False
    return True

def get_next_business_day(date):
    if is_work_day(date):
        return date
    one_day = timedelta(days=1)
    cur_date = date + one_day
    while not is_work_day(cur_date):
        cur_date = cur_date + one_day
    return cur_date

def generate_credit_card_periods():
    cur_date = first_date
    while True:
        cur_date_business_day = get_next_business_day(cur_date)
        print(cur_date_business_day.date())
        if (cur_date.month < 12):
            cur_date = datetime(cur_date.year, cur_date.month + 1, cur_date.day)
        else:
            break


def main():
    generate_credit_card_periods()

if __name__ == "__main__":
    main()



