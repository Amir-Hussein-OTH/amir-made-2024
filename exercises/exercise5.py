import zipfile
import pandas as pd
from urllib.request import urlretrieve
import sqlite3


def validate_stops(filtered_stops):
    filtered_stops['stop_name'] = filtered_stops['stop_name'].apply(
        lambda x: x.encode('latin1').decode('utf-8', 'ignore'))
    return filtered_stops[
        (-90 <= filtered_stops['stop_lat']) & (filtered_stops['stop_lat'] <= 90) &
        (-90 <= filtered_stops['stop_lon']) & (filtered_stops['stop_lon'] <= 90)
        ].dropna()


def filter_stops(stops_df):
    selected_columns = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'zone_id']
    return stops_df[selected_columns][stops_df['zone_id'] == 2001]


def load_stops_into_dataframe(stops_filename='stops.txt'):
    return pd.read_csv(stops_filename)


class GTFSDataPipeline:
    def __init__(self, gtfs_url, gtfs_zip_file='GTFS.zip', db_filename='gtfs.sqlite', table_name='stops'):
        print("Initializing GTFS Data Pipeline...")
        self.gtfs_url = gtfs_url
        self.gtfs_zip_file = gtfs_zip_file
        self.db_filename = db_filename
        self.table_name = table_name

        self.download_gtfs_data()
        self.extract_stops_from_zip()

        self.stops_df = load_stops_into_dataframe()
        self.filtered_stops = filter_stops(self.stops_df)
        self.validated_stops = validate_stops(self.filtered_stops)
        self.write_to_sqlite(self.validated_stops)

    def download_gtfs_data(self):
        print("Downloading GTFS data from:", self.gtfs_url)
        urlretrieve(self.gtfs_url, self.gtfs_zip_file)

    def extract_stops_from_zip(self, stops_filename='stops.txt'):
        print("Extracting stops from GTFS zip file...")
        with zipfile.ZipFile(self.gtfs_zip_file, 'r') as zip_ref:
            zip_ref.extract(stops_filename, '.')

    def write_to_sqlite(self, validated_stops):
        print("Writing validated stops to SQLite database...")
        db_connection = sqlite3.connect(self.db_filename)
        validated_stops.to_sql(self.table_name, db_connection, if_exists='replace', index=False)
        db_connection.close()


def main():
    gtfs_url = "https://gtfs.rhoenenergie-bus.de/GTFS.zip"
    data_pipeline = GTFSDataPipeline(gtfs_url)

if __name__ == "__main__":
    main()
