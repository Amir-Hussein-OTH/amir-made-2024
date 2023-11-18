import pandas as pd
from sqlalchemy import create_engine

# URL of the CSV data
data_url = "https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv"

# Read CSV data into a DataFrame
df = pd.read_csv(data_url, sep=";")

# Print the DataFrame content
print("DataFrame content:")
print(df)

# Create the SQLAlchemy engine
engine = create_engine("sqlite:///airports.sqlite")

# Write the DataFrame to the SQLite database
df.to_sql("airports", engine, if_exists="replace", index=False)

# Print a message indicating success
print("Data successfully loaded and written to the 'airports' table in airports.sqlite.")

