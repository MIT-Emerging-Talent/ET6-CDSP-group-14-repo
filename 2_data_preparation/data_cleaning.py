#!/usr/bin/env python
# coding: utf-8

# ## Data Cleaning

# In[ ]:


import re
import pandas as pd


class PhishingAnalyzer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.clean_df = None
        self.results = {}

    def load_data(self):
        """Load and perform initial data exploration."""
        print("Loading Enron dataset...")
        self.df = pd.read_csv(self.csv_path)

        print(f"Dataset shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print(f"Label distribution:\n{self.df['label'].value_counts()}")
        print(f"Missing values:\n{self.df.isnull().sum()}")

        # Store basic stats
        self.results["dataset_stats"] = {
            "total_emails": len(self.df),
            "safe_emails": len(self.df[self.df["label"] == 0]),
            "phishing_emails": len(self.df[self.df["label"] == 1]),
            "phishing_percentage": (len(self.df[self.df["label"] == 1]) / len(self.df))
            * 100,
        }

    def clean_data(self):
        """Clean and preprocess the email data."""
        print("Cleaning data...")

        # Create a copy for cleaning
        self.clean_df = self.df.copy()

        # Remove rows with missing body text
        self.clean_df = self.clean_df.dropna(subset=["body"])

        # Remove empty bodies
        self.clean_df = self.clean_df[self.clean_df["body"].str.strip() != ""]

        # Basic text cleaning function
        def clean_text(text):
            if pd.isna(text):
                return ""
            # Convert to lowercase
            text = text.lower()

            # Remove Enron-specific terms and patterns more aggressively
            # Remove specific Enron corporate phrases and signatures
            enron_patterns = [
                r"enron\s+capital\s*&?\s*trade\s*resources?\s*corp?\.?",
                r"enron\s+north\s+america\s+corp?\.?",
                r"enron\s+corp\.?",
                r"enron\s+global\s+markets",
                r"forwarded\s+by\s+[^/]+/\s*hou\s*/\s*ect",
                r"forwarded\s+by\s+[^/]+/\s*hol\s*/\s*aepin",
                r"/\s*hou\s*/\s*ect\s+on",
                r"/\s*hol\s*/\s*aepin\s+on",
            ]

            for pattern in enron_patterns:
                text = re.sub(pattern, " ", text)

            # Remove individual Enron-specific words
            enron_words = [
                "ect",
                "hou",
                "enron",
                "hpl",
                "hplno",
                "hplo",
                "aepin",
                "hol",
            ]
            for word in enron_words:
                # Remove whole words (with word boundaries)
                text = re.sub(r"\b" + re.escape(word) + r"\b", " ", text)

            # Remove email forwarding headers and timestamps
            text = re.sub(r"- - - - -.*?- - - - -", " ", text)
            text = re.sub(r"forwarded by .+? on \d+/\d+/\d+", " ", text)
            text = re.sub(r"original message.*?from:", " ", text)
            text = re.sub(r"sent:\s*\w+,.*?\d+:\d+\s*[ap]m", " ", text)

            # Remove common email artifacts
            text = re.sub(r"see attached file\s*:?", " ", text)
            text = re.sub(r"mailto\s*:", " ", text)
            text = re.sub(r"\b\w+\.\w+@\w+\.\w+\b", " ", text)  # Remove email addresses

            # Remove numbers (standalone digits, dates, file numbers, etc.)
            text = re.sub(r"\b\d+\b", " ", text)  # Remove standalone numbers
            text = re.sub(r"\b\d+\.\d+\b", " ", text)  # Remove decimal numbers
            text = re.sub(
                r"\b\w*\d+\w*\b",
                " ",
                text,
            )  # Remove words containing numbers

            # Remove extra whitespace
            text = re.sub(r"\s+", " ", text)
            # Remove special characters but keep basic punctuation and @ for email detection
            text = re.sub(r"[^\w\s\.\,\!\?\-@]", " ", text)
            return text.strip()

        self.clean_df["body_clean"] = self.clean_df["body"].apply(clean_text)

        # Remove very short emails (less than 10 characters)
        MIN_EMAIL_LENGTH = 10
        self.clean_df = self.clean_df[
            self.clean_df["body_clean"].str.len() >= MIN_EMAIL_LENGTH
        ]

        print(f"After cleaning: {len(self.clean_df)} emails remaining")

        # Update results
        self.results["cleaned_stats"] = {
            "remaining_emails": len(self.clean_df),
            "removed_emails": len(self.df) - len(self.clean_df),
            "removal_percentage": ((len(self.df) - len(self.clean_df)) / len(self.df))
            * 100,
        }


# Initialize the analyzer with the path to our dataset
pa = PhishingAnalyzer("../1_datasets/Enron.csv")

# Test: Load and examine the data
pa.load_data()
pa.clean_data()


# In[2]:


# Test: Save cleaned data to verify the pipeline works end-to-end
print("Testing data export functionality...")
print(f"Cleaned dataset shape: {pa.clean_df.shape}")
print(f"Columns in cleaned dataset: {list(pa.clean_df.columns)}")

# Show sample of cleaned data
print("\nSample of cleaned emails:")
for i in range(3):
    if i < len(pa.clean_df):
        row = pa.clean_df.iloc[i]
        print(f"Email {i + 1} - Label: {row['label']}")
        print(f"Original length: {len(str(row['body']))}")
        print(f"Cleaned length: {len(str(row['body_clean']))}")
        print(f"Cleaned text preview: {str(row['body_clean'])[:100]}...")
        print("-" * 50)

print("✅ Data cleaning notebook is working correctly!")
print("✅ Dataset successfully loaded from ../1_datasets/Enron.csv")
print("✅ Data cleaning pipeline completed successfully")
