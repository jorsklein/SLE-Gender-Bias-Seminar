"""
Seminar Project: Gender Bias in Gene Expression-Based SLE Prediction

Author: Jordan Klein
Description: This script trains a Random Forest model on the GSE88884 dataset to
analyze gender-specific patterns in gene expression related to SLE diagnosis.
"""

import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns


# === Utility function to run model on a given CSV file ===
def run_model_on_file(filepath):
    # === 1. Load data ===
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower().str.strip()
    df = df.replace("--", np.nan)
    df['group'] = df['group'].str.strip().str.lower()
    df['sex'] = df['sex'].str.strip().str.lower()

    # === 2. Drop columns with too many missing values ===
    missing_ratio = df.isna().mean()
    df = df.loc[:, missing_ratio < 0.3]

    # === 3. Drop incomplete rows ===
    df = df.dropna(subset=['group', 'sex'])

    # === 4. Prepare output folder ===
    output_dir = "C:\\Users\\PC\\Desktop\\SLE\\output"
    os.makedirs(output_dir, exist_ok=True)

    metrics_list = []
    features_list = []
    model_info = {
        "Model": "RandomForestClassifier",
        "n_estimators": 100,
        "random_state": 42,
        "Categorical Encoding": "One-hot",
        "SMOTE": "Applied when imbalance detected",
        "Data Source": filepath
    }

    # === 5. Loop by gender ===
    for gender in ['male', 'female']:
        print(f"\n=== Gender: {gender.upper()} ===")
        sub = df[df['sex'] == gender]

        print("Group distribution:")
        print(sub['group'].value_counts())

        y = sub['group']
        drop_cols = ['geo_accession', 'sex', 'group', 'subject_id', 'title', 'description', 'source_name_ch1']
        X = sub.drop(columns=[col for col in drop_cols if col in sub.columns])
        X = pd.get_dummies(X, dummy_na=False)

        if X.empty or len(y.unique()) < 2:
            print(f"\u26a0 Not enough class variation for {gender}. Skipping.")
            continue

        if y.value_counts().min() < y.value_counts().max():
            smote = SMOTE(random_state=42)
            X, y = smote.fit_resample(X, y)
            print("✅ SMOTE applied – dataset balanced")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        print("Accuracy:", acc)
        print(classification_report(y_test, y_pred))

        metrics_list.append({
            "Gender": gender,
            "Accuracy": acc,
            "Precision_Normal": report.get("normal", {}).get("precision", None),
            "Recall_Normal": report.get("normal", {}).get("recall", None),
            "F1_Normal": report.get("normal", {}).get("f1-score", None),
            "Precision_SLE": report.get("sle", {}).get("precision", None),
            "Recall_SLE": report.get("sle", {}).get("recall", None),
            "F1_SLE": report.get("sle", {}).get("f1-score", None),
        })

        importances = pd.Series(model.feature_importances_, index=X.columns)
        top_features = importances.sort_values(ascending=False).head(10)

        top_features.to_csv(os.path.join(output_dir, f"feature_importance_{gender}.csv"))
        df_feat = top_features.reset_index()
        df_feat.columns = ["Feature", "Importance"]
        df_feat["Gender"] = gender
        features_list.append(df_feat)

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=top_features.values, y=top_features.index)
        ax.set_title(f"Top 10 Important Features - {gender.title()}")
        ax.set_xlabel("Importance")
        ax.set_ylabel("")
        ax.tick_params(axis='y', labelsize=10)
        for label in ax.get_yticklabels():
            label.set_horizontalalignment('right')
            label.set_fontsize(9)

        plt.subplots_adjust(left=0.4)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"feature_importance_{gender}.png"))
        plt.close()

    # === 6. Save Excel summary ===
    excel_path = os.path.join(output_dir, "SLE_RF_summary.xlsx")
    metrics_df = pd.DataFrame(metrics_list)
    features_df = pd.concat(features_list, ignore_index=True)
    model_meta = pd.DataFrame(model_info.items(), columns=["Parameter", "Value"])

    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        metrics_df.to_excel(writer, index=False, sheet_name="Model_Performance")
        features_df.to_excel(writer, index=False, sheet_name="Top_Features")
        model_meta.to_excel(writer, index=False, sheet_name="Model_Info")

    print("\n🎉 Done! All files saved in /output folder.")


# === Run on your cleaned dataset by default ===
run_model_on_file("C:\\Users\\PC\\Desktop\\SLE\\GSE88884_metadata_transposed_clean.csv")
