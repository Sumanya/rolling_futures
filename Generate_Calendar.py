# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 16:25:30 2020

@author: sumanya.sahoo
"""

from datetime import datetime as dt
from pandas import offsets as pof
import numpy as np


def Advanced(date,params):
    if params[1] in np.arange(7) :        
        ans = date + pof.Day(np.mod(7-date.weekday()+params[1],7)) + (params[0]-1)*pof.Week(1)
    elif params[1] == 7:
        ans = date + params[0]*pof.Day(params[2])
    elif params[1] == 8:
        if date.weekday() < 5:
            ans = date + params[0]*pof.BusinessDay(params[2])
        else:
            ans = date + params[0]*pof.BusinessDay(params[2]+1)
    return ans


def Holidays(date,typ):
    if typ == 0 : 
        shift_dt = date + pof.BusinessDay(-1)
    elif typ ==1 : 
        shift_dt = date + pof.BusinessDay(1)
    elif typ == 2:
        shift_dt = date + pof.BusinessDay(1)
        if shift_dt.month > date.month:
            shift_dt = date + pof.BusinessDay(-1)
    return shift_dt 


def Calendar(st,end,window,recur,select,cus_mnth,hol_list,adj_typ,adv):
    final = []
    i = 0
    adj_quatr = 0
    while True:
        if select < 9:
            if window == 0: fst = st + pof.Week(i)
            elif window == 1 : fst = st + pof.MonthBegin(i)
            elif window ==2 :
                if adj_quatr == 1:
                    fst = st + pof.MonthBegin(3*i)
                    if i==0 and fst.month > st.month:
                        fst = fst+pof.MonthBegin(-1)
                else:
                    if i == 0: fst = st + pof.QuarterBegin(i)+pof.MonthBegin(-2)
                    else: fst = st + pof.QuarterBegin(i)+pof.MonthBegin(1)
            elif window == 3: fst = st + pof.YearBegin(i+1)
        
        else :
            if window == 0: fst = st + pof.Day(7-st.weekday())
            elif window == 1 : fst = st + pof.MonthEnd(i+1)
            elif window ==2 : fst = st + pof.QuarterEnd(i+1)
            elif window == 3: fst = st + pof.YearEnd(i+1)
            
            if select ==9:
                ans = fst - pof.Day(recur)
            elif select ==10:
                if fst.weekday() < 5:
                    ans = fst - pof.BusinessDay(recur)
                else:
                    ans = fst - pof.BusinessDay(recur+1)
              
        if select in np.arange(7) :        
            ans = fst + pof.Day(np.mod(7-fst.weekday()+select,7)) + recur*pof.Week(1)
        elif select == 7:
            ans = fst + recur*pof.Day(1)
        elif select == 8:
            if fst.weekday() < 5:
                ans = fst + pof.BusinessDay(recur)
            else :
                ans = fst + pof.BusinessDay(recur+1)
                
        if sum([np.abs(i) for i in adv])>0:
            ans = Advanced(ans,adv)                          
        
        if ans.date() <= end.date() :
            i += 1
            if adj_typ in  np.arange(3):
                while ans.date() in hol_list:
                    ans = Holidays(ans,adj_typ)
            if ans.date() >= st.date() and ans.month in cus_mnth:
                final.append(ans.date())
        else:
            break
    return final

#
#def setParams(criteria,st,end,recur,select,window,cus_mnth,hol_list,adv)
#
#if __name__ == "__main__":
#    print("Enter criteria as 0 or 1 (Custom_Month, Holiday, Advanced, Variable_Quater)  :")
#    criteria = [int(i) for i in input().split(",")]        
#    print("Enter start date (ddmmyyyy):")
#    st =  dt.strptime(input(),"%d%m%Y").date()
#    print("Enter end date (ddmmyyyy):")
#    end =  dt.strptime(input(),"%d%m%Y").date()
#    print("Enter recurrence :")
#    recur = int(input())-1
#    print("Enter type of Day:")
#    select = int(input())
#    if criteria[0] ==0:
#        print("Select window (0-Week, 1-Month, 2-Quater, 3-Year)")
#        window = int(input())
#        cus_mnth = list(1+np.arange(12))
#    else:
#        print("Select custom months(comma_separated)")
#        cus_mnth = [int(i) for i in input().split(",")]
#        window = 1
#    
#    if criteria[1] == 0:
#        hol_list = []
#        adj_typ = 0
#
#    else:
#        print("Type of adjustment(0-Previous, 1-Following, 2- Modified Following)")
#        adj_typ = int(input())
#        hol_list = []
#        
#    if criteria[2] == 0:
#        adv = [0,0,0]
#    else:
#        print("Enter Advanced criteria (Number,Day,Preivious/After):")
#        adv = [int(i) for i in input().split(",")]
#     
#    dates = Calendar(st,end,window,recur,select,cus_mnth,adj_typ,adv,criteria[-1])
#    
#    