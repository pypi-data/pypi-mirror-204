import pandas as pd
import mysql.connector as msql
from sqlalchemy import create_engine, types
import sys
import argparse
parser = argparse.ArgumentParser(description='Show top lines from each file')
parser.add_argument('filepath',type=str,help='enter the table name you want to generate')
args = parser.parse_args()
print(args)
df = pd.read_excel(args.filepath,sheet_name='Sheet2' ,index_col=False)
engine = create_engine('mysql+pymysql://root:Lly486597@localhost/loyalty') # enter your password and database names here
df.to_sql(args.filepath.split('/')[-1].split('.')[0],con=engine,index=False,if_exists='replace') # Replace Table_name with your sql table name
