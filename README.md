# 3D Tiles Height Aligner

A lightweight Python utility designed to adjust the vertical alignment of OGC 3D Tilesets (`tileset.json`). This tool is particularly useful when 3D models (like photogrammetry or BIM) appear floating or buried compared to the ground level in viewers like CesiumJS.

## Features

- **Automatic Extraction**: Reads ECEF coordinates directly from the tileset's root bounding volume.
- **Geodetic Conversion**: Converts coordinates between EPSG:4978 (ECEF) and EPSG:4326 (WGS84) to accurately calculate height.
- **Transformation Matrix**: Applies a precise translation matrix to the root of the tileset to adjust its altitude.
- **Manual Override**: Option to specify a custom target height.

## Prerequisites

- Python 3.13 or higher.
- A virtual environment (recommended).

## Installation

1. **Clone or download** this repository to your local machine.

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   The tool relies on `numpy` and `pyproj`. Install them using the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The script takes the path to your `tileset.json` as a mandatory argument. It will generate a new file named `[original_name]_aligned.json`.

### Basic Alignment (Automatic)
To align the tileset based on its internal coordinates:
```bash
python 3dtiles_height_aligner.py path/to/tileset.json
```