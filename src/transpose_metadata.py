"""
Utility script to transpose the original metadata file and save it as a CSV file.
"""

import pandas as pd

# === 1. Read the uncompressed GEO matrix file ===
with open("C:\\Users\\PC\\Desktop\\SLE\\GSE88884_series_matrix.txt", "r") as f:
    lines = f.readlines()

# === 2. Filter only sample metadata lines (those that start with '!Sample_') ===
sample_metadata = [line for line in lines if line.startswith("!Sample_")]

# === 3. Parse Lines into a list of rows ===
rows = []
row_names = []

for line in sample_metadata:
    parts = line.strip().split("\t")
    row_names.append(parts[0].replace("!Sample_", ""))
    rows.append(parts[1:])

# === 4. Transpose the matrix so samples are rows, and metadata types are columns ===
df = pd.DataFrame(rows, index=row_names).transpose()

# === 5. Save to CSV ===
df.to_csv("C:\\Users\\PC\\Desktop\\SLE\\GSE88884_metadata_transposed.csv", index=False)

print("File saved!")
