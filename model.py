# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 16:51:45 2020

@author: sumanya.sahoo
"""
import datetime
import pandas as pd
from pandas import offsets as pof
from fractions import Fraction
import db
from getExcelData import getData


def units(rlamt,u_1,u_2,t,icl,pri,pro,LD):
    if t > 0:
        u1 = (icl/pri)*sum(rlamt[:LD-t+1])
        u2 = (icl/pro)*(1-sum(rlamt[:LD-t+1]))
    elif t == 0:
        u1 = 0
        u2 = u_1
    else:
        u1 = u_1
        u2 = u_2
    return u1,u2

def weights(t):
    if t == 0:
        w1 = 1
        w2 = 0
    elif t == 1:
        w1 = 0
        w2 = 1
    return w1,w2




def Calculate(stdt,enddt,LD,dfRI,dfRO,hol_list,rollDates,rlamt,typ):
#    x = time.time()
    
    print(len(dfRO),len(dfRI),len(hol_list),len(rollDates))

    intlvl = 100
    run_date = stdt
    dts,idx,idxprd,uro,uri = [],[],[-2],[],[]
    ro,ri,pro,pri,ltd,rlflg = [],[],[],[],[],[]
    rlcnt,cnt,flg = 0,-2,0
    reduce1 =  lambda x: -2 if x < -1 else x-1
    reduce2 =  lambda x: 0 if x < 1 else x-1
    srl = 0
    print
    while run_date <= enddt:
        try:
             
            if  run_date > stdt and rol_date== (run_date+pof.CustomBusinessDay(LD,holidays = hol_list)).date():
                cnt = LD
                flg = LD
                rlcnt +=1
    
            if (run_date not in hol_list) and (run_date >= stdt):
                try :                
                    dts.append(run_date)
                    ro.append(dfRO.loc[run_date].RO)
                    ri.append(dfRI.loc[run_date].RI)
                    pro.append(dfRO.loc[run_date].PRO)
                    pri.append(dfRI.loc[run_date].PRI)
                    rlflg.append(flg)
                except:
                    print("Data issue on",str(run_date))
                    print(dts,ro,ri,pro,pri)
                    run_date += pof.CustomBusinessDay(1,holidays = hol_list)
                    run_date = run_date.date()
                    continue
                if typ == 0:
                    rol_date = rollDates.loc[ro[-1]]
                else:
                    while run_date > rollDates[srl].date():
                        srl+=1
                    rol_date = rollDates[srl].date()
                    ltd_prvDay = rol_date
  
                if run_date == stdt:
                    idx.append(intlvl)
                    ltd_prvDay = rol_date
                    ltd.append(ltd_prvDay)
                    if (cnt > 0):
                        uro.append(0)
                        uri.append(idx[-1]/dfRI.loc[run_date].PRI)       
                    else :
                        uro.append(idx[-1]/dfRO.loc[run_date].PRO)
                        uri.append(0)
                    rlcnt = 0
                    
                else:
                    if dts[-2] == ltd_prvDay:
                        idx.append(idx[-1]+uro[-1]*(dfRO.loc[run_date].PRO-dfRI.loc[dts[-2]].PRI)+uri[-1]*(dfRI.loc[run_date].PRI-dfRI.loc[dts[-2]].PRI))
                        ltd_prvDay = rol_date
                        ltd.append(ltd_prvDay)
        
                       
                    else:
                        idx.append(idx[-1]+uro[-1]*(dfRO.loc[run_date].PRO-dfRO.loc[dts[-2]].PRO)+uri[-1]*(dfRI.loc[run_date].PRI - dfRI.loc[dts[-2]].PRI))
                        ltd.append(ltd[-1])
                    u1,u2 = units(rlamt,uri[-1],uro[-1],cnt,idx[-1],dfRI.loc[run_date].PRI,dfRO.loc[run_date].PRO,LD)
                    uri.append(u1)
                    uro.append(u2)
            idxprd.append(cnt)
            cnt = reduce1(cnt)
            flg = reduce2(flg)
            run_date += pof.CustomBusinessDay(1,holidays = hol_list)
            run_date = run_date.date()
#    y = time.time()
#        except:
#            print("Error on ", str(run_date))
#            run_date += pof.CustomBusinessDay(1,holidays = hol_list)
#            run_date = run_date.date(
        except:
            print(len(dts),"\t",len(ro),"\t",len(idx),"\t",len(uri),"\t",len(uro))
            break
        
    
    fdf = pd.DataFrame()
    fdf = pd.DataFrame(index=dts)
    fdf["Contract_RO"] = ro
    fdf["Contract_RI"] = ri
    fdf["Price_RO"] = pro
    fdf["Price_RI"] = pri
    fdf["Roll_Flag"] = rlflg
    fdf["Units_RO"] = uro
    fdf["Units_RI"] = uri
    fdf["ICL"] = idx
    
    return fdf



##params = [idxTicker,stDate,EndDate,Underlying,Generic1,2,]
    
def setData(params,tables,extras,rldts):


    
    index = params[0] 
    stdt = params[1].date()
    endt = params[2].date()
    typ = 0
    
    if tables[0] == 1: 
        idx_data = db.getIndexData(index)
        generics = db.getRollSchedule(index).User_Selection[0]
        ro_data = db.getPrices(idx_data.Underlying[0]+generics.split("-")[0])
        ro_data.columns = ["RO","PRO"]
        ri_data = db.getPrices(idx_data.Underlying[0]+generics.split("-")[1])
        ri_data.columns = ["RI","PRI"]
        hlds = db.getHolidays(index)
        LD = idx_data.Lead_Days[0]
        rldts = db.getRolldates(idx_data.Underlying[0])    
        rlamt = [float(Fraction(i)) for i in idx_data.Roll_Amount[0].split(",")]        
        
        df = Calculate(stdt,endt,LD,ri_data,ro_data,hlds,rldts,rlamt,typ)
   
    
    
    

    if params[8] is False:
        typ = 1

    if params[10] is True:
        
#        if sum(tables) == 4:

        if tables[3] == 1 & tables[1] == 1:
            ro_data = db.getPrices(params[3]+str(params[4]))
            ro_data.columns = ["RO","PRO"]
            ri_data = db.getPrices(params[3]+str(params[5]))
            ri_data.columns = ["RI","PRI"]
            hlds = db.getHolidays(index)
            LD = int(params[8])
            rlamt = [float(Fraction(i)) for i in params[9].split(",")]
            df = Calculate(stdt,endt,LD,ri_data,ro_data,hlds,rldts,rlamt,typ)

        else:
            print("Check for required data.")
    elif params[10] is False:
        ro_data, ri_data, rldts, hlds = getData(extras[0])
        LD = int(params[8])
        rlamt = [float(Fraction(i)) for i in params[9].split(",")]
        df = Calculate(stdt,endt,LD,ri_data,ro_data,hlds,rldts,rlamt,typ)
      
        

    if extras[1] is not True:
        if str(extras[1]).replace(" ","") == "":
            df.to_csv(index+" "+str(datetime.datetime.today().date())+".csv")
        else:
            df.to_csv(extras[1].strip(".csv")+".csv")
    print("Run complete")