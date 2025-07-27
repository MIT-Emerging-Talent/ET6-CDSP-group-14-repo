# 🛡️ Phishing Email Linguistic Analysis Project

## A Linguistic Analysis of Phishing vs Legitimate Emails: Identifying Common Patterns and Language Tactics

[![Project Status](https://img.shields.io/badge/Status-Complete-success)](https://github.com/MIT-Emerging-Talent/ET6-CDSP-group-14-repo)
[![Dataset](https://img.shields.io/badge/Dataset-Enron_Emails-blue)](./1_datasets/)
[![Language](https://img.shields.io/badge/Language-Python-yellow)](https://www.python.org/)
[![Accuracy](https://img.shields.io/badge/ML_Accuracy-84%25-brightgreen)](./4_data_analysis/)

---

## 🎯 Research Overview

This project investigates the linguistic patterns and psychological manipulation tactics that distinguish phishing emails from legitimate communications. Using a dataset of 29,767 emails, we applied statistical analysis and machine learning to identify key features that make phishing emails effective.

### Key Findings

🔍 **Phishing emails use 85% more negative sentiment** and contain **3.5x more exclamation marks** than legitimate emails

📊 **84% detection accuracy** achieved through linguistic pattern analysis

💰 **57% higher frequency of financial terms** and urgency language in phishing attempts

🧠 **Psychological manipulation tactics** clearly identifiable through linguistic analysis

---

## 🌍 About The Pandas Pact

**The Pandas Pact** is a diverse, cross-cultural team of data science researchers from across the globe, working collaboratively to understand cybersecurity threats through linguistic analysis. Our team combines diverse cultural perspectives with technical expertise to deliver meaningful research insights.

---

## 🗂️ Project Structure

```text
├── README.md                        # Project overview (you are here)
├── guide.md                         # Detailed usage guidelines
├── CONTRIBUTING.md                  # Contribution guidelines
├── collaboration/                   # Team norms and retrospectives
├── notes/                          # Shared learning resources
├── 0_domain_study/                 # Phishing research background
├── 1_datasets/                     # Raw and processed email data
├── 2_data_preparation/            # Data cleaning and feature extraction
├── 3_data_exploration/            # Initial data understanding
├── 4_data_analysis/               # Main analysis and results
├── 5_communication_strategy/      # Results communication planning
└── 6_final_presentation/          # Presentation materials
```

---

## 🔬 Research Methodology

### Data Collection

- **Dataset**: Enron Email Dataset with phishing labels
- **Size**: 29,767 emails (53% legitimate, 47% phishing)
- **Source**: [1_datasets/](./1_datasets/) folder
- **Documentation**: [Dataset README](./1_datasets/README.md)

### Data Preparation

- **Text Cleaning**: Removed Enron-specific artifacts and standardized formatting
- **Feature Extraction**: 22 linguistic and psychological features
- **Processing**: [2_data_preparation/](./2_data_preparation/) scripts
- **Documentation**: [Preparation README](./2_data_preparation/README.md)

### Analysis Approach

- **Statistical Analysis**: Cohen's d effect sizes for feature importance
- **Machine Learning**: Random Forest classifier with cross-validation
- **Visualization**: 10 comprehensive plots illustrating findings
- **Implementation**: [4_data_analysis/](./4_data_analysis/) folder
- **Results**: [Technical Report](./4_data_analysis/technical_report.md) | [Non-Technical Report](./4_data_analysis/non_technical_report.md)

---

## 📊 Key Research Results

### Statistical Findings

| Feature | Phishing vs Legitimate | Effect Size (Cohen's d) | Significance |
|---------|------------------------|-------------------------|--------------|
| Negative Sentiment | +85% higher | 0.73 | Large |
| Exclamation Marks | +3.5x more | 0.58 | Medium-Large |
| Financial Terms | +57% higher | 0.52 | Medium |
| Urgency Language | +36% higher | 0.48 | Medium |

### Machine Learning Performance

- **Accuracy**: 84%
- **Precision**: 83% (phishing detection)
- **Recall**: 85% (phishing detection)
- **F1-Score**: 84%

### Research Confidence

We have **high confidence** in these results based on:

- Large sample size (29,767 emails)
- Statistically significant effect sizes
- Cross-validated machine learning performance
- Consistent patterns across multiple analytical approaches

---

## 🎨 Visualizations

Our analysis includes comprehensive visualizations located in [4_data_analysis/plots/](./4_data_analysis/plots/):

1. **Dataset Overview** - Sample composition and balance
2. **Sentiment Analysis** - Emotional manipulation patterns  
3. **Psychological Radar** - Manipulation tactic comparison
4. **Text Complexity** - Linguistic sophistication analysis
5. **Punctuation Analysis** - Structural pattern differences
6. **TF-IDF Analysis** - Most discriminative terms
7. **Feature Importance** - Machine learning insights
8. **Readability Analysis** - Text accessibility patterns
9. **URL/Email Patterns** - Structural characteristics
10. **Enhanced Comparison** - Comprehensive feature overview

---

## 🚀 Reproducibility

### Quick Start

```bash
# Clone repository
git clone https://github.com/MIT-Emerging-Talent/ET6-CDSP-group-14-repo.git
cd ET6-CDSP-group-14-repo

# Install dependencies
pip install -r 4_data_analysis/requirements.txt

# Run full analysis
python 4_data_analysis/phishing_analysis.py
```

### Requirements

- Python 3.8+
- Dependencies: pandas, scikit-learn, matplotlib, seaborn, nltk, wordcloud
- Full requirements: [4_data_analysis/requirements.txt](./4_data_analysis/requirements.txt)

---

## 📚 Documentation Links

### Core Analysis

- [Technical Report](./4_data_analysis/technical_report.md) - Complete methodology and statistical results
- [Non-Technical Report](./4_data_analysis/non_technical_report.md) - Executive summary for general audiences
- [Analysis Code](./4_data_analysis/phishing_analysis.py) - Main analysis implementation

### Data Documentation

- [Dataset Overview](./1_datasets/README.md) - Data sources and characteristics
- [Data Preparation](./2_data_preparation/README.md) - Cleaning and processing methodology
- [Feature Engineering](./2_data_preparation/data_cleaning.ipynb) - Detailed preprocessing pipeline

### Research Background

- [Domain Study](./0_domain_study/README.md) - Phishing research background and problem definition
- [Research Question Evolution](./0_domain_study/guide.md) - How our research focus developed

### Project Management

- [Team Collaboration](./collaboration/README.md) - Group norms and communication strategies
- [Project Retrospectives](./collaboration/retrospectives/) - Milestone reflections and lessons learned

---

## 🔮 Future Research Directions

1. **Contemporary Phishing Analysis** - Study current phishing campaigns vs historical data
2. **Multilingual Detection** - Extend analysis to non-English phishing emails
3. **Real-World Validation** - Test findings with live email filtering systems
4. **Cross-Platform Analysis** - Compare email phishing with SMS and social media tactics
5. **User Behavior Integration** - Incorporate human response patterns into detection models

---

## ⚠️ Limitations

- **Historical Data**: Enron dataset may not reflect current phishing techniques
- **Corporate Context**: Business email environment may not generalize to personal emails
- **English Only**: Analysis limited to English-language communications
- **Balanced Dataset**: Artificial 50/50 split doesn't reflect real-world phishing prevalence (typically <1%)

---

## 🤝 Collaboration & Communication

### Team Coordination

- **Slack Channel**: `#et6_cdsp_group_14`
- **Meetings**: Weekly team coordination via Zoom
- **Documentation**: All shared resources maintained in this repository
- **Full Collaboration Guide**: [collaboration/README.md](./collaboration/README.md)

### Group Norms

- Respect for diverse cultural perspectives and communication styles
- Open, constructive feedback and collaborative problem-solving
- Clear expectations with mutual accountability
- Regular reflection and continuous improvement
- **Complete Group Norms**: [collaboration/README.md](./collaboration/README.md)

---

## 📄 Citation

If you use this research or methodology in your work, please cite:

```bibtex
The Pandas Pact (2025). A Linguistic Analysis of Phishing vs Legitimate Emails: 
Identifying Common Patterns and Language Tactics. 
MIT Emerging Talent Program, Collaborative Data Science Project.
GitHub: https://github.com/MIT-Emerging-Talent/ET6-CDSP-group-14-repo
```

---

## Happy learning and stay safe from phishing! 🛡️
