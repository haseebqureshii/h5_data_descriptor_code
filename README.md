# Melt-Pool-Kinetics Dataset Inventory Toolkit

Lightweight Python tooling to inspect a large Melt-Pool-Kinetics HDF5 dataset and generate static + interactive metadata dashboards.

This project currently includes:
- HDF5 structure exploration and sample frame export
- Source-level dashboard generation from metadata (`.xlsx` or `.csv`)
- Interactive topology views (Treemap + Parallel Categories)
- A simple HTML page that embeds interactive chart fragments

## Project Layout

- `dataset_inventory_dashboard.py`: Main analytics pipeline for metadata summaries and visual outputs
- `explorer.py`: HDF5 explorer that prints dataset hierarchy and exports sample frames
- `browser.py`: Utility to list/select HDF5 datasets and preview frames interactively
- `index.html`: Presentation page embedding generated Plotly fragments
- `requirements.txt`: Python dependencies
- Generated outputs:
  - `dataset_inventory_dashboard.png`
  - `dataset_topology_treemap.html`
  - `dataset_topology_parallel_categories.html`
  - `treemap.html`
  - `parallel.html`
  - `h5_preview_samples.png`

## Requirements

- Python 3.10+ (recommended: local virtual environment)
- Dataset files available locally:
  - HDF5 file (example: `Final_DatasetV3.h5`)
  - Metadata file (example: `Metadata Revised.xlsx`)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Generate metadata dashboard + topology plots

```powershell
.\.venv\Scripts\python.exe dataset_inventory_dashboard.py
```

Outputs are written to the current working directory:
- `dataset_inventory_dashboard.png`
- `dataset_topology_treemap.html`
- `dataset_topology_parallel_categories.html`
- `treemap.html` (embedded fragment)
- `parallel.html` (embedded fragment)

### 3. Explore the HDF5 file structure and sample frames

```powershell
.\.venv\Scripts\python.exe explorer.py
```

Output:
- `h5_preview_samples.png`

## How the Dashboard Script Works

`dataset_inventory_dashboard.py` performs two stages:

1. Metadata summary and static charts
- Loads metadata from `.xlsx/.xls` (via `pandas.read_excel`) or `.csv` (via `pandas.read_csv`)
- Aggregates frame counts (`DataSize`) per source
- Produces a static multi-panel PNG dashboard

2. Interactive topology views
- Treemap by `MaterialName -> AMSystemType -> Source`
- Parallel categories by `MaterialName`, `AMSystemType`, `AMInsituDataSensorType`
- Saves full interactive HTML files and lightweight iframe-ready fragments

## Data Assumptions

The metadata table is expected to include at least:
- `AMInsituDataID`
- `DataSize`
- `MaterialName`
- `AMSystemType`
- `AMInsituDataSensorType`

The HDF5 explorer expects image-like datasets with shape:
- `(frames, height, width)` or
- `(height, width)`

## Viewing the Web Dashboard

`index.html` embeds:
- `treemap.html`
- `parallel.html`

Open `index.html` in a browser after running `dataset_inventory_dashboard.py` so the embedded chart fragments exist.

## Common Troubleshooting

### `ModuleNotFoundError: No module named 'pandas'` (or similar)
You are likely using a different Python interpreter than the one where dependencies were installed.

Use the project virtual environment explicitly:

```powershell
.\.venv\Scripts\python.exe dataset_inventory_dashboard.py
```

### Excel file decode/parser errors
If your metadata is `.xlsx`, do not use CSV loading. This repo already auto-detects Excel extensions and requires `openpyxl`.

Verify:

```powershell
.\.venv\Scripts\python.exe -m pip show openpyxl
```

### Plotly `parallel_categories(... got unexpected keyword argument ...)`
This can happen across Plotly versions. The project uses `go.Parcats` for compatibility.

### Matplotlib/Tk GUI errors in headless or restricted environments
Scripts use a non-GUI backend (`Agg`) and save figures directly to files.

## Notes

- Current scripts use absolute local paths in their `__main__` blocks. Update those paths for your machine if needed.
- Generated files can be large; keep only the artifacts you need for sharing.

## License

No explicit license file is currently included in this folder. Add one if you plan to distribute the code publicly.
