import subprocess
import os

class SDSSDownloader:
    def __init__(self, local_base_dir):
        self.local_base_dir = local_base_dir
        os.makedirs(local_base_dir, exist_ok=True)
        
    def sync_spectro_data(self, data_release="dr19", plate_folder="v6_1_3"):
        remote_url = f"rsync://dtn.sdss.org/{data_release}/spectro/boss/redux/{plate_folder}/"

        # We remove --progress to stop rsync from generating millions of lines of text,
        # but keep -v (verbose) so we know what's happening.
        command = ["rsync", "-avz", "--update", remote_url, self.local_base_dir]

        print("Connecting to SDSS Server and syncing files...")
        print(f"Source: {remote_url}")
        print("This will run silently in the background until completion.")

        # By NOT capturing stdout, Python passes the execution directly to the system.
        # It will block here safely, downloading at maximum hardware speed without buffering bugs.
        result = subprocess.run(command, capture_output=False, text=True)

        if result.returncode == 0:
            print("\nSync complete and up to date!")
        else:
            print("\nSync encountered an error or was interrupted.")