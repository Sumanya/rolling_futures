# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:33:13 2020

@author: sumanya.sahoo
"""

import mysql.connector as mariadb
import pandas as pd

def DB_connect(query):  
        mariadb_connection=mariadb.connect(host='evs01cpa008', user='root', password='cajust1234', database='factset')
        cursor=mariadb_connection.cursor()
    
        try:
            cursor.execute(query)  
        except mariadb.Error as error:
            print("Error{}".format(error))

        try:
            sql_data=pd.DataFrame(cursor.fetchall())
            sql_data.columns=cursor.column_names
        except Exception as e:
            print("Error_{}".format(e))
            sql_data=pd.DataFrame()        
        cursor.close()
        return sql_data

def getHolidays(ticker):
    q3 = 'SELECT Date FROM roll_fut_holiday WHERE IndexTicker = "'+ticker+'"'
    hld = DB_connect(q3)
    return list(hld[hld.columns[0]])

def getLastRolldate(name,date):
    q8 = 'SELECT Date FROM roll_fut_output WHERE Name = "'+name+'" AND Date < "'+date.strftime('%Y-%m-%d')+'"'
    dates = DB_connect(q8)
    return max(dates["Date"])

def getRollSchedule(idx_ticker):
    q7 = 'SELECT * FROM roll_fut_index_roll_schedule WHERE Index_Ticker = "'+idx_ticker+'"'
    rlsc = DB_connect(q7)
    return rlsc

def getIndexData(name):
    q9 = 'SELECT * FROM roll_fut_index_data WHERE Index_Ticker = "'+name+'"'
    data = DB_connect(q9)
    return data

def getRolldates(Ul_name):
    q12 = 'SELECT * FROM roll_fut_contracts WHERE Underlying = "'+Ul_name+'"'
    data = DB_connect(q12)
    data.index = data.Ticker
    return data.LTD

def getPrices(name):
    q13 = 'SELECT Date,Contract_Name,Contract_Price FROM roll_fut_price_data WHERE Generic_Name = "'+name+'"'
    price = DB_connect(q13)
    price.index = price.Date
    price = price.drop(["Date"],axis=1)
    price.Contract_Price = price.Contract_Price.astype(float)
    return price
