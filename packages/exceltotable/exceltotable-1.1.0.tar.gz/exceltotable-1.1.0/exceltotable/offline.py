import pandas as pd
import mysql.connector as msql
from sqlalchemy import create_engine, types
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Show top lines from each file')
parser.add_argument('path',type=str,help='enter the path you want to generate')
parser.add_argument('database',type=str,help='enter the database')
args = parser.parse_args()
engine = create_engine('mysql+pymysql://root:Lly486597@localhost/'+args.database) # enter your password and database names here
print(args)
for root,d_names,f_names in os.walk(args.path):
  for filename in f_names:
    f = os.path.join(root, filename)
    print(f)
    if("_2023" in f and ".xls" in f): 
      df = pd.read_excel(f,index_col=False)
      df.to_sql(filename.split('_2023')[0],con=engine,index=False,if_exists='append')   
      continue
    if(" 2023" in f): 
      df = pd.read_excel(f,index_col=False)
      df.to_sql(filename.split(' 2023')[0],con=engine,index=False,if_exists='append') 
      continue 
    if("_2023" in f and ".csv" in f): 
      df = pd.read_csv(f,index_col=False,delimiter=',')
      df.to_sql(filename.split('.')[0],con=engine,index=False,if_exists='append')  
    if(".xls" in f): 
      df = pd.read_excel(f,index_col=False)
      df.to_sql(filename.split('.')[0],con=engine,index=False,if_exists='append')  
      continue
    if(".csv" in f): 
      df = pd.read_csv(f,index_col=False,delimiter=',')
      df.to_sql(filename.split('.')[0],con=engine,index=False,if_exists='append')  
      continue


