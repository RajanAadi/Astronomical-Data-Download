import sqlite3
from astropy.io.fits import open as open_fits
import glob
from tqdm import tqdm

class SDSSIndexer:
    def __init__(self, db_path="sdss_metadata.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
        
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE,
                ra REAL,
                dec REAL,
                exposure_time REAL,
                target_mag REAL
            )
        ''')
        self.conn.commit()

    def index_new_files(self, search_directory):
        """Scans folder for FITS files, extracts headers, saves to SQL."""
        fits_files = glob.glob(f"{search_directory}/**/*.fits", recursive=True)
        
        print(f"Found {len(fits_files)} files. Indexing metadata...")

        # Wrapping the list in tqdm() creates a live progress bar!
        for path in tqdm(fits_files, desc="Parsing FITS Headers"):
            try:
                with open_fits(path) as hdul:
                    header = hdul[0].header
                    ra = header.get("RA", None)
                    dec = header.get("DEC", None)
                    exp = header.get("EXPTIME", None)

                    self.cursor.execute(
                        """
                        INSERT OR IGNORE INTO observations (file_path, ra, dec, exposure_time)
                        VALUES (?, ?, ?, ?)
                    """,
                        (path, ra, dec, exp),
                    )
            except Exception:
                continue

        self.conn.commit()
