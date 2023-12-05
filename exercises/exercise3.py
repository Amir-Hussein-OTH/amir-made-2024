import pandas as pd
from pandas import DataFrame
import sqlalchemy

# Global variables for source URL and database table name
SOURCE_URL = 'https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv'
TABLE_NAME = 'cars'


# Function to read CSV data from the specified source URL
def read_csv(source: str):
    use_columns = [0, 1, 2, 12, 22, 32, 42, 52, 62, 72]
    return pd.read_csv(source, sep=';', on_bad_lines='skip', encoding='latin1', skiprows=6, skipfooter=4,
                       usecols=use_columns, engine='python', index_col=False)


# Function to rename columns in the DataFrame for clarity
def rename_columns(df: DataFrame):
    column_names = ['date', 'CIN', 'name', 'petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']
    df.columns = column_names
    return df


# Function to drop invalid rows based on CIN length and non-negative values for specified columns
def drop_invalid_rows(df: DataFrame):
    df['CIN'] = df['CIN'].astype(str).apply(lambda x: '0' + x if len(x) == 4 else x)
    df = df[df['CIN'].str.len() == 5]
    for col in df.columns.tolist()[3:]:
        df = df[df[col].replace("-", "-1").astype(int) > 0]
    return df


# Function to save the DataFrame into an SQLite database with specified database name, table name, and data types
def save_in_db(df: DataFrame, db_name: str, table_name: str, d_types: dict):
    df.to_sql(table_name, 'sqlite:///' + db_name, if_exists='replace', index=False, dtype=d_types)


# Function to get data types for each column in the DataFrame
def get_dtypes(df: DataFrame):
    meta_data = list(df)
    sql_dtypes = [sqlalchemy.TEXT()] * 3 + [sqlalchemy.INTEGER()] * 7
    return dict(zip(meta_data, sql_dtypes))


# Main function to execute the data processing pipeline
def execute_pipeline():
    df = read_csv(SOURCE_URL)
    df = rename_columns(df)
    df = drop_invalid_rows(df)
    db_name = TABLE_NAME + '.sqlite'
    table_name = TABLE_NAME
    d_types = get_dtypes(df)
    print(df)
    save_in_db(df, db_name, table_name, d_types)


# Entry point of the script
if __name__ == '__main__':
    execute_pipeline()
