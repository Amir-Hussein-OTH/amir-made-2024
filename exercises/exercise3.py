import pandas as pd
from sqlalchemy import create_engine

# Define the URL of the CSV data
data_url = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv"

# Read the CSV data into a DataFrame, dropping the first 6 rows and the last 4 rows, and encode with iso-8859-1 to preserve German umlauts
df = pd.read_csv(data_url, sep=";", encoding="iso-8859-1", engine="python", skiprows=6, skipfooter=4)

# Rename specific columns for clarity
df.columns = ["date", "CIN", "name", *[f"{fuel}_count" for fuel in ["petrol", "diesel", "gas", "electro", "hybrid", "plugInHybrid", "others"]]]

# Drop all other columns
keep_cols = ["date", "CIN", "name", "petrol_count", "diesel_count", "gas_count", "electro_count", "hybrid_count", "plugInHybrid_count", "others_count"]
df = df[keep_cols]

# Validate the data
# Ensure that the CIN is a string and has 5 characters (leading zeros)
df["CIN"] = df["CIN"].astype(str).str.zfill(5)

# Ensure that all other columns are positive integers greater than 0
for col in keep_cols[3:]:
    df = df[df[col] != "-"]
    df[col] = df[col].astype(int, errors="raise").dropna()
    df = df[df[col] > 0]

# Create the SQLAlchemy engine
engine = create_engine("sqlite:///cars.sqlite")

# Write the DataFrame to the SQLite database
df.to_sql("cars", engine, if_exists="replace", index=False)
