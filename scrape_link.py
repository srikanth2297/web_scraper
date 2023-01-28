import selenium
import requests
import time
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os
import pandas as pd
from pandas import *
from locale import currency
import os

from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil import parser
from pymongo import ReadPreference
import boto3
import json
from bson.json_util import loads
from datetime import datetime, timedelta
from dateutil.tz import *
from datetime import datetime, tzinfo, timezone
from pytz import timezone
from datetime import datetime, timedelta
import  datetime
from pytz import timezone
import os
import pytz
utc = pytz.utc
utc.zone
import re

from bson.json_util import dumps as mongo_dumps
import gzip
import boto3

options = webdriver.ChromeOptions()
options.add_argument("headless")


bucket_name=os.environ["S3_BUCKET"]


AWS_ACCESS_KEY_ID=os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY=os.environ["AWS_SECRET_ACCESS_KEY"]

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

current_date=datetime.datetime.now()
YEAR=current_date.year
MONTH=current_date.month
DAY=current_date.day
HOUR=current_date.hour
MINUTE=current_date.minute

present_time=str(YEAR) + "-" + str(MONTH) + "-" + str(DAY) 


def main(): 
    print('start')

    cwd_path = '/Users/srikanths/scripts/sensibullcsv'
    # userList = (pd.read_csv(r'users_sensibull.csv').squeeze().tolist())
    userList = ['accustomed-hornet','broad-field','gated-bat','some-bichon','rapid-chrysanthemum','picking-bus','supreme-lettuce','parting-carnation','blinking-rat','gloried-hovercraft']
    # data = read_csv('users_sensibull.csv')
    # df = pd.DataFrame(data)
    # userList =  df.tolist()
    
    # print(type(userList))
    # print(userList)
    # numberOfUsers = len(userList)
    # # element = userList[0].text 
    # # print(element)
    # # print(type(element))
    # for user in userList : 
    #     print(user)
        
    
    for user in userList:
        url = 'https://web.sensibull.com/verified-pnl/' + user  + '/'

        browserMain = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        dataMain = browserMain.get(url)

        time.sleep(3)
        
        
        

        sourceMain = browserMain.page_source
        documentMain = BeautifulSoup(sourceMain, 'html.parser')
        

        print(user)
        twitter = documentMain.find('span',class_= 'style__MutedText-sc-1a2uzpb-8 iylEpU')
        twitterat = twitter.text

        

        
        screenshotList = documentMain.find_all('div' , class_= 'style__ScreenshotHistoryListItem-sc-cn9x4k-4 iVLvPH')
        # print(screenshotList)
        historyList = []
        firstUrl = documentMain.find_all('div', class_= 'style__ScreenshotHistoryListItem-sc-cn9x4k-4 gIfmdg')

        for screenshot in firstUrl:
            firstLink = 'https://web.sensibull.com' + screenshot.find('a').get('href')
            historyList.append(firstLink)
        
        for screenshot in screenshotList:
            historyLink = 'https://web.sensibull.com' + screenshot.find('a').get('href')
            historyList.append(historyLink)


        
        filename = cwd_path + '/'
        filename += user
        filename += ".csv"
        fields = []
        fields.append('date') 
        fields.append('user') 
        fields.append('@twitter')
        fields.append('ticker')
        fields.append('Name')
        fields.append('Qty')
        fields.append('Avg')
        fields.append('LTP')
        fields.append('P/L')
        fields.append('pnlvalue')
        with open(filename, 'a+') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            
            for link in historyList:
                url = link
                browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                data = browser.get(url)
                time.sleep(3)
                source = browser.page_source
                document = BeautifulSoup(source, 'html.parser')
                stockTablesDiv = document.find_all('div', class_='underlying-summary')
                snapshotDate = document.find('div', class_='taken-timestamp')
                snapshotDateText = snapshotDate.text + ''
                snapshotDateSnip = snapshotDateText[8:19]
                print(snapshotDateSnip)
                

                for stockTableDiv in stockTablesDiv:

                    rows = []

                    tableRows = stockTableDiv.find_all(class_='MuiTableRow-root');
                    
                    for row in tableRows:
                        row_val = []
                        styledPnls = row.find('div', class_='styled-pnl')
                        row_val.append(snapshotDateSnip) 
                        row_val.append(user) 
                        row_val.append(twitterat)
                        ticker = stockTableDiv.find('span').text
                        row_val.append(ticker)
                        for col in row:
                            row_val.append(col.text)
                        row_val.append(styledPnls.find('div').attrs['value'])   
                        rows.append(row_val)
                    
                    csvwriter.writerows(rows)
                    csvfile.flush()
        
    with open(filename, 'a+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        
        
        
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        data = browser.get(url)
        time.sleep(3)
        source = browser.page_source
        document = BeautifulSoup(source, 'html.parser')
        stockTablesDiv = document.find_all('div', class_='underlying-summary')
        snapshotDate = document.find('div', class_='taken-timestamp')
        snapshotDateText = snapshotDate.text + ''
        snapshotDateSnip = snapshotDateText[8:19]
        print(snapshotDateSnip)
        

        for stockTableDiv in stockTablesDiv:

            rows = []

            tableRows = stockTableDiv.find_all(class_='MuiTableRow-root');
            
            for row in tableRows:
                row_val = []
                styledPnls = row.find('div', class_='styled-pnl')
                row_val.append(snapshotDateSnip) 
                row_val.append(user) 
                row_val.append(twitterat)
                ticker = stockTableDiv.find('span').text
                row_val.append(ticker)
                for col in row:
                    row_val.append(col.text)
                row_val.append(styledPnls.find('div').attrs['value'])   
                rows.append(row_val)
            
            csvwriter.writerows(rows)
            csvfile.flush()

    file_path="/mongo-data" + "/semsibull-data"
    
    bucket_path= "sensibull_scrape" + present_time + "-data"
    
    s3_client.upload_file(
        file_path,
        bucket_name,
        bucket_path,
    )


main();

