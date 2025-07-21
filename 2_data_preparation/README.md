# Data Preparation

## Overview

This folder contains scripts and notebooks for cleaning, transforming, and preparing our phishing email dataset for analysis. All scripts read data from `/1_datasets` and output cleaned/processed data back to the same folder.

## Scripts and Notebooks

### data_cleaning.ipynb

**Purpose**: Comprehensive data cleaning and feature extraction pipeline for the Enron phishing email dataset.

**Input**:

- `../1_datasets/Enron.csv` - Raw email dataset

**Processing Steps**:

1. **Text Cleaning**: Removes Enron-specific artifacts, email headers, corporate signatures, and stop words
2. **Feature Extraction**: Applies NLP techniques for:
   - Sentiment analysis (VADER sentiment scores)
   - Linguistic features (type-token ratio, word lengths, sentence complexity)
   - Psychological markers (urgency words, financial terms, manipulation tactics)
   - Readability metrics (Flesch scores, Gunning Fog index)
   - Structural patterns (punctuation analysis, URL detection)

**Output**:

- Cleaned and feature-enriched dataset with 22 linguistic and psychological features
- Ready for statistical analysis and machine learning modeling

**Dependencies**: See `../4_data_analysis/requirements.txt` for required Python packages

## Data Preparation Strategy

Our research focuses on identifying linguistic differences between phishing emails and legitimate ones by studying how language is used in both. Phishing emails often use certain writing tactics to trick or pressure readers, and we aim to uncover those patterns.

### Text Processing Approach

We convert text into measurable patterns using several techniques:

- **Word Frequency Analysis**: Identify phrases that appear more often in phishing emails than in legitimate ones
- **Sentiment Analysis**: Measure emotional content and manipulation tactics
- **Linguistic Complexity**: Analyze vocabulary diversity, sentence structure, and readability
- **Psychological Markers**: Detect urgency, financial pressure, and reward promises

### Quality Control

- **Deduplication**: Remove repeated emails by comparing content
- **Missing Data Handling**: Process emails with missing subject or body values
- **Text Normalization**: Convert to consistent format for analysis
- **Feature Validation**: Ensure extracted features are meaningful and consistent

## Usage

To run the data cleaning pipeline:

1. Ensure the raw dataset is in `/1_datasets/Enron.csv`
2. Open `data_cleaning.ipynb` in Jupyter Notebook
3. Run all cells to process the data and extract features
4. The cleaned dataset will be ready for analysis in `/4_data_analysis`
