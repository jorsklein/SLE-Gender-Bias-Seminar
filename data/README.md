# Data

This folder contains the cleaned metadata file used in the analysis.

The original dataset is available on GEO under accession [GSE88884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884).

Due to size and license restrictions, raw data files are not included here.

## Data Processing

The original metadata file (`GSE88884_series_matrix.txt`) was transposed using the script `src/transpose_metadata.py`.

This produced the file `GSE88884_metadata_transposed.csv`, which serves as the base for the cleaned dataset used in the analysis.

To regenerate it:
```bash
python src/transpose_metadata.py
```
