import sqlite3
from astropy.io.fits import open as open_fits
from pathlib import Path
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
        print("Scanning directory structure...")

        # 1. Use Pathlib to scan files streamingly
        path_object = Path(search_directory)
        # rglob returns a generator, which doesn't choke your memory or disk
        fits_generator = path_object.rglob("*.fits")

        # 2. Since generators don't have a pre-calculated length,
        # we manually update tqdm so it starts ticking immediately.
        progress_bar = tqdm(desc="Parsing FITS Headers", unit=" files")

        # 3. Optimize SQLite by turning off safety features temporarily for speed
        self.cursor.execute("PRAGMA synchronous = OFF")
        self.cursor.execute("PRAGMA journal_mode = MEMORY")

        batch_size = 1000
        current_batch = 0

        for path in fits_generator:
            # Convert Path object to string for the database
            file_path_str = str(path)

            try:
                with open_fits(file_path_str) as hdul:
                    header = hdul[0].header
                    ra = header.get("RA", None)
                    dec = header.get("DEC", None)
                    exp = header.get("EXPTIME", None)

                    self.cursor.execute(
                        """
                        INSERT OR IGNORE INTO observations (file_path, ra, dec, exposure_time)
                        VALUES (?, ?, ?, ?)
                    """,
                        (file_path_str, ra, dec, exp),
                    )

                    current_batch += 1

            except Exception:
                # Safely skip corrupt files without crashing the pipeline
                continue

            finally:
                progress_bar.update(1)

            # Commit to disk in batches of 1,000 so the database stays fast
            if current_batch >= batch_size:
                self.conn.commit()
                current_batch = 0

        # Final commit for any remaining files
        self.conn.commit()
        progress_bar.close()
        print("\nDatabase indexing finished!")