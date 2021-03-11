# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 21:48:16 2020

@author: sumanya.sahoo
"""
import pandas as pd

def getData(filename):
    pro,pri = [],[]
    Pdf = pd.read_excel(filename,sheet_name="Price")
    df1 = Pdf[Pdf.columns[[0,1]]].dropna()
    df1.columns = ["Date","RO"]
    df1["Date"] = pd.to_datetime(df1["Date"])
    df1.index = df1["Date"]
    df1 = df1.drop(["Date"],axis=1)
    df2 = Pdf[Pdf.columns[[6,7]]].dropna()
    df2.columns = ["Date","PRO"]
    df2["Date"] = pd.to_datetime(df2["Date"])
    df2.index = df2["Date"]
    for i in df1.index:
        try: pro.append(df2.loc[i].PRO)
        except: 
            print("Data error for PRO on ", str(i.date()))
            pro.append(None)
    
    df1["PRO"] = pro
    
    df3 = Pdf[Pdf.columns[[3,4]]].dropna()
    df3.columns = ["Date","RI"]
    df3["Date"] = pd.to_datetime(df3["Date"])
    df3.index = df3["Date"]
    df3 = df3.drop(["Date"],axis=1)

    df4 = Pdf[Pdf.columns[[9,10]]].dropna()
    df4.columns = ["Date","PRI"]
    df4["Date"] = pd.to_datetime(df4["Date"])
    df4.index = df4["Date"]
    for i in df3.index:
        try : pri.append(df4.loc[i].PRI)
        except : 
            print("Data error for PRI on ", str(i.date()))
            pri.append(None)

    df3["PRI"] = pri
    
    Cdf = pd.read_excel(filename,sheet_name="Contracts")
    Cdf.index = Cdf.Ticker
    Cdf["Date"] = pd.to_datetime(Cdf["Date"])
    df5 = Cdf["Date"]

    Hdf = pd.read_excel(filename,sheet_name="Holidays")
    hlds =  list(Hdf["Date"])
    
    return df1,df3,df5,hlds
    
    
    
    

