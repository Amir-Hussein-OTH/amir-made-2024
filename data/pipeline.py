import os
import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
import sqlite3

# Dataset 1: Bicycle Ridership Data
url_dataset1 = 'https://opendata.muenchen.de/dataset/022a11ff-4dcb-4f03-b7dd-a6c94a094587/resource/86962013-4854-4deb-aaf9-36e3770cde24/download/rad_2012_15min_06_06_23_r.csv'

# Dataset 2: Weather Data for Munich
start_date = datetime(2012, 1, 1)
end_date = datetime(2012, 12, 31)
point = Point(48.1351, 11.5820)  # Coordinates for Munich


# Load Data for Dataset 1
def load_dataset1():
    df = pd.read_csv(url_dataset1, sep=',', dtype={'column_name': str}, low_memory=False)
    # Data Transformation for Dataset 1
    df = df.dropna(axis=0, how='all')
    df.columns = ['datum', 'uhrzeit_start', 'uhrzeit_ende', 'zaehlstelle', 'richtung_1', 'richtung_2', 'gesamt',
                  'kommentar']
    df['datum'] = pd.to_datetime(df['datum']).dt.normalize()
    df = df.groupby('datum', as_index=False).sum(numeric_only=True)
    return df


# Load Data for Dataset 2
def load_dataset2():
    data = Daily(point, start_date, end_date).fetch()
    df = pd.DataFrame(data)
    # Data Transformation for Dataset 2
    df.columns = ['temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun']
    return df


# Create SQLite Databases
def create_sqlite_databases():
    data_dir = 'data'

    # Ensure the 'data' directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Database paths
    db1_path = os.path.join(data_dir, 'dataset1.sqlite')
    db2_path = os.path.join(data_dir, 'dataset2.sqlite')

    # Check if databases exist
    if os.path.exists(db1_path):
        os.remove(db1_path)

    if os.path.exists(db2_path):
        os.remove(db2_path)

    # Create new databases
    conn1 = sqlite3.connect(db1_path)
    df1 = load_dataset1()
    df1.to_sql('dataset1', conn1, if_exists='replace', index=False)
    conn1.close()

    conn2 = sqlite3.connect(db2_path)
    df2 = load_dataset2()
    df2.to_sql('dataset2', conn2, if_exists='replace', index=False)
    conn2.close()


if __name__ == '__main__':
    create_sqlite_databases()
