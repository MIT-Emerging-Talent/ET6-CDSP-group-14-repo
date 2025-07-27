# Contributing to Phishing Email Linguistic Analysis Project

This document provides guidelines for contributing to **The Pandas Pact** project repository.

---

## 🤝 How to Contribute

We welcome contributions in several areas:

### Research Contributions

- **Data Analysis Improvements**: Enhanced statistical methods or machine learning approaches
- **Feature Engineering**: New linguistic or psychological features for phishing detection
- **Validation Studies**: Testing our methodology on different datasets
- **Contemporary Analysis**: Applying our approach to current phishing campaigns

### Technical Contributions

- **Code Optimization**: Performance improvements or code refactoring
- **Documentation**: Enhanced README files, code comments, or tutorial materials
- **Visualization**: Improved or additional data visualization techniques
- **Reproducibility**: Better environment setup or dependency management

### Methodological Contributions

- **Cross-Language Analysis**: Extending analysis to non-English emails
- **Real-World Testing**: Validation in production email filtering systems
- **User Studies**: Integration of human behavior research with linguistic analysis

---

## 🛠️ Development Workflow

### Getting Started

1. **Fork the Repository**

   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/ET6-CDSP-group-14-repo.git
   cd ET6-CDSP-group-14-repo
   ```

2. **Set Up Environment**

   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r 4_data_analysis/requirements.txt
   ```

3. **Create Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. **Follow Project Structure**
   - Use appropriate folders for your contributions
   - Follow existing naming conventions
   - Update relevant README files

2. **Code Quality Standards**

   ```bash
   # Format code consistently
   pip install black isort
   black .
   isort .
   
   # Add docstrings and comments
   # Follow PEP 8 style guidelines
   ```

3. **Testing Your Changes**

   ```bash
   # Test analysis pipeline
   python 4_data_analysis/phishing_analysis.py
   
   # Verify reproducibility
   # Check that plots and results match expected outputs
   ```

### Submitting Changes

1. **Commit Guidelines**

   ```bash
   # Use descriptive commit messages
   git add .
   git commit -m "feat: add new sentiment analysis feature
   
   - Implement BERT-based sentiment scoring
   - Update feature extraction pipeline
   - Add validation tests for new feature"
   ```

2. **Push and Create Pull Request**

   ```bash
   git push origin feature/your-feature-name
   # Create pull request on GitHub
   ```

---

## 📊 Data Guidelines

### Working with Datasets

1. **Data Privacy**
   - Never commit personally identifiable information
   - Use anonymized or synthetic data for examples
   - Follow ethical guidelines for email data analysis

2. **Data Documentation**
   - Document data sources and collection methods
   - Include data limitation and bias considerations
   - Provide clear usage instructions

3. **Reproducibility**
   - Include data preprocessing steps
   - Document feature engineering decisions
   - Provide sample data for testing

### New Dataset Integration

If adding new datasets:

```python
# Follow this structure in 1_datasets/
dataset_name/
├── README.md           # Dataset documentation
├── raw_data.csv       # Original data (if shareable)
├── processed_data.csv # Cleaned data
└── validation_report.md # Data quality assessment
```

---

## 🔬 Research Standards

### Analysis Contributions

1. **Statistical Rigor**
   - Report effect sizes, not just p-values
   - Include confidence intervals
   - Address multiple testing corrections when appropriate
   - Validate assumptions of statistical tests

2. **Machine Learning Best Practices**
   - Use proper train/validation/test splits
   - Report cross-validation results
   - Include feature importance analysis
   - Discuss model limitations and bias

3. **Visualization Standards**
   - Clear, publication-ready plots
   - Appropriate chart types for data
   - Consistent color schemes and styling
   - Accessible design (colorblind-friendly)

### Documentation Requirements

1. **Technical Reports**
   - Complete methodology description
   - Statistical results with interpretation
   - Discussion of limitations
   - Future research directions

2. **Code Documentation**

   ```python
   def extract_linguistic_features(text):
       """
       Extract linguistic features from email text.
       
       Args:
           text (str): Email content (subject + body)
           
       Returns:
           dict: Dictionary containing feature values
           
       Example:
           >>> features = extract_linguistic_features("Urgent! Act now!")
           >>> print(features['exclamation_count'])
           2
       """
   ```

---

## 🌍 Collaboration Guidelines

### Team Communication

1. **Inclusive Collaboration**
   - Respect diverse cultural perspectives
   - Use clear, accessible language in discussions
   - Provide context for technical decisions
   - Welcome questions and different approaches

2. **Feedback Culture**
   - Provide constructive, specific feedback
   - Focus on improvement opportunities
   - Acknowledge good work and contributions
   - Be open to receiving feedback

### Cross-Cultural Considerations

1. **Communication Styles**
   - Be explicit about expectations and deadlines
   - Accommodate different time zones for synchronous work
   - Use written communication to supplement verbal discussions
   - Provide multiple channels for contribution (issues, discussions, PR comments)

2. **Knowledge Sharing**
   - Explain domain-specific concepts clearly
   - Provide background context for technical decisions
   - Share learning resources and references
   - Create opportunities for skill development

---

## 🐛 Issue Reporting

### Bug Reports

Use this template for bug reports:

```markdown
**Bug Description**
Brief description of the issue

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen

**Environment**
- OS: [e.g., Windows 10, macOS 12.0]
- Python version: [e.g., 3.9.7]
- Package versions: [relevant package versions]

**Additional Context**
Any other context about the problem
```

### Feature Requests

```markdown
**Feature Description**
Clear description of the proposed feature

**Research Justification**
How this feature would improve the analysis or methodology

**Implementation Ideas**
Suggestions for how this could be implemented

**References**
Relevant papers, tools, or examples
```

---

## 📚 Resources

### Technical References

- [Cohen's d Effect Size Calculator](https://www.psychometrica.de/effect_size.html)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [NLTK Documentation](https://www.nltk.org/)

### Research Background

- [Phishing Detection Research](./0_domain_study/README.md)
- [Feature Engineering Guide](./2_data_preparation/README.md)
- [Analysis Methodology](./4_data_analysis/technical_report.md)

### Project Documentation

- [Team Collaboration Guide](./collaboration/README.md)
- [Project Structure Guide](./guide.md)
- [Retrospectives](./collaboration/retrospectives/)

---

## 📄 License and Attribution

### Contributing Agreement

By contributing to this project, you agree that:

1. Your contributions will be licensed under the same terms as the project
2. You have the right to submit your contributions
3. Your contributions are your original work or properly attributed
4. You consent to the potential use of your contributions in academic publications

### Attribution

Contributors will be acknowledged in:

- Project documentation and README files
- Academic publications resulting from this work
- Presentation materials and reports

---

## ❓ Getting Help

### Support Channels

1. **GitHub Issues**: Technical problems or feature requests
2. **GitHub Discussions**: General questions and brainstorming
3. **Team Slack**: `#et6_cdsp_group_14` (for team members)

### FAQ

**Q: Can I contribute if I'm not part of the original team?**
A: Yes! We welcome external contributions that advance the research.

**Q: What if I find an error in the analysis?**
A: Please open an issue with details. We value corrections and improvements.

**Q: Can I use this methodology for my own research?**
A: Yes! Please cite our work appropriately.

**Q: How can I contribute without coding skills?**
A: You can contribute through documentation, literature review, or research design suggestions.

---

## 🚀 Recognition

Outstanding contributors may be invited to:

- Co-author academic publications
- Present findings at conferences
- Collaborate on future research projects
- Mentor new contributors to the project

---

## Thank You

Thank you for contributing to better understanding of phishing detection through linguistic analysis! 🛡️
