# SLE Gender Bias Analysis

This project analyzes gender bias in gene expression–based classification of Systemic Lupus Erythematosus (SLE)
using the GEO dataset [GSE88884](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE88884).

## 🎯 Goals
- Explore whether gender bias exists in gene expression–based classification of SLE.
- Compare model performance for male vs female patients.
- Identify top predictive features per gender using Random Forest classifiers.

## 🧪 What it does
- Loads and cleans metadata (from GEO dataset GSE88884)
- Separates samples by sex (male/female)
- Drops columns with >30% missing data
- Applies one-hot encoding on categorical variables
- Balances classes with SMOTE when needed
- Trains a Random Forest model for each sex group
- Evaluates using accuracy, precision, recall, and F1
- Extracts and saves top 10 most important features
- Outputs results as CSV, PNG, and Excel summary

## 📂 Input
Expected input:  
`GSE88884_metadata_transposed_clean.csv` — a cleaned, row-wise metadata file based on GEO SeriesMatrix

## 📁 Output (in `/output` folder)
- Top features per gender (CSV + PNG)
- Performance summary (Excel) — performance + top features

## 🧠 Model Configuration
- Model: `RandomForestClassifier(n_estimators=100, random_state=42)`
- Train/test split: 70/30
- Oversampling: `SMOTE(random_state=42)` (only if imbalance detected)

## 🚀 How to run
```bash
python Seminar.py
```

## 📌 Notes
- Requires pandas, numpy, matplotlib, seaborn, sklearn, imblearn, xlsxwriter
- Can be extended to support new datasets by updating the input file
- The dataset used in this project is from GEO Series GSE88884. It is not included here due to size and license considerations.

## 👩‍🔬 Created by
Jordan Klein | Open University of Israel
for a B.Sc. Bioinformatics seminar on gender bias in gene-expression-based ML models for SLE
