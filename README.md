# Supermarket ETL Pipeline

An automated ETL (Extract, Transform, Load) pipeline that extracts supermarket transaction data from Google Sheets, cleans and validates it, then loads it into both PostgreSQL and MongoDB databases.

##  Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Data Schema](#data-schema)
- [Tech Stack](#tech-stack)

##  Features

- **Extract**: Pulls data from Google Sheets using Google Sheets API
- **Transform**: 
  - Removes duplicate records based on transaction ID
  - Filters out invalid data (negative quantities/amounts)
  - Handles missing values
  - Data type validation
- **Load**: 
  - PostgreSQL: Uses COPY command for fast bulk inserts
  - MongoDB: Stores as JSON documents for flexible querying
- **Dual Database Support**: Load to PostgreSQL, MongoDB, or both simultaneously

##  Project Structure
```
supermarket/
├── extract.py                        
├── load.py                          
├── load_mongo.py                   
├── supermarket-credentials.json     
├── .gitignore                       
├── .env                            
└── README.md                     
```

##  Prerequisites

- Python 3.8+
- PostgreSQL database (cloud or local)
- MongoDB database (cloud or local)
- Google Sheets API credentials
- Google Sheet with transaction data

##  Installation

1. **Clone the repository:**
```bash
git clone https://github.com/mwandikikepha/supermarket_etl.git
cd supermarket_etl
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install pandas gspread oauth2client gspread-dataframe psycopg2-binary pymongo python-dotenv
```

##  Configuration

### 1. Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API
4. Create service account credentials
5. Download JSON credentials and save as `supermarket-credentials.json`
6. Share your Google Sheet with the service account email

### 2. Environment Variables

Create a `.env` file in the project root:
```env
# PostgreSQL Configuration
POSTGRES_HOST=your-postgres-host.com
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

# MongoDB Configuration
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/?appName=YourApp

# Google Sheets
SHEET_ID=your_google_sheet_id
```

##  Usage

### Load to PostgreSQL only:
```bash
python load.py
```

### Load to MongoDB only:
```bash
python load_mongo.py
```

### Load to both databases:
```bash
python load_mongo.py
```
*(The mongo script imports and calls the PostgreSQL loader)*

### Expected Output:
![ETL Pipeline Output](https://i.imgur.com/db0eSd8.png)

```
 Extracting data...
 50783 rows extracted

 Loading to PostgreSQL...
 PostgreSQL: Loaded 50783 rows

 Loading to MongoDB...
 MongoDB: Loaded 50783 documents

 ETL Complete! Data loaded to both databases.
```

##  Data Schema

### Source Data (Google Sheets)
| Column | Type | Description |
|--------|------|-------------|
| id | String | Unique transaction identifier |
| quantity | Integer | Number of items purchased |
| product_name | String | Name of the product |
| total_amount | Float | Total transaction amount |
| payment_method | String | Payment type (cash, card, etc.) |
| customer_type | String | Customer category (member, gold, etc.) |

### PostgreSQL Table Structure
```sql
CREATE TABLE supermarket_transactions (
    id VARCHAR(255) PRIMARY KEY,
    quantity INTEGER,
    product_name VARCHAR(255),
    total_amount FLOAT,
    payment_method VARCHAR(100),
    customer_type VARCHAR(100)
);
```

### MongoDB Collection Structure
```json
{
  "_id": ObjectId("..."),
  "id": "47d54138-a950-4ec0-9d4a-e637e8dfb290",
  "quantity": 10,
  "product_name": "Product A",
  "total_amount": 150.50,
  "payment_method": "cash",
  "customer_type": "non-member"
}
```

##  Tech Stack

- **Python 3.12**: Core programming language
- **pandas**: Data manipulation and transformation
- **gspread**: Google Sheets API client
- **psycopg2**: PostgreSQL database adapter
- **pymongo**: MongoDB driver
- **PostgreSQL**: Relational database for structured queries
- **MongoDB**: NoSQL database for flexible document storage

##  Performance

- **Extraction**: ~50,000 rows in 2-3 seconds
- **PostgreSQL Load**: Uses COPY command for bulk insert (~1 second for 50k rows)
- **MongoDB Load**: Bulk insert with batch processing (~2 seconds for 50k rows)
- **Total Pipeline**: Approximately 5-8 seconds end-to-end


##  Author

**Kepha Mwandiki - Data Engineer**
- GitHub: [@mwandikikepha](https://github.com/mwandikikepha)

