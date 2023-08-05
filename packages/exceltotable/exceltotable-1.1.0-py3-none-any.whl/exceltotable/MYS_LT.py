import os
#更改列错位，修改页为sheet1
from datetime import datetime

import pandas as pd
import numpy as np

Frontier_BrandCode_mapping = {'EL': '01', 'CL': '03', 'CM': '10', 'BB': '11', 'OR': '07', 'JM': '17', 'DA': '22',
                              'TF': '26', 'CS': '99', 'MC': '12', 'AV': '21', 'TO': '41', 'KL': '38', 'GG': '35','LL':'37',
                              'AR': '02', 'MACCN': '12'}

Frontier_Market_mapping = {'TW': 'TWN', 'HK': 'HKG', 'AU': 'AUS', 'NZ': 'NZL', 'SG': 'SGP'}


def __get_sourcefile():
    FILE_PATH_DB1 = '/Users/abocide/Downloads/ChecksumFile/DB1File/MYS/apac_mys_lt.csv'
    col_names = ['AsOfMonth(LoyaltyTransactionTimestamp)', 'CLTN_MarketCode', 'CSLS_BrandCode',
'CLSP_LoyaltyProgramID', 'CLTN_LoyaltyTransactionTypeCode', 'count(1)', 'count(distinct CLTN_LoyaltyTransactionID)',
                 'count(distinct CLTN_TransactionInvoiceNum)', 'count(distinct CLTN_LoyaltyAccountID)', 'count(distinct CLTN_ConsumerID)','sum(CLTN_LoyaltyPoints)']
    df_source = pd.DataFrame(columns=col_names)
    df_source_tmp = pd.read_csv(FILE_PATH_DB1,index_col=False,delimiter=',')
    df_source["AsOfMonth(LoyaltyTransactionTimestamp)"] = pd.to_datetime(df_source["AsOfMonth(LoyaltyTransactionTimestamp)"], format='%d-%b-%Y')
    df_source["CLTN_MarketCode"] = df_source["CLTN_MarketCode"].map(Frontier_Market_mapping)
    df_source["CSLS_BrandCode"] = df_source["CSLS_BrandCode"].map(Frontier_BrandCode_mapping)
    df_source['CSLS_BrandCode'] = df_source['CSLS_BrandCode'].astype(int)
    df_source = df_source[df_source["CSLS_BrandCode"] != 99]
    df_db1 = pd.read_csv(FILE_PATH_DB1)
    df_db1["AsOfDate"] = pd.to_datetime(df_db1["AsOfDate"], format='%Y-%m-%d')
    df_db1['BrandCode'] = df_db1['BrandCode'].astype(int)
    df_merged = pd.merge(df_source, df_db1, left_on=['AsOfMonth(LoyaltyTransactionTimestamp)', 'CLTN_MarketCode', 'CSLS_BrandCode',
                                                     'CLTN_LoyaltyTransactionTypeCode'], right_on=['AsOfDate', 'MarketCode', 'BrandCode', 'LoyaltyTransactionTypeCode'], how='left').fillna(0)
    df_merged["LoyaltyTransactionId_Gap"] = df_merged["LoyaltyTransactionID_x"] - df_merged["LoyaltyTransactionID_y"]
    df_merged["Points_Gap"] = df_merged["Points_x"] - df_merged["Points_y"]

    df_result = df_merged[["TransactionDate", "MarketCode", "BrandCode", "LoyaltyTransactionID_x",
                           "LoyaltyTransactionID_y", "LoyaltyTransactionId_Gap", "Points_x", "Points_y", "Points_Gap"]]
    df_summary = df_result[["TransactionDate", "MarketCode", "LoyaltyTransactionID_x", "LoyaltyTransactionID_y",
                            "LoyaltyTransactionId_Gap"]].copy()
    df_summary["Year"] = df_summary["TransactionDate"].dt.year
    df_summary["Month"] = df_summary["TransactionDate"].dt.month
    df = df_summary.groupby(["Year", "Month", "MarketCode"]).agg([np.sum])
    df["Percentage"] = df["LoyaltyTransactionId_Gap"] / df["LoyaltyTransactionID_x"]
    with pd.ExcelWriter('/Users/abocide/Downloads/ChecksumFile/result/LT_MYS.xlsx') as writer:
        df_result.to_excel(writer, sheet_name='df_result', index=False)
        df.to_excel(writer, sheet_name='df')


__get_sourcefile()
