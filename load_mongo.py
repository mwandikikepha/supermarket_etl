import pandas as pd
from pymongo import MongoClient
from extract import extract_data
from load import postgres_load
import os
from dotenv import load_dotenv

load_dotenv()

def load_to_mongo(df):
    print("Loading to MongoDB...")
    
    try:
        
        MONGO_URL = os.getenv('MONGO_URL')
        client = MongoClient(MONGO_URL)
        
        
        db = client['supermarket_db']
        collection = db['transactions']
        
        # Convert DataFrame to dictionary 
        records = df.to_dict('records')
        
        # Clear existing data and insert new
        collection.delete_many({})
        result = collection.insert_many(records)
        
        print(f"MongoDB: Loaded {len(result.inserted_ids)} documents")
        
    except Exception as e:
        print(f"MongoDB Error: {e}")
        raise
        
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    print("Extracting data...")
    df = extract_data()
    print(f"{len(df)} rows extracted\n")
    
    # Load to BOTH databases
    postgres_load(df) 
    print()
    load_to_mongo(df)    
    
    print("\n ETL Complete! Data loaded to both databases.")