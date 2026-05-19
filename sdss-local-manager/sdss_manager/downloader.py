import subprocess
import os

class SDSSDownloader:
    def __init__(self, local_base_dir):
        self.local_base_dir = local_base_dir
        os.makedirs(local_base_dir, exist_ok=True)
        
    def sync_spectro_data(self, data_release="dr19", plate_folder="v6_1_3"):
        """Syncs specific BOSS spectro data via the public SDSS rsync mirror."""
        # SDSS public data mirror path structure
        remote_url = f"rsync://dtn.sdss.org/{data_release}/spectro/boss/redux/{plate_folder}/"
        
        # Rsync flags: -a (archive mode), -v (verbose), -z (compress), --progress
        # --update ensures you only fetch newer/missing files
        command = [
            "rsync", "-avz", "--update", "--progress",
            remote_url,
            self.local_base_dir
        ]
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        print("Syncing with SDSS Server live...")
        # Print each line of rsync output as it happens
        for line in process.stdout:
            if "to-check" in line or "🚀" in line:  # clean up the spam, show progress
                print(line.strip(), end="\r")

        process.wait()
        print("\nSync complete!")
