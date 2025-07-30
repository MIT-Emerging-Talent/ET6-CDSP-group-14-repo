# Technical Analysis Summary

We analyzed a total of **29,710 emails** from the Enron dataset to investigate our research question:

> **"Do linguistic features differ between phishing and non-phishing emails, and are those differences statistically significant?"**

## Hypothesis

We hypothesized that phishing emails would differ from legitimate emails in measurable linguistic ways — such as tone, complexity, and word usage — and that those differences would be statistically significant.

---

### Methodology

- We extracted multiple linguistic features (e.g., sentiment scores, punctuation ratios, readability metrics) from each email.
- For each feature, we compared phishing vs. non-phishing emails using:
  - **Welch’s t-test** to calculate **p-values**
  - **Cohen’s d** to assess **effect size**
  - **95% confidence intervals** to estimate the precision of the difference

All results were stored in `feature_comparison_stats.csv`. Confidence intervals were computed only for features with **effect size ≥ 0.5** and later filtered to include those with **p-value < 0.05**.

---

### Key Finding

One feature met both statistical criteria (**effect size ≥ 0.5** and **p-value < 0.05**):

i.e sentiment negative : we used VADER Sentiment Analyzer to analyze the sentiment

- **Effect size**: 0.50 (Cohen’s d)
- **p-value**: 0.000  
- **95% CI**: (0.0249, 0.0273)

This indicates a **statistically significant** and **substantial difference** in negative emotional tone: phishing emails consistently had **higher negative sentiment scores** than safe emails.

---

### Interpretation

While several other features (e.g., exclamation marks, urgency-related words) showed directional differences, they did not pass the threshold for statistical significance. Therefore, they were not included in the confidence interval summary.

---

### Conclusion

The analysis shows that **negative sentiment** is a key differentiator between phishing and non-phishing emails in this dataset. This finding is both statistically reliable and practically relevant, suggesting it could be useful in phishing detection models.
