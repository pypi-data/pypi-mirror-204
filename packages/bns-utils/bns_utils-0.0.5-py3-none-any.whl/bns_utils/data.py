import pyodbc
import pandas as pd

class IP21:
    def __init__(self,host,port,ads='MINPRO'):
        self.host = host
        self.port = port
        self.ads = ads
        self.connnection_string = f"DRIVER={{AspenTech SQLplus}};HOST={host};PORT={port};ADS={ads};TIMEOUT=;MAXROWS=1000000;TABLE=;CHARINT=Y;CHARFLOAT=N;CHARTIME=Y;READONLY=N;ALLFIELDS=N;ROWID=N;CONVERTERRORS=Y;CHARISNULL=Y;TIBCO=N;"

    def tag_dump(self,write_csv=True):
        cnxn = pyodbc.connect(self.connnection_string)
        queryString = f"SELECT NAME WIDTH 255, IP_DESCRIPTION FROM IP_AnalogDef UNION SELECT NAME WIDTH 255, IP_DESCRIPTION FROM IP_DiscreteDef;"
        df = pd.read_sql(queryString,cnxn)
        try:
            if write_csv:
                df.to_csv('tag_dump.csv',index=False)
            return df.values.to_list()
        except Exception as e:
            print(e)
    
    #Date Format: "16-Feb-23 09:00:00"
    #Interval Format: "00:00:01"
    def tag_data(self,tag_list,start,end,freq,separate=True,file_type='ftr'):
        if file_type != 'ftr' and file_type != 'csv':
            raise ValueError(f"Invalid file type {file_type}, use ftr or csv")
        is_first =True
        cnxn = pyodbc.connect(self.connnection_string)
        for tag in tag_list:
            queryString = f"Select TS, Value from History Where name = '{tag}' and TS Between '{start}' and '{end}' And Period = {freq};"
            df = pd.read_sql(queryString,cnxn)
            if is_first and not(separate):
                df_all = df
            if separate:
                try:
                    if file_type == 'ftr':
                        df.to_feather(tag+'.ftr')
                    elif file_type == 'csv':
                        df.to_csv(tag+'.csv',index=False)                   
                except Exception as e:
                    raise IOError("Cannot write file: "+ e)
            elif not(is_first) and not(separate):
                df_all = df_all.merge(df,how="left",on="TS")
        if not(separate):
            try:
                if file_type == 'ftr':
                    df_all.to_feather(tag+'.ftr')
                elif file_type == 'csv':
                    df_all.to_csv(tag+'.csv',index=False)                  
            except Exception as e:
                raise IOError("Cannot write file: "+ e)

#class BNSHistorian:
#    def __init__(self,host,port,ads='MINPRO'):
#        self.host = host
#        self.port = port
#        self.ads = ads
#        self.connnection_string = f"DRIVER={{AspenTech SQLplus}};HOST={host};PORT={port};ADS={ads};TIMEOUT=;MAXROWS=1000000;TABLE=;CHARINT=Y;CHARFLOAT=N;CHARTIME=Y;READONLY=N;ALLFIELDS=N;ROWID=N;CONVERTERRORS=Y;CHARISNULL=Y;TIBCO=N;"