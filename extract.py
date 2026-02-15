import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe

JSON_KEY_FILE = 'supermarket-credentials.json'  
SHEET_ID = '1CHSfRQTla3Kkang7E_PptCKc6WYMIlzwDoe_hgMMajE' 

def extract_data():
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(SHEET_ID)
    worksheet = sheet.get_worksheet(0)
    
    df = get_as_dataframe(worksheet, evaluate_formulas=True, parse_dates=True)
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    required_cols = ['id', 'quantity', 'product_name', 'total_amount', 'payment_method', 'customer_type']
    clean_df = df[required_cols].copy()

    clean_df = clean_df.drop_duplicates(subset='id')

    clean_df = clean_df[clean_df['quantity'] > 0]

    clean_df = clean_df[clean_df['total_amount'] > 0]

    clean_df = clean_df.dropna()

    clean_df = clean_df.reset_index(drop=True)
    return clean_df

finaldf = extract_data()
print(finaldf.head())