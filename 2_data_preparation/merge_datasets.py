#!/usr/bin/env python3
"""
Dataset Merger Script
=====================

This script merges two phishing email datasets:
1. phising_vs_simple_email_raw(1993_2008).csv
2. phising_vs_simple_email_raw(2015-2022).csv

Merge Criteria:
- Both datasets contain the same columns but in different order
- Dataset 1 (1993-2008): sender, receiver, date, subject, body, label, urls
- Dataset 2 (2015-2022): sender, receiver, date, subject, body, urls, label
- Final merged dataset will use consistent column order: sender, receiver, date, subject, body, label, urls
- All rows from both datasets will be included (concatenation)
- No deduplication performed as datasets cover different time periods
- Output file: merged_phishing_dataset.csv
"""

import os
from datetime import datetime

import pandas as pd


def merge_datasets():
    """
    Merge the two phishing email datasets into a single file.
    """
    # Define file paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset1_path = os.path.join(
        base_path, "1_datasets", "phising_vs_simple_email_raw(1993_2008).csv"
    )
    dataset2_path = os.path.join(
        base_path, "1_datasets", "phising_vs_simple_email_raw(2015-2022).csv"
    )
    output_path = os.path.join(base_path, "1_datasets", "merged_phishing_dataset.csv")

    print("Starting dataset merge process...")
    print(f"Dataset 1: {dataset1_path}")
    print(f"Dataset 2: {dataset2_path}")
    print(f"Output: {output_path}")

    # Load datasets
    print("\nLoading datasets...")
    try:
        df1 = pd.read_csv(dataset1_path)
        print(f"Dataset 1 loaded: {len(df1)} rows")
        print(f"Columns: {list(df1.columns)}")

        df2 = pd.read_csv(dataset2_path)
        print(f"Dataset 2 loaded: {len(df2)} rows")
        print(f"Columns: {list(df2.columns)}")

    except Exception as e:
        print(f"Error loading datasets: {e}")
        return False

    # Define consistent column order
    target_columns = ["sender", "receiver", "date", "subject", "body", "label", "urls"]

    # Reorder columns in both datasets
    print("\nReordering columns to match target schema...")
    df1_reordered = df1[target_columns]
    df2_reordered = df2[target_columns]

    # Add source information to track which dataset each row came from
    df1_reordered = df1_reordered.copy()
    df2_reordered = df2_reordered.copy()
    df1_reordered["source_dataset"] = "1993-2008"
    df2_reordered["source_dataset"] = "2015-2022"

    # Merge datasets
    print("\nMerging datasets...")
    merged_df = pd.concat([df1_reordered, df2_reordered], ignore_index=True)

    print(f"Merged dataset: {len(merged_df)} rows")
    print(f"Final columns: {list(merged_df.columns)}")

    # Save merged dataset
    print(f"\nSaving merged dataset to: {output_path}")
    try:
        merged_df.to_csv(output_path, index=False)
        print("✓ Merged dataset saved successfully!")

        # Display summary statistics
        print("\n" + "=" * 50)
        print("MERGE SUMMARY")
        print("=" * 50)
        print(f"Total rows in merged dataset: {len(merged_df):,}")
        print(f"Rows from 1993-2008 dataset: {len(df1):,}")
        print(f"Rows from 2015-2022 dataset: {len(df2):,}")
        print(f"Total columns: {len(merged_df.columns)}")

        # Label distribution
        print("\nLabel distribution:")
        label_counts = merged_df["label"].value_counts()
        for label, count in label_counts.items():
            percentage = (count / len(merged_df)) * 100
            print(f"  {label}: {count:,} ({percentage:.1f}%)")

        # Source distribution
        print("\nSource dataset distribution:")
        source_counts = merged_df["source_dataset"].value_counts()
        for source, count in source_counts.items():
            percentage = (count / len(merged_df)) * 100
            print(f"  {source}: {count:,} ({percentage:.1f}%)")

        return True

    except Exception as e:
        print(f"Error saving merged dataset: {e}")
        return False


if __name__ == "__main__":
    print("Email Phishing Dataset Merger")
    print("=" * 30)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    success = merge_datasets()

    if success:
        print("\n✓ Dataset merge completed successfully!")
    else:
        print("\n✗ Dataset merge failed!")
