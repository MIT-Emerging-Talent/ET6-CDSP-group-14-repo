# Data Collection Retrospective

## Stop Doing

- Searching for perfect datasets that may not exist
- Underestimating time needed for dataset evaluation and documentation
- Making assumptions about data quality without thorough examination

## Continue Doing

- Thorough documentation of data sources and limitations
- Balanced approach to dataset selection considering both quality and feasibility
- Clear connection between datasets and research questions
- Transparent reporting of data limitations and caveats

## Start Doing

- Earlier exploration of multiple dataset options
- Creating data validation scripts to verify dataset integrity
- Establishing clear data quality criteria upfront
- Building relationships with data providers for future research

## Lessons Learned

1. **Dataset availability constrains research scope** - Available phishing datasets shaped our research direction more than initially expected
2. **Historical data has inherent limitations** - Enron dataset provides valuable insights but may not reflect current phishing techniques
3. **Documentation is crucial for reproducibility** - Detailed dataset documentation saves significant time in later analysis phases
4. **Balanced datasets may not reflect reality** - Artificial balance in phishing/legitimate ratios needs careful consideration in real-world applications

---

## Strategy vs. Board

### What parts of your plan went as expected?

- Successfully identified a substantial dataset (29,767 emails) suitable for linguistic analysis
- Documented dataset characteristics, sources, and limitations comprehensively
- Established clear connection between data and research questions
- Created organized storage structure for raw and processed data

### What parts of your plan did not work out?

- Limited options for current/contemporary phishing data
- Inability to obtain user behavior data (click-through rates) as originally planned
- Corporate email context limits generalizability to personal email patterns
- Single language (English) constraint limits global applicability

### Did you need to add things that weren't in your strategy?

- Extended dataset evaluation process to assess multiple options
- Additional documentation for data preprocessing requirements
- Risk assessment for using historical vs. contemporary data
- Evaluation of dataset representativeness and bias considerations

### Or remove extra steps?

- Removed plans for real-time data collection due to ethical and technical constraints
- Simplified multi-dataset approach to focus on single high-quality source
- Eliminated cross-platform data collection (email, SMS, social media)

---

## Individual Retrospectives

### Team Data Collection Efforts

The team collaboratively evaluated multiple phishing datasets including:

- Enron email dataset with phishing labels
- Academic phishing research datasets
- Public cybersecurity datasets

**Key contributions:**

- Systematic evaluation of data quality and research fit
- Comprehensive documentation of selected dataset
- Clear articulation of data limitations and their implications
- Establishment of data handling and storage protocols

---

## Technical Challenges Overcome

1. **Data Format Standardization** - Converted various data formats into consistent structure
2. **Quality Assessment** - Developed criteria for evaluating dataset suitability
3. **Documentation Standards** - Created comprehensive data documentation template
4. **Ethical Considerations** - Established guidelines for handling sensitive email data

---

## Impact on Next Milestones

This data collection phase established:

- Clear understanding of available data for analysis
- Realistic scope for linguistic feature extraction
- Foundation for reproducible data preparation pipeline
- Awareness of limitations that will inform result interpretation
- Data structure that supports planned analytical approaches
