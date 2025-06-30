# Data Preparation

This directory contains scripts and documentation for preparing the phishing email datasets for analysis.

## Overview

The data preparation phase involves merging two separate phishing email datasets from different time periods into a single, unified dataset that can be used for machine learning and analysis.

## Dataset Merge Process

### Input Datasets

1. **Historical Dataset (1993-2008)**
   - File: `phising_vs_simple_email_raw(1993_2008).csv`
   - Records: 3,065 emails
   - Time Period: 1993-2008
   - Original Column Order: `sender`, `receiver`, `date`, `subject`, `body`, `label`, `urls`

2. **Recent Dataset (2015-2022)**
   - File: `phising_vs_simple_email_raw(2015-2022).csv`
   - Records: 1,565 emails
   - Time Period: 2015-2022
   - Original Column Order: `sender`, `receiver`, `date`, `subject`, `body`, `urls`, `label`

### Merge Criteria

#### 1. **Column Standardization**

- **Issue**: The two datasets had identical columns but in different orders
- **Solution**: Standardized column order to: `sender`, `receiver`, `date`, `subject`, `body`, `label`, `urls`
- **Rationale**: Ensures consistent data structure for downstream analysis

#### 2. **Data Preservation**

- **Approach**: No deduplication performed
- **Rationale**:
  - Different time periods make duplicates unlikely
  - Preserves all available training data
  - Maintains temporal distribution of phishing techniques

#### 3. **Source Tracking**

- **Implementation**: Added `source_dataset` column with values:
  - `"1993-2008"` for historical data
  - `"2015-2022"` for recent data
- **Purpose**: Enables analysis of temporal patterns and dataset-specific characteristics

#### 4. **Data Integrity**

- **Validation**: Verified column types and structures match between datasets
- **Preservation**: No modification of original data values
- **Quality**: Maintained all original email content and labels

### Output Dataset

**File**: `merged_phishing_dataset.csv` (saved in `1_datasets/` directory)

**Statistics**:

- **Total Records**: 4,630 emails
- **Columns**: 8 (`sender`, `receiver`, `date`, `subject`, `body`, `label`, `urls`, `source_dataset`)
- **Label Distribution**:
  - Phishing emails (label=1): 3,130 (67.6%)
  - Legitimate emails (label=0): 1,500 (32.4%)
- **Source Distribution**:
  - 1993-2008 dataset: 3,065 records (66.2%)
  - 2015-2022 dataset: 1,565 records (33.8%)

## Files

### `merge_datasets.py`

**Purpose**: Main script for merging the two phishing datasets

**Features**:

- Loads both CSV datasets using pandas
- Standardizes column ordering
- Adds source tracking column
- Performs data validation
- Outputs comprehensive merge statistics
- Saves merged dataset to `1_datasets/merged_phishing_dataset.csv`

**Usage**:

```bash
python merge_datasets.py
```

**Dependencies**:

- `pandas`: For data manipulation and CSV handling
- `os`: For file path operations
- `datetime`: For timestamping the merge process

## Merge Process Documentation

### Step-by-Step Process

1. **Load Datasets**
   - Read both CSV files using pandas
   - Verify successful loading and record counts

2. **Column Analysis**
   - Compare column names and data types
   - Identify any structural differences

3. **Standardization**
   - Reorder columns to match target schema
   - Ensure consistent data types

4. **Source Annotation**
   - Add `source_dataset` column to track data origin
   - Enables future analysis of temporal patterns

5. **Concatenation**
   - Merge datasets using pandas concat
   - Preserve all records without deduplication

6. **Validation**
   - Verify final record count matches sum of inputs
   - Check column structure and data types
   - Generate summary statistics

7. **Output**
   - Save merged dataset to CSV format
   - Generate comprehensive merge report

### Quality Assurance

- **Record Count Verification**: Final count (4,630) = Dataset1 (3,065) + Dataset2 (1,565) ✓
- **Column Integrity**: All original columns preserved with consistent ordering ✓
- **Data Type Consistency**: Maintained original data types across merge ✓
- **Source Traceability**: Each record tagged with source dataset ✓

## Next Steps

The merged dataset (`merged_phishing_dataset.csv`) is now ready for:

1. **Data Exploration**: Statistical analysis and visualization
2. **Feature Engineering**: Text processing and feature extraction
3. **Model Training**: Machine learning model development
4. **Analysis**: Comparative studies across time periods

## Notes

- The merge process is fully automated and reproducible
- All original data is preserved without modification
- The source tracking enables temporal analysis of phishing evolution
- No data cleaning or preprocessing is performed at this stage
