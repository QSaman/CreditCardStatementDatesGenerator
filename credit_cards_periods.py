#!/bin/python

import argparse
import array
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import holidays
import sys

def generate_holidays(year_list, country, subdivision):
    global local_holidays
    local_holidays = holidays.country_holidays(country, subdiv=subdivision, years=year_list)

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

def generate_credit_card_periods(start_date, end_date):
    cur_date = start_date
    while True:
        cur_date_business_day = get_next_business_day(cur_date)
        if cur_date_business_day > end_date:
            break
        print(cur_date_business_day)
        cur_date = (cur_date + relativedelta(months=1))

def main():
    parser = argparse.ArgumentParser()


    parser.add_argument('-c', '--country', nargs='?', default='CA', help='Country code in ISO 3166. By default it\'s Canada')
    parser.add_argument('-p', '--subdivision', nargs='?', default=None, help='Subdivision (.e.g province and state) code. By default it\'s Quebec')

    subparsers = parser.add_subparsers(dest='command')

    list_holidays_parser = subparsers.add_parser('list_holidays', help='List holidays')
    list_holidays_parser.add_argument('year', nargs='?', default=datetime.now().year, type=int, help='A year. If you don\'t specify it, it\'s current year')

    generate_dates_parser = subparsers.add_parser('generate_dates', help='Generate dates for credit card statements')
    generate_dates_parser.add_argument('-s', '--start-date', required=True, help='Start date in YYYY-MM-DD format')
    generate_dates_parser.add_argument('-e', '--end-date', required=True, help='End date in YYYY-MM-DD format')

    is_work_day_parser = subparsers.add_parser('is_work_day', help='Determines whether or not a specific date is a work day')
    is_work_day_parser.add_argument('date', help='Date in YYYY-MM-DD format')

    global args
    args = parser.parse_args()
    if args.country == 'CA' and args.subdivision is None:
        args.subdivision = 'QC'

    if args.command == "list_holidays":
        generate_holidays(args.year, args.country, args.subdivision)
        print_holidays()
    elif args.command == "generate_dates":
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date()
        if start_date > end_date:
            print("Start date cannot be greater than end date", file=sys.stderr)
            sys.exit(1)

        start_year = start_date.year
        end_year = end_date.year
        generate_holidays(array.array('i', range(start_year, end_year + 1)), args.country, args.subdivision)
        generate_credit_card_periods(start_date, end_date)
    elif args.command == "is_work_day":
        date_obj = datetime.strptime(args.date, '%Y-%m-%d').date()
        generate_holidays(date_obj.year, args.country, args.subdivision)
        print(is_work_day(date_obj))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
