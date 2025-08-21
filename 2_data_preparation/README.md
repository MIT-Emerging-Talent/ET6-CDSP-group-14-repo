# Data Preparation

## Overview

This folder contains scripts and notebooks for cleaning and preparing the phishing email dataset for analysis. All scripts read data from `/1_datasets` and output cleaned data back to the same folder.

## Scripts and Notebooks

### data_cleaning.py

**Purpose**: Data loading, cleaning, and preprocessing pipeline for the Enron phishing email dataset.

**Input**:

- `../1_datasets/Enron.csv` - Raw email dataset

**Processing Steps**:

1. **Initial Exploration**: Loads dataset, prints shape, columns, label distribution, and missing values.
2. **Filtering**: Removes emails with missing or empty bodies.
3. **Text Cleaning**:
   - Removes Enron-specific headers, footers, signatures, and forwarded-message artifacts.
   - Strips company names and identifiers (e.g., `enron`, `ect`, `hou`).
   - Removes email addresses, numbers, dates, and boilerplate phrases.
   - Normalizes whitespace and characters for consistent formatting.
4. **Length Filtering**: Drops very short or trivial messages (less than 10 characters).
5. **Output Validation**: Prints stats on remaining vs. removed emails, dataset shape, and preview of cleaned text.

**Output**:

- Cleaned dataset saved as `Enron_cleaned.csv` in `/1_datasets`
- Includes a new column `body_clean` with processed text

**Dependencies**: See `../4_data_analysis/requirements.txt` for required Python packages

## Data Preparation Strategy

Our research focuses on identifying linguistic differences between phishing emails and legitimate ones by studying how language is used in both. Cleaning the raw text is a necessary first step before extracting features and running analysis.

### Cleaning Approach

We prepare the text for further analysis by:

- **Removing noise**: Corporate artifacts, forwarded lines, and technical markers
- **Normalizing text**: Lowercasing, stripping numbers, and standardizing whitespace
- **Filtering**: Dropping incomplete or trivial messages

### Quality Control

- **Deduplication/Filtering**: Remove unusable or empty entries
- **Missing Data Handling**: Exclude rows with missing body text
- **Export Validation**: Save and check that the cleaned dataset has expected size and columns

## Usage

To run the cleaning pipeline:

1. Ensure the raw dataset is in `/1_datasets/Enron.csv`
2. Open `data_cleaning.py`
3. Run the script
4. The cleaned dataset will be saved as `Enron_cleaned.csv` in `/1_datasets`
