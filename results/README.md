# Results Directory

This directory contains all the outputs and results from the phishing email analysis project.

## 📊 Structure

### `/visualizations/`

Contains all plots and charts generated from the analysis:

- `01_dataset_overview.png` - Dataset composition and statistics
- `02_sentiment_analysis.png` - Sentiment distribution comparison
- `03_psychological_radar.png` - Psychological manipulation tactics
- `04_text_complexity.png` - Text complexity metrics
- `05_punctuation_analysis.png` - Punctuation usage patterns
- `06_tfidf_analysis.png` - TF-IDF feature importance
- `07_feature_importance.png` - Machine learning feature importance
- `08_readability_analysis.png` - Readability scores comparison
- `09_url_email_patterns.png` - URL and email pattern analysis
- `10_enhanced_boxplot_comparison.png` - Statistical comparison boxplots
- `effect_sizes_with_significance.png` - Effect sizes with significance testing

### `/statistical_analysis/`

Contains statistical analysis results and data:

- `feature_comparison_stats.csv` - Complete statistical comparison of all features
- `enhanced_statistical_results.csv` - Enhanced results with p-values and confidence intervals
- `top_phishing_terms.csv` - Most discriminative terms for phishing emails
- `top_safe_terms.csv` - Most discriminative terms for legitimate emails

### `/reports/`

Contains human-readable analysis reports:

- `technical_report.md` - Detailed technical analysis with methodology
- `non_technical_report.md` - Accessible summary for general audiences
- `REVIEW_RESPONSE.md` - Response to peer review feedback and improvements made

## 🔍 Key Findings

### Statistical Significance

- **Medium effects**: sentiment_neg (Cohen's d = 0.501)
- **Small effects**: 10 features including sentiment manipulation and vocabulary complexity
- **Negligible effects**: 13 features including email length measures

### Critical Insight

**Phishing emails are NOT significantly longer than legitimate emails** (Cohen's d = -0.061, negligible effect). The key differences lie in psychological manipulation tactics and word choice, not overall length.

### Most Discriminative Features

1. **Sentiment manipulation**: Higher negative sentiment, lower neutral sentiment
2. **Vocabulary complexity**: More diverse vocabulary, longer words
3. **Psychological tactics**: More financial terms, reward words, urgency language
4. **Structural elements**: More exclamation marks, more URLs

## 📈 Model Performance

- **Accuracy**: 83.5%
- **Precision**: 86.4% (phishing detection)
- **Recall**: 77.1% (phishing detection)
- **F1-Score**: 81.5%
