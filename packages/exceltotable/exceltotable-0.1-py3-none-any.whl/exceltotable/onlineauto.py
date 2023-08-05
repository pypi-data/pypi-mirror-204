import pandas as pd
import  os
import numpy as np
#read source
excelpath='/Users/abocide/Downloads/bb/outlookkpi1'
dfAll = pd.DataFrame()
for filename in os.listdir(excelpath):
  f = os.path.join(excelpath, filename)
  if os.path.isfile(f):
    dftmp = pd.read_csv(f,index_col=False,delimiter=',')
    dfAll=dfAll.append(dftmp,ignore_index=True)


df_db1 = pd.read_csv("/Users/abocide/Downloads/bb/db1/apac_trns_online.csv")
df_db1["TransactionDate"] = pd.to_datetime(df_db1["TransactionDate"], format='%Y-%m')
df_db1['Brand'] = df_db1['Brand'].astype(int)
db_select = df_db1[["TransactionDate","Market","Brand","InvoiceNum","Net_with"]].copy()
db_select["yearmon"]=db_select["TransactionDate"].dt.strftime('%Y-%m')
db_mer=db_select.groupby(["yearmon","Market","Brand"]).agg([np.sum])
print(db_select)
print(db_mer)
with pd.ExcelWriter('/Users/abocide/Downloads/result.xlsx') as wr:
  db_mer.to_excel(wr,sheet_name='sheet_one')
#dfall_merged=pd.merge(dfAll,db_mer,left_on=["Year_Month","Brand"],right_on=["k)
