#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

from __future__ import print_function

import datetime
import warnings

import MySQLdb as mdb 
import requests

from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
from sqlalchemy import create_engine

# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'root'
db_pass = 'root'
db_name = 'quantitative'
con = mdb.connect(db_host, db_user, db_pass, db_name)


def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols in the database.
    """
    with con: 
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol where ticker in (%s,%s,%s,%s)" % ('600179','002266','601211','000725'))
        data = cur.fetchall()
        return [(d[0], d[1]) for d in data]


def get_daily_historic_data_google(ticker, years=5):
   
    param = {
        'q': ticker, # Stock symbol (ex: "AAPL")
        'i': "300", # Interval size in seconds ("86400" = 1 day intervals)
        'p': "%sY" % years # Period (Ex: "1Y" = 1 year)
        }
    # get price data (return pandas dataframe)
    df = get_price_data(param)
    
    '''
        param = [
            {'q': ticker} # Stock symbol (ex: "AAPL")
        ]
        period = "3Y"
        interval = 60*5 # 30 minutes
        df = get_prices_time_data(param, period, interval)
    '''
    return df

def insert_daily_data_into_db(
        data_vendor_id, symbol_id, daily_data
    ):
    """
    Takes a list of tuples of daily data and adds it to the
    MySQL database. Appends the vendor ID and symbol ID to the data.

    daily_data: List of tuples of the OHLC data (with 
    adj_close and volume)
    """
    # Create the time now
    now = datetime.datetime.utcnow()
    #print(daily_data)
    #print(daily_data.index)
    #for index in daily_data.index:
        # print(daily_data.loc[index].values[0:-1])


    #engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/quantitative', echo=False)
    #daily_data.to_sql('daily_price', engine, if_exists='append', index=False)

    # Amend the data to include the vendor ID and symbol ID
    daily_data_list = []
    for index, row in daily_data.iterrows():
        daily_data_list.append((data_vendor_id, symbol_id, row['price_date'], now, now,
        row['Open'],
        row['High'], 
        row['Low'], 
        row['Close'], 
        row['Volume'], 
        row['Close']))


    # Create the insert strings
    column_str = """data_vendor_id, symbol_id, price_date, created_date, 
                 last_updated_date, open_price, high_price, low_price, 
                 close_price, volume, adj_close_price"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = "INSERT INTO 5min_price (%s) VALUES (%s)" % \
        (column_str, insert_str)

    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    with con: 
        cur = con.cursor()
        cur.executemany(final_str, daily_data_list)
    

if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation
    # from the Yahoo precision to Decimal(19,4) datatypes
    warnings.filterwarnings('ignore')

    # Loop over the tickers and insert the daily historical
    # data into the database
    #tickers = obtain_list_of_db_tickers()
   
    tickers = obtain_list_of_db_tickers()
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print(
            "Adding data for %s: %s out of %s" % 
            (t[1], i+1, lentickers)
        )
        google_data = get_daily_historic_data_google(t[1])
        google_data['price_date'] = google_data.index
        print(len(google_data.index))
        print(google_data.head(1))
        insert_daily_data_into_db('1', t[0], google_data)
    print("Successfully added Yahoo Finance pricing data to DB.")
    '''
    df = get_daily_historic_data_google('600179')
    print(len(df.index))
    print(df.head(1))
    print(df.tail(1))
    '''