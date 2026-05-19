# sdss_manager/__init__.py

# Expose the main classes
from .downloader import SDSSDownloader
from .indexer import SDSSIndexer
from .core import SDSSDatabase

# Package metadata
__version__ = "0.1.0"
__author__ = "Adhyatma Rajan"

# Control what gets imported with "from sdss_manager import *"
__all__ = ["SDSSDownloader", "SDSSIndexer", "SDSSDatabase"]
