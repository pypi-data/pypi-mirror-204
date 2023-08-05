import pandas as pd
import mysql.connector as msql
from sqlalchemy import create_engine, types
import sys
import argparse
class filetodb:
  parser = argparse.ArgumentParser(description='Show top lines from each file')
  parser.add_argument('filepath',type=str,help='enter the table name you want to generate')
  parser.add_argument('database',type=str,help='enter the database')
  args = parser.parse_args()
  print(args)
  df = pd.read_csv(args.filepath,index_col=False,delimiter=',')
  engine = create_engine('mysql+pymysql://root:Lly486597@localhost/'+args.database) # enter your password and database names here
  df.to_sql(args.filepath.split('/')[-1].split('.')[0],con=engine,index=False,if_exists='replace') # Replace Table_name with your sql table name
