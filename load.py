import pandas as pd
import psycopg2
from io import StringIO
from extract import extract_data
from dotenv import load_dotenv
import os

load_dotenv()

def postgres_load(df):  
    print("Loading to PostgreSQL...")

    conn = psycopg2.connect(
        host=os.getenv('host'),
        port=os.getenv('port'),
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        sslmode=os.getenv('sslmode')
    )

    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS supermarket_transactions")
        
        cursor.execute("""
            CREATE TABLE supermarket_transactions (
                id VARCHAR(255),
                quantity INTEGER,
                product_name VARCHAR(255),
                total_amount FLOAT,
                payment_method VARCHAR(100),
                customer_type VARCHAR(100)
            )
        """)
        
        # using 'copy' for fast inserts
        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        
        cursor.copy_from(buffer, 'supermarket_transactions', sep=',', null='')
        
        conn.commit()
        print(f"PostgreSQL: Loaded {len(df)} rows to postgresql")
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Extracting data...")
    df = extract_data()
    print(f"{len(df)} rows extracted\n")
    
    postgres_load(df)
    print("\n Loading Done!")