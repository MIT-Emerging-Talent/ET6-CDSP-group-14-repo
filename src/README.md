# Source Code Directory

This directory contains all the Python scripts and Jupyter notebooks for the phishing email analysis project.

## 📁 Files

### Core Analysis Scripts

#### `phishing_analysis.py`

The main comprehensive analysis script that performs:

- Data loading and cleaning
- Feature extraction (linguistic, psychological, sentiment analysis)
- Statistical analysis with Cohen's d effect sizes
- TF-IDF analysis with length normalization
- Machine learning classification
- Visualization generation

**Usage:**

```bash
python phishing_analysis.py
```

#### `enhanced_statistical_report.py`

Dedicated statistical analysis script that adds:

- Statistical significance testing (t-tests)
- P-value calculations
- Confidence intervals
- Multiple comparison corrections
- Enhanced effect size visualizations

**Usage:**

```bash
python enhanced_statistical_report.py
```

#### `statistical_analysis.py`

Pure statistical analysis script for comprehensive testing:

- Advanced statistical testing
- Effect size analysis
- Statistical visualization
- Significance testing with corrections

**Usage:**

```bash
python statistical_analysis.py
```

#### `data_cleaning.py`

Data preprocessing script that handles:

- Text cleaning and normalization
- Removal of Enron-specific artifacts
- Email header cleaning
- Data validation and quality checks

**Usage:**

```bash
python data_cleaning.py
```

## 🛠️ Dependencies

Install required packages:

```bash
pip install -r ../requirements.txt
```

## 📊 Output Files

Running these scripts will generate:

- Statistical analysis CSV files → `../results/statistical_analysis/`
- Visualization plots → `../results/visualizations/`
- Analysis reports → `../results/reports/`

## 🔧 Configuration

Scripts are configured to use:

- **Input data**: `../1_datasets/Enron.csv`
- **Cleaned data**: `../1_datasets/Enron_cleaned.csv`
- **Output directories**: `../results/`

## 📝 Notes

- All scripts include proper error handling and progress indicators
- Statistical analysis follows rigorous standards with significance testing
- Visualizations are saved at publication quality (300 DPI)
- Scripts are optimized for the project's specific dataset structure
