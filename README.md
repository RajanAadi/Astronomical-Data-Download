# Astronomical-Data-Download

A highly optimized, object-oriented Python pipeline designed to automate the synchronization, streaming, and indexing of massive astronomical data releases. 

Currently implemented for the **Sloan Digital Sky Survey (SDSS)**, this project serves as a foundational architecture to programmatically handle and normalize heterogeneous astronomical archives without memory bottlenecks or file I/O crashes.

---

## 🌌 Project Vision & Roadmap

This repository is built with scalability in mind. While the current release handles SDSS spectro/photometric data via Rsync and FITS headers, the core retrieval and indexing layers are designed to be dataset-agnostic. 

**Upcoming Integrations:**
* **Gaia Archive:** Implementing TAP (Table Access Protocol) and Astroquery integrations for billion-star astrometric queries.
* **Kepler / TESS:** Automating time-series light curve retrievals via the MAST server APIs.
* **JWST / Hubble:** Integrating robust AWS S3 / cloud-native data streaming for public space telescope pipelines.
* **Distributed Pipelines:** Expanding the sync layer to optionally utilize the Globus SDK for multi-terabyte cluster transfers.

---

## 🚀 Key Features & Engineering

* **Streaming File Discovery:** Utilizes `pathlib.rglob` generators instead of in-memory arrays to instantly process multi-terabyte directory trees without freezing.
* **High-Speed Relational Indexing:** Bypasses standard SQLite disk-flush waits using `PRAGMA` memory-buffered journaling and batch commits, extracting FITS metadata into queryable catalogs in seconds.
* **Unbuffered Network Synchronization:** Wraps native `rsync` processes directly to the system terminal to ensure maximum unthrottled network bandwidth during large data pulls.
* **Jupyter-Ready:** Includes a clean, object-oriented Python API that easily integrates into Pandas and Matplotlib workflows for instant data visualization.

---

## 📦 Installation & Setup

### Prerequisites
* Python 3.8+
* `rsync` installed on your system (native on Linux/macOS; use WSL or Git Bash on Windows)