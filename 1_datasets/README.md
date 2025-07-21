# Datasets

## Dataset Overview

This folder contains the datasets used for our phishing email detection research.

### Enron.csv

**Source**: Enron Email Dataset - publicly available corporate email dataset

**Collection Method**: Historical email data from Enron Corporation, preprocessed for phishing detection research

**Size**: 29,767 emails

- Safe emails: 15,791 (53.05%)
- Phishing emails: 13,976 (46.95%)

**Connection to Research Question**: This dataset allows us to analyze linguistic patterns and psychological manipulation tactics used in phishing emails compared to legitimate business communications. The balanced nature of the dataset ensures fair comparison between phishing and safe email characteristics.

**Structure**:

- Email content (subject + body)
- Binary classification label (phishing/safe)
- Preprocessed and cleaned text data

**Limitations and Caveats**:

- Historical data may not reflect current phishing techniques
- Corporate email context may not generalize to personal email patterns
- Dataset balance is artificially maintained and may not reflect real-world proportions
- Some preprocessing artifacts may be present from the original Enron dataset

**Usage**: This dataset is used by scripts in `/2_data_preparation` for cleaning and feature extraction, and by analysis scripts in `/4_data_analysis` for modeling and statistical analysis.
