# Data Exploration

## Overview

This folder is designated for initial data exploration scripts and notebooks to understand the structure and characteristics of our phishing email dataset before conducting formal analysis.

## Purpose

Data exploration helps us:

- Understand dataset structure and quality
- Identify patterns and anomalies in the data
- Inform feature engineering decisions
- Guide analysis strategy development
- Validate data cleaning effectiveness

## Expected Explorations

Future explorations in this folder should focus on:

### Dataset Overview

- Email distribution (phishing vs. safe)
- Text length distributions
- Missing data patterns
- Data quality assessment

### Preliminary Pattern Analysis

- Word frequency distributions
- Basic sentiment patterns
- Email structure characteristics
- Temporal patterns (if timestamp data available)

### Feature Understanding

- Distribution of extracted linguistic features
- Correlation between features
- Outlier identification
- Feature stability across different email types

## Usage Notes

- Scripts in this folder should be exploratory and experimental
- Use this folder for initial insights before formal analysis in `/4_data_analysis`
- All exploration should use datasets from `/1_datasets`
- Document interesting findings that inform the analysis strategy

**Note**: Current explorations are integrated into the main analysis pipeline in `/4_data_analysis`. This folder is prepared for future exploration work or alternative analysis approaches.

Our datset contains 15761 phishing and 13949 safe emails.Below we visually summarize the total class phishing and safe emails

![Class Distribution](../plots/01_dataset_overview.png)

### Sentiment Analysis Results

- **Sentiment Scores Explained**:  
  - **Negative**: Threatening, alarming, or discouraging language.  
  - **Neutral**: Plain, factual, or emotionless language.  
  - **Positive**: Encouraging, flattering, or rewarding language.  

- **Average Sentiment Scores (bar chart)**:  
  Shows the average negative, neutral, and positive scores.  
  👉 Safe emails are mostly neutral. Phishing emails are less neutral and show slightly higher negative and positive tone.

- **Compound Sentiment Distribution (histogram)**:  
  Compound = one overall score from -1 (very negative tone, e.g., threats or warnings) to +1 (very positive tone, e.g., congratulations or rewards).  
  👉 Safe emails cluster around neutral to slightly positive. Phishing emails spread more widely, with spikes toward both very positive and more negative scores.

- **Sentiment Feature Correlation Matrix (heatmap)**:  
  Correlation shows how scores move together.  
  👉 Negative sentiment correlates positively with phishing (+0.25), neutral correlates negatively (−0.24), positive correlates weakly positively (+0.11), and compound is slightly negative (−0.076). Effects are modest but indicate phishing emails are less neutral and somewhat more emotional.

- **Sentiment Score Distribution by Email Type (boxplots)**:  
  Boxplots show spread and outliers.  
  👉 Safe emails stay mostly neutral with low variability. Phishing emails show higher negative and positive scores, lower neutrality, and more variability overall.

![Frequent Words](../plots/02_sentiment_analysis.png)

### Technical Pattern Analysis Results

- **URL Usage in Emails (bar chart, top-left)**:  
  Shows the average number of links (URLs) per email.  
  👉 Phishing emails contain more URLs on average, while safe emails have fewer.

- **Email Address Patterns in Content (bar chart, top-right)**:  
  Measures how often email addresses appear within the message text.  
  👉 Safe emails include more visible email address patterns (e.g., signatures, contact info), while phishing emails rarely include them.

- **Distribution of URL Counts (histogram, bottom-left)**:  
  Shows how many emails contain different numbers of URLs.  
  👉 Most emails (safe and phishing) contain no URLs, but phishing emails are more likely to include multiple links.

- **Technical Pattern Usage (grouped bar chart, bottom-right)**:  
  Combines URL and email address counts for comparison.  
  👉 Safe emails rely heavily on email address patterns, phishing emails rely more on URLs.

![URL_Existence](../plots/09_url_email_patterns.png)
