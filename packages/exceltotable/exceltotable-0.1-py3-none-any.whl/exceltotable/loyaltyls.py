import pandas as pd
import mysql.connector as msql
from sqlalchemy import create_engine, types
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Show top lines from each file')
parser.add_argument('path',type=str,help='enter the path you want to generate')
args = parser.parse_args()
engine = create_engine('mysql+pymysql://root:Lly486597@localhost/loyaltyls') # enter your password and database names here
print(args)
for root,d_names,f_names in os.walk(args.path):
  for filename in f_names:
    f = os.path.join(root, filename)
    if(".xls" in f): 
      print(f)
      df = pd.read_excel(f,sheet_name='Sheet1' ,index_col=False)
      df.to_sql(filename.split('.')[0],con=engine,index=False,if_exists='replace') 
      continue
    if(".csv" in f): 
      print(f)
      df = pd.read_csv(f,index_col=False,delimiter=',')
      df.to_sql(filename.split('.')[0],con=engine,index=False,if_exists='replace') 



