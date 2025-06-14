# Source Code

This folder contains the Python scripts used for used to preprocess the data,
train Random Forest models per gender, and output performance results.

## 📄 Files

### transpose_metadata.py
Converts the original GSE88884_series_matrix.txt file into a structured CSV format.

**Input**: Raw metadata file from GEO./n
**Output**: `GSE88884_metadata_transposed.csv`

### main.py
Main script that performs gender-specific modeling using Random Forest classifiers.

**Input**: Cleaned transposed metadata file (`GSE88884_metadata_transposed_clean.csv`).
**Output**: 
- Accuracy & classification report
- Top feature barplots and CSVs
- Excel summary (`SLE_RF_summary.xlsx`)
