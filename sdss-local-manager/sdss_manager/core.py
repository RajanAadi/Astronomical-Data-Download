import pandas as pd
import sqlite3
from .downloader import SDSSDownloader
from .indexer import SDSSIndexer

class SDSSDatabase:
    def __init__(self, local_base_dir, db_path="sdss_metadata.db"):
        self.downloader = SDSSDownloader(local_base_dir)
        self.indexer = SDSSIndexer(db_path)
        self.db_path = db_path

    def update_database(self):
        """One command to rule them all: syncs data and updates indices."""
        self.downloader.sync_spectro_data()
        self.indexer.index_new_files(self.downloader.local_base_dir)

    def get_catalog(self):
        """Returns all readable metadata instantly as a Pandas DataFrame."""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM observations"
        # Reading SQL results cleanly into Pandas allows for beautiful table displays
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df