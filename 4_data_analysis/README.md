# Data Analysis

## Overview

This folder contains the main analysis scripts, notebooks, and results for our phishing email detection research. The analysis examines linguistic patterns and psychological manipulation tactics that distinguish phishing emails from legitimate communications.

## Analysis Strategy

Our analysis approach combines statistical analysis with machine learning to understand phishing email characteristics:

1. **Feature Engineering**: Extract 22 linguistic and psychological features from email text
2. **Statistical Analysis**: Use Cohen's d effect size to quantify feature importance
3. **Machine Learning**: Implement Random Forest classifier for prediction
4. **Visualization**: Create comprehensive plots to illustrate findings

## Files and Components

### Main Analysis Script

**phishing_analysis.py**

- Core analysis implementation
- Feature extraction and statistical analysis
- Machine learning model training and evaluation
- Generates all plots and statistical comparisons

### Reports

**technical_report.md**

- Detailed technical methodology and findings
- Statistical results with effect sizes
- Machine learning performance metrics
- Technical interpretation of results

**non_technical_report.md**

- Executive summary for general audiences
- Key findings explained in accessible language
- Practical implications and real-world examples
- Visual aids and clear explanations

### Results and Outputs

**plots/** folder contains:

- `01_dataset_overview.png` - Dataset composition and balance
- `02_sentiment_analysis.png` - Sentiment differences between email types
- `03_psychological_radar.png` - Psychological manipulation tactics
- `04_text_complexity.png` - Linguistic complexity patterns
- `05_punctuation_analysis.png` - Punctuation usage differences
- `06_tfidf_analysis.png` - Most discriminative terms
- `07_feature_importance.png` - Machine learning feature importance
- `08_readability_analysis.png` - Text readability comparisons
- `09_url_email_patterns.png` - Structural pattern analysis
- `10_enhanced_boxplot_comparison.png` - Comprehensive feature comparison

**Analysis Result Files**:

- `feature_comparison_stats.csv` - Statistical comparison of all features
- `top_phishing_terms.csv` - Most characteristic phishing words
- `top_safe_terms.csv` - Most characteristic legitimate email words

### Dependencies

**requirements.txt**

- Python packages required for analysis
- Includes pandas, scikit-learn, matplotlib, seaborn, nltk, etc.

## Key Research Findings

### Main Conclusions

Our analysis reveals that **phishing emails use specific psychological tactics and language patterns** that can be detected with 84% accuracy. Key findings include:

1. **Emotional Manipulation**: Phishing emails contain 85% more negative sentiment and 3.5x more exclamation marks
2. **Psychological Tactics**: Higher use of financial terms (57%), reward words (36%), and urgency language
3. **Linguistic Patterns**: More complex vocabulary but different structural patterns than legitimate emails

### Confidence Level

We have **high confidence** in these results based on:

- Large sample size (29,767 emails)
- Statistically significant effect sizes (Cohen's d > 0.5 for key features)
- Consistent patterns across multiple analytical approaches
- Cross-validated machine learning performance

### Limitations

- Historical dataset may not reflect current phishing techniques
- Corporate email context may limit generalizability
- English-only analysis
- Balanced dataset doesn't reflect real-world phishing prevalence

### Future Research

- Analysis of current phishing campaigns
- Multilingual phishing detection
- Real-time classification systems
- Integration with email security platforms

## Usage

1. Ensure data preparation is complete (`/2_data_preparation/data_cleaning.ipynb`)
2. Install dependencies: `pip install -r requirements.txt`
3. Run the main analysis: `python phishing_analysis.py`
4. Review results in the generated plots and CSV files
5. Read detailed findings in the technical and non-technical reports
