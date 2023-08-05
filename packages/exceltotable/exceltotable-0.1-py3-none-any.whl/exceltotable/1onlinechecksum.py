import pandas as pd
import mysql.connector as msql
from sqlalchemy import create_engine, types
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Show top lines from each file')
parser.add_argument('path',type=str,help='enter the path you want to generate')
args = parser.parse_args()
engine = create_engine('mysql+pymysql://root:Lly486597@localhost/onlinechecksum') # enter your password and database names here
print(args)
for filename in os.listdir(args.path):
    f = os.path.join(args.path, filename)
    # checking if it is a file
    if os.path.isfile(f):
      if(".csv" in f):
        df = pd.read_csv(f,index_col=False,delimiter=',')
        df.to_sql(filename.split('_kpi1')[0],con=engine,index=False,if_exists='append') # Replace Table_name with your sql table name
