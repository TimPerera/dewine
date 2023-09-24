"""
main.py
Provides a command line interface for ecommerce app.
"""

import argparse
import re
import logging



from app import run
from utils.logger import SetupLogging

# initialize logger
SetupLogging().setup_logging()

def date_range(value):
    "Checks if provided dates are correctly formatted."
    pattern = r'\[\[\d{4},\d{4}\],\[\d{1,2},\d{1,2}\],\[\d{1,2},\d{1,2}\]\]'
    
    if not re.match(pattern,value):
        raise argparse.ArgumentError('Error. Invalid date format, see argument help for more information.')
    
    date_range = value.strip('[]').split('],[')
    return {
        'y':list(map(int, date_range[0].split(','))),
        'm':list(map(int, date_range[1].split(','))),
        'd':list(map(int, date_range[2].split(',')))
    }

parser = argparse.ArgumentParser(description='User interface for DeWine!')
parser.add_argument('--file-path','-f',type=str, default='./wine_data/consolidated_wine_data.csv',
                    dest='file_path',help='File path directory to products database.')
parser.add_argument('--transactions', '-t', type = int, required=True,
                    dest='transactions', help='How many transactions?')
parser.add_argument('--num-customers','-c',type=int, required=True,
                    dest='num_customers', help='How many customers?')
parser.add_argument('--seasonal-dates','-s',type=date_range, dest='seasonal_dates', default=None,
                    help="Introduce seasonality in the form \
                    [[start_year, end_year],[start_month, end_month], [start_day, end_day]]). \
                        Example: --seasonal_dates [2019,2018],[5,8],[1,30]")
parser.add_argument('--num-items', '-i', type=int, dest='num_items', default=1,
                    help='How many product items per customer?')
parser.add_argument('--discount','-d', type=float, dest='discount', default=0,
                    help='Percentage discount to apply to final cost. Example: 0.05')
parser.add_argument('--wine-type','-w', type=str,choices=['Rose','Red','Sparkling','White'],
                     dest='wine_type', default=None, help='Choose wine type?')
parser.add_argument('--minimum-age-filter','-g',dest='min_age',type=int, default=None,
                    help='Filter customers greater than specified age limit.')
parser.add_argument('--maximum-age-filter','-l',dest='max_age',type=int, default=None,
                    help='Filter customer less than specified age limit.')

args = parser.parse_args()
print(f'file path',args.file_path)
if __name__=='__main__':
    print(f'Executed script, number of transactions {args.transactions}. Number of customers {args.num_customers}.\n \
          Type of transaction: {type(args.transactions)}. Type of customers: {type(args.num_customers)}')
    run(file_path=args.file_path,
        transactions=args.transactions,
        num_customers=args.num_customers,
        seasonal_dates=args.seasonal_dates,
        num_items=args.num_items,
        discount=args.discount,
        type_of_wine=args.wine_type,
        less_than_age_condition=args.min_age,
        greater_than_age_condition=args.max_age,
        )