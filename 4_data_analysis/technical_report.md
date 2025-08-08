# Technical Report: Phishing Email Detection Analysis

## 1. Introduction

Phishing emails remain a critical cybersecurity threat, leveraging social engineering to deceive recipients into compromising actions. We conducted an in-depth analysis of 29,711 emails from the Enron corpus — 15,762 safe (53.05%) and 13,949 phishing (46.95%) — to identify textual fingerprints and build an
automated detection model. This report details our methodology, exploratory findings (with figures), statistical significance assessments, and a
Random Forest classification performance.

______________________________________________________________________

## 2. Methodology

### 2.1 Dataset & Preprocessing

- **Enron Email Dataset**: 29,767 messages labeled safe or phishing
- **Distribution**: Safe (53.01%), Phishing (46.95%)

**Preprocessing Pipeline:**

1. Text cleaning: strip Enron-specific artifacts, headers, signatures, non-ASCII characters
1. Tokenization: split text into sentences and words
1. Stop-word removal: eliminate common English stop words
1. Normalization: lowercase, remove redundant punctuation

______________________________________________________________________

### 2.2 Feature Engineering

We engineered **22 textual features** across four categories:

**A. Linguistic Complexity**

- Word count, character count, sentence count
- Average word length, average sentence length
- Type-token ratio (vocabulary diversity)

**B. Readability & Style**

- Flesch Reading Ease, Flesch-Kincaid Grade, Gunning Fog Index
- Punctuation density, exclamation ratio, question ratio, special character ratio

**C. Psychological Cues**

- VADER sentiment scores: negative, neutral, positive
- Manipulation lexicons: urgency words, action words, financial terms, fear words, reward words

**D. Structural Patterns**

- URL count, email-pattern count (forwards, CC markers, signature lines)

______________________________________________________________________

### 2.3 Statistical Analysis: Effect Sizes

Cohen’s d was computed to quantify the magnitude of feature differences between phishing and safe emails:

- **Large effect (|d| ≥ 0.5)**:

  - sentiment_neg (d = 0.50)
  - sentiment_neu (d = –0.49)

- **Medium effect (0.3 ≤ |d| < 0.5)**:

  - type_token_ratio (d = 0.37)
  - exclamation_ratio (d = 0.36)
  - avg_word_length (d = 0.32)
  - financial_words (d = 0.32)
  - reward_words (d = 0.31)

- **Small effect (0.2 ≤ |d| < 0.3)**:

  - url_count (d = 0.27)
  - action_words (d = 0.20)
  - urgency_words (d = 0.20)

______________________________________________________________________

### 2.4 Classification Model

- **Algorithm**: Random Forest Classifier (100 trees, `class_weight='balanced'`)
- **Evaluation**: 5-fold cross-validation

**Performance:**

- Accuracy: **83.5%**
- Precision (phishing): **86.4%**
- Recall (phishing): **77.1%**
- F1-score: **81.5%**

**Top 5 Feature Importances:**

1. Exclamation ratio (0.245)
1. URL count (0.139)
1. Type-token ratio (0.133)
1. Punctuation density (0.091)
1. Sentiment compound (0.076)

______________________________________________________________________

## 3. Exploratory Analysis Results

### 3.1 Dataset Overview

- Safe: **15,791 emails** (53.05%)
- Phishing: **13,976 emails** (46.95%)
- Balanced distribution supports robust training without heavy resampling.

______________________________________________________________________

### 3.2 Sentiment Analysis

- Negative sentiment: phishing **0.05** vs safe **0.03** (d = 0.50)
- Neutral sentiment: phishing **0.82** vs safe **0.87** (d = –0.49)
- Positive sentiment: phishing **0.13** vs safe **0.11** (d = 0.23)

**Insight**: Phishing emails leverage both negative pressure and occasional positive reinforcement to manipulate recipients.

______________________________________________________________________

### 3.3 Psychological Feature Radar

- Financial terms: phishing **1.20** vs safe **0.60** (d = 0.32)
- Reward words: phishing **0.95** vs safe **0.60** (d = 0.31)
- Urgency words: phishing **0.42** vs safe **0.35** (d = 0.20)

**Insight**: Financial and reward cues are prominent phishing tactics, while urgency remains a moderate signal.

______________________________________________________________________

### 3.4 Text Complexity

- Word count: phishing **230** vs safe **280** (d = –0.28)
- Char count: phishing **1200** vs safe **1500** (d = –0.29)
- Type-token ratio: phishing **0.52** vs safe **0.48** (d = 0.37)

**Insight**: Phishing messages are shorter but display slightly higher vocabulary diversity.

______________________________________________________________________

### 3.5 Punctuation Usage

- Exclamation ratio: phishing **0.0028** vs safe **0.0008** (d = 0.36)
- Question ratio: phishing **0.0027** vs safe **0.0010** (d = 0.36)
- Punctuation density: phishing **0.065** vs safe **0.045** (d = 0.44)

**Insight**: Elevated punctuation marks underscore the urgent and interrogative tone of phishing emails.

______________________________________________________________________

### 3.6 TF-IDF Term Comparison

**Phishing terms**: `http` (0.049), `www` (0.025), `com` (0.025), `click` (0.025), `free` (0.017)\
**Safe terms**: `vince` (0.038), `pm` (0.034), `cc` (0.032), `subject` (0.031), `thanks` (0.028)

**Insight**: URL-related tokens dominate phishing, whereas names and corporate markers prevail in safe emails.

______________________________________________________________________

### 3.7 Feature Importance

Top discriminative features:

- sentiment_neg (d = 0.50)
- sentiment_neu (d = –0.49)
- type_token_ratio (d = 0.37)
- exclamation_ratio (d = 0.36)
- avg_word_length (d = 0.32)

**Insight**: Emotional tone and vocabulary diversity are the strongest signals.

______________________________________________________________________

### 3.8 Readability Metrics

- Flesch Reading Ease: phishing **–163** vs safe **–200** (d = 0.25)
- Flesch-Kincaid Grade: phishing **8.5** vs safe **10.0**
- Gunning Fog Index: phishing **12.0** vs safe **14.5**

**Insight**: Phishing emails use simpler, more direct language to facilitate quick action.

______________________________________________________________________

### 3.9 URL & Email Pattern Counts

- URL count: phishing **0.70** vs safe **0.25** (d = 0.27)
- Email-pattern count: phishing **0.42** vs safe **2.48** (d = –0.30)

**Insight**: Phishing emails include substantially more URLs; safe emails contain more reply/forward metadata.

______________________________________________________________________

### 3.10 Feature Distributions (Phishing)

- **Word and char counts**: long-tailed distributions with many short emails and few lengthy outliers
- **Exclamation and question ratios**: positively skewed, reflecting urgent tone across most phishing messages

______________________________________________________________________

## 4. Certainty Assessment

- **Overall Confidence**: High, given N = 29,767 and consistent medium-to-large effect sizes
- **CI Coverage**:
  - 95% CI exclude zero for |d| ≥ 0.5
  - 90% CI for 0.3 ≤ |d| < 0.5
  - 85% CI for 0.2 ≤ |d| < 0.3

______________________________________________________________________

## 5. Technical Limitations

- **Temporal Bias**: Enron (2001) may not reflect modern phishing strategies
- **Domain Specificity**: Corporate email context limits generalizability
- **Lexicon Bias**: VADER and static word lists may miss nuanced or emerging manipulation

______________________________________________________________________

## 6. Conclusion & Future Work

We demonstrate that phishing emails exhibit distinctive linguistic and psychological signatures enabling **83.5% detection accuracy** with a Random Forest model. Key signals include sentiment patterns, punctuation usage, URLs, and vocabulary metrics. Future directions involve incorporating header metadata, hybrid ensemble
models, transformer-based sequence analysis, and evaluation on contemporary, diverse datasets.

______________________________________________________________________

## Figures

- **Figure 1**: See `plots/01_*.png`
- **Figure 2**: See `plots/02_*.png`
- **Figure 3**: See `plots/03_*.png`
- **Figure 4**: See `plots/04_*.png`
- **Figure 5**: See `plots/05_*.png`
- **Figure 6**: See `plots/06_*.png`
- **Figure 7**: See `plots/07_*.png`
- **Figure 8**: See `plots/08_*.png`
- **Figure 9**: See `plots/09_*.png`
- **Figure 10**: See `plots/10_*.png`
