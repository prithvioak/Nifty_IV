from scraping import optionchain, scrape_strikes
from db_connect import db_connect, insert_into_db
import time
import numpy as np
from datetime import datetime, time
import time
from utils import *
import pytz
import pandas as pd; import os

def main():
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }
    i = 6
    print("We're running")
    (pd.DataFrame()).to_csv(os.path.join(os.getcwd(),"hello.csv"))
    while datetime.now(intz).time() > datetime.strptime("09:14:59","%H:%M:%S").time() and\
        datetime.now(intz).time() < datetime.strptime("15:30:01","%H:%M:%S").time() and\
        datetime.now(intz).weekday() <= 4:

        data = scrape_strikes(url, headers)

        if i == 6:
            option_chain = optionchain(url, headers)

            option_chain = option_chain.replace({np.nan: None})
            print(option_chain)

            # data = option_chain.to_records(index=False).tolist()
            # data = [row for row in data if None not in row]

            print("Data inserted successfully !")
            i = 0
        
        i += 1
            
        time.sleep(10)
    

if __name__ == '__main__':
    main()