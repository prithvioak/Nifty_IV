import requests
import pandas as pd
import numpy as np  
from datetime import datetime
import time
from utils import *
import logging
import os
import pytz
import pathlib

def optionchain(url, headers):
    response = requests.get(url, headers=headers)
    data = response.json()
    option_chain_data = data['records']['data']
    option_chain_data_df = pd.DataFrame(option_chain_data)
    option_chain_data
    # print(option_chain_data_df['CE'].iloc[55])
    print(option_chain_data_df.columns)

    option_chain = pd.DataFrame()
    option_chain_CE = pd.DataFrame()
    option_chain_CE["CE"] = option_chain_data_df["CE"]
    option_chain_CE_expand = pd.concat([option_chain_CE.drop(["CE"], axis=1), option_chain_CE["CE"].apply(pd.Series)], axis=1)
    option_chain_CE_expand.add_prefix('CE_')

    option_chain_PE = pd.DataFrame()
    option_chain_PE["PE"] = option_chain_data_df["PE"]
    option_chain_PE_expand = pd.concat([option_chain_PE.drop(["PE"], axis=1), option_chain_PE["PE"].apply(pd.Series)], axis=1)
    option_chain_PE_expand.add_prefix('PE_')

    option_chain = pd.concat([option_chain_CE_expand, option_chain_PE_expand])

    option_chain["DATE"]= str(datetime.now(intz).date())
    option_chain["TIME"] = datetime.now(intz)

    print(option_chain)
    file_name = str(datetime.now(intz).time()).replace('.', '_').replace(':','_') + '.csv'
    print("The path is:", os.path.join(os.getcwd(),"data_collection",file_name))
    # subdirs = [x[0] for x in os.walk('.')]
    # print(subdirs)
    option_chain.to_csv(os.path.join(os.getcwd(),"data_collection",file_name), index=False)
    # option_chain.to_csv(os.path.join("./data_collection",file_name), index=False)
    print("Successfulll")

    return option_chain

def scrape_strikes(url, headers):
    session = requests.Session()
    request = session.get(url, headers=headers)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, cookies=cookies).json()
    rawdata = pd.DataFrame(response)
    rawop = pd.DataFrame(rawdata['filtered']['data'])
    rawop['Date'] = datetime.now(intz).date()
    rawop['Time'] = datetime.now(intz).time()

    # print('rawop["CE"]\n', (rawop.iloc[0])['CE']['underlyingValue'], rawop['CE'].iloc[0]['underlyingValue'])
    # underlying_value = rawop.iloc[0]['underlyingValue'] ## fix this
    underlying_value = (rawop.iloc[0])['CE']['underlyingValue']

    atmStrike = round_to_multiple(underlying_value, 50)

    strikes1 = list(range(atmStrike-300, atmStrike, 50))
    strikes2 = list(range(atmStrike, atmStrike+300, 50))

    strikes = strikes1 + strikes2
    test_df = rawop[rawop['strikePrice'].isin(strikes)]
    test_df['Date'] = datetime.now(intz).date()
    test_df['call_iv'] = test_df['CE'].apply(lambda x: x['impliedVolatility'])
    test_df['put_iv'] = test_df['PE'].apply(lambda x: x['impliedVolatility'])
    test_df['underlying_value'] = underlying_value

    test_df['strike_type_call'] = ''
    test_df['strike_type_put'] = ''

    price = test_df['underlying_value'].iloc[0]
    atmStrike = round_to_multiple(price, 50)

    test_df['strike_type_call'] = test_df['strikePrice'].apply(lambda a: get_type_ce(a, atmStrike))
    test_df['strike_type_put'] = test_df['strikePrice'].apply(lambda a: get_type_pe(a, atmStrike))

    test_df = test_df[['Date', 'Time', 'strikePrice', 'call_iv', 'put_iv', 'underlying_value', 'strike_type_call', 'strike_type_put']]

    print(test_df)

    return [tuple(row) for row in test_df.values]