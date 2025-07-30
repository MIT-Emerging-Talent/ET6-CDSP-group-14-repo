#!/usr/bin/env python3
"""
Phishing Email Analysis Project
===============================
Comprehensive analysis of phishing vs safe emails using the Enron dataset.
This script performs comparative analysis to uncover patterns and language tactics used by phishers.
"""

import os
import re
import string
import warnings

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from scipy.stats import ttest_ind
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from textstat import flesch_kincaid_grade, flesch_reading_ease, gunning_fog

warnings.filterwarnings("ignore")

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("vader_lexicon")
except LookupError:
    nltk.download("vader_lexicon")


class PhishingAnalyzer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.clean_df = None
        self.tfidf_vectorizer = None
        self.results = {}

    def load_data(self):
        """Load and perform initial data exploration"""
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
        self.clean_df = self.df.copy()

    def calculate_basic_features(self):
        """Calculate basic text features for each email"""
        print("Calculating basic text features...")

        def get_text_features(text):
            words = word_tokenize(text.lower())
            sentences = sent_tokenize(text)

            # Basic counts
            word_count = len(words)
            sentence_count = len(sentences)
            char_count = len(text)

            # Type-token ratio (vocabulary richness)
            unique_words = len(set(words))
            type_token_ratio = unique_words / word_count if word_count > 0 else 0

            # Average lengths
            avg_word_length = np.mean([len(word) for word in words]) if words else 0
            avg_sentence_length = (
                word_count / sentence_count if sentence_count > 0 else 0
            )

            # Punctuation analysis (replacing uppercase ratio)
            exclamation_count = text.count("!")
            question_count = text.count("?")
            dot_count = text.count(".")
            comma_count = text.count(",")

            # Punctuation ratios
            exclamation_ratio = exclamation_count / char_count if char_count > 0 else 0
            question_ratio = question_count / char_count if char_count > 0 else 0
            punctuation_density = (
                (exclamation_count + question_count + dot_count + comma_count)
                / char_count
                if char_count > 0
                else 0
            )

            # Special characters
            special_char_count = sum(1 for char in text if char in string.punctuation)
            special_char_ratio = (
                special_char_count / char_count if char_count > 0 else 0
            )

            # URL and email patterns (accounting for spaces in cleaned text)
            # Look for http/https patterns with potential spaces
            url_patterns = [
                r"http\s*:\s*/\s*/\s*[a-zA-Z0-9\s\.-]+",  # http://domain.com with spaces
                r"https\s*:\s*/\s*/\s*[a-zA-Z0-9\s\.-]+",  # https://domain.com with spaces
                r"http\s+[a-zA-Z0-9\s\.-]+\s*\.\s*[a-zA-Z]{2,}",  # http domain.com with spaces
                r"www\s*\.\s*[a-zA-Z0-9\s\.-]+\s*\.\s*[a-zA-Z]{2,}",  # www.domain.com with spaces
            ]

            url_count = 0
            for pattern in url_patterns:
                url_count += len(re.findall(pattern, text, re.IGNORECASE))

            # Email count - simply count @ symbols (much more reliable)
            email_pattern_count = text.count("@")

            # Readability scores
            try:
                flesch_score = flesch_reading_ease(text)
                flesch_grade = flesch_kincaid_grade(text)
                fog_index = gunning_fog(text)
            except Exception:
                flesch_score = flesch_grade = fog_index = 0

            return {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "char_count": char_count,
                "type_token_ratio": type_token_ratio,
                "avg_word_length": avg_word_length,
                "avg_sentence_length": avg_sentence_length,
                "exclamation_count": exclamation_count,
                "question_count": question_count,
                "exclamation_ratio": exclamation_ratio,
                "question_ratio": question_ratio,
                "punctuation_density": punctuation_density,
                "special_char_ratio": special_char_ratio,
                "url_count": url_count,
                "email_pattern_count": email_pattern_count,
                "flesch_score": flesch_score,
                "flesch_grade": flesch_grade,
                "fog_index": fog_index,
            }

        # Apply feature extraction
        features = self.clean_df["body_clean"].apply(get_text_features)
        feature_df = pd.DataFrame(list(features))

        # Combine with original data
        self.clean_df = pd.concat(
            [self.clean_df.reset_index(drop=True), feature_df], axis=1
        )

    def analyze_sentiment(self):
        """Perform sentiment analysis"""
        print("Analyzing sentiment...")

        sia = SentimentIntensityAnalyzer()

        def get_sentiment(text):
            scores = sia.polarity_scores(text)
            return scores

        sentiment_data = self.clean_df["body_clean"].apply(get_sentiment)
        sentiment_df = pd.DataFrame(list(sentiment_data))

        # Add sentiment columns
        for col in ["neg", "neu", "pos", "compound"]:
            self.clean_df[f"sentiment_{col}"] = sentiment_df[col]

    def analyze_psychological_words(self):
        """Analyze psychological manipulation words including fear, reward, urgency, action, and financial"""
        print("Analyzing psychological manipulation words...")

        urgency_words = [
            "urgent",
            "immediate",
            "asap",
            "hurry",
            "quickly",
            "fast",
            "expire",
            "expires",
            "deadline",
            "limited",
            "act now",
            "don't delay",
            "time sensitive",
            "emergency",
            "instant",
            "rush",
            "last chance",
            "final notice",
            "ending soon",
            "while supplies last",
        ]

        action_words = [
            "click",
            "download",
            "verify",
            "confirm",
            "update",
            "login",
            "sign in",
            "activate",
            "secure",
            "protect",
            "suspend",
            "block",
            "freeze",
            "submit",
            "register",
            "respond",
            "reply",
            "call now",
            "visit",
            "access",
            "open",
        ]

        financial_words = [
            "money",
            "bank",
            "account",
            "credit",
            "payment",
            "transfer",
            "withdraw",
            "deposit",
            "loan",
            "debt",
            "refund",
            "tax",
            "irs",
            "prize",
            "winner",
            "cash",
            "dollar",
            "earn",
            "profit",
            "investment",
            "savings",
            "mortgage",
        ]

        fear_words = [
            "warning",
            "alert",
            "danger",
            "risk",
            "threat",
            "compromised",
            "hacked",
            "stolen",
            "fraud",
            "scam",
            "unauthorized",
            "suspicious",
            "breach",
            "violation",
            "penalty",
            "consequences",
            "legal action",
            "lawsuit",
            "investigation",
            "arrest",
        ]

        reward_words = [
            "free",
            "bonus",
            "gift",
            "reward",
            "prize",
            "win",
            "winner",
            "lucky",
            "congratulations",
            "selected",
            "chosen",
            "exclusive",
            "special offer",
            "discount",
            "save",
            "deal",
            "promotion",
            "guarantee",
            "amazing",
        ]

        def count_words(text, word_list):
            text_lower = text.lower()
            return sum(1 for word in word_list if word in text_lower)

        self.clean_df["urgency_words"] = self.clean_df["body_clean"].apply(
            lambda x: count_words(x, urgency_words)
        )
        self.clean_df["action_words"] = self.clean_df["body_clean"].apply(
            lambda x: count_words(x, action_words)
        )
        self.clean_df["financial_words"] = self.clean_df["body_clean"].apply(
            lambda x: count_words(x, financial_words)
        )
        self.clean_df["fear_words"] = self.clean_df["body_clean"].apply(
            lambda x: count_words(x, fear_words)
        )
        self.clean_df["reward_words"] = self.clean_df["body_clean"].apply(
            lambda x: count_words(x, reward_words)
        )

    def perform_tfidf_analysis(self, max_features=1000):
        """Perform TF-IDF analysis to find important terms"""
        print("Performing TF-IDF analysis...")

        # Create TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=5,
            max_df=0.95,
        )

        # Fit and transform
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.clean_df["body_clean"])
        feature_names = self.tfidf_vectorizer.get_feature_names_out()

        # Separate by class
        phishing_mask = (self.clean_df["label"] == 1).values
        safe_mask = (self.clean_df["label"] == 0).values

        # Calculate mean TF-IDF scores for each class
        phishing_tfidf = tfidf_matrix[phishing_mask].mean(axis=0).A1
        safe_tfidf = tfidf_matrix[safe_mask].mean(axis=0).A1

        # Create feature importance dataframes
        tfidf_comparison = pd.DataFrame(
            {
                "feature": feature_names,
                "phishing_score": phishing_tfidf,
                "safe_score": safe_tfidf,
                "difference": phishing_tfidf - safe_tfidf,
            }
        )

        # Store top distinguishing features
        self.results["top_phishing_terms"] = tfidf_comparison.nlargest(
            20, "difference"
        )[["feature", "difference"]].to_dict("records")
        self.results["top_safe_terms"] = tfidf_comparison.nsmallest(20, "difference")[
            ["feature", "difference"]
        ].to_dict("records")

        return tfidf_matrix, tfidf_comparison

    def compare_classes(self):
        """Compare various metrics between phishing and safe emails"""
        print("Comparing phishing vs safe email characteristics...")

        numeric_columns = [
            "word_count",
            "sentence_count",
            "char_count",
            "type_token_ratio",
            "avg_word_length",
            "avg_sentence_length",
            "exclamation_ratio",
            "question_ratio",
            "punctuation_density",
            "special_char_ratio",
            "url_count",
            "email_pattern_count",
            "flesch_score",
            "flesch_grade",
            "fog_index",
            "sentiment_neg",
            "sentiment_neu",
            "sentiment_pos",
            "sentiment_compound",
            "urgency_words",
            "action_words",
            "financial_words",
            "fear_words",
            "reward_words",
        ]

        comparison_stats = {}

        for col in numeric_columns:
            if col in self.clean_df.columns:
                phishing_values = self.clean_df[self.clean_df["label"] == 1][
                    col
                ].dropna()
                safe_values = self.clean_df[self.clean_df["label"] == 0][col].dropna()

                # Calculate means and std
                phishing_mean = phishing_values.mean()
                phishing_std = phishing_values.std()
                safe_mean = safe_values.mean()
                safe_std = safe_values.std()

                # Effect size (Cohen's d)
                pooled_std = np.sqrt((phishing_values.var() + safe_values.var()) / 2)
                effect_size = (
                    (phishing_mean - safe_mean) / pooled_std if pooled_std > 0 else 0
                )

                stats_dict = {
                    "phishing_mean": phishing_mean,
                    "phishing_std": phishing_std,
                    "safe_mean": safe_mean,
                    "safe_std": safe_std,
                    "difference": phishing_mean - safe_mean,
                    "effect_size": effect_size,
                }

                # Compute 95% CI if effect size is medium or large
                if abs(effect_size) >= 0.5:
                    t_stat, p_val = ttest_ind(
                        phishing_values, safe_values, equal_var=False
                    )
                    # CI for difference of means
                    se_diff = np.sqrt(
                        phishing_values.var() / len(phishing_values)
                        + safe_values.var() / len(safe_values)
                    )
                    ci_low, ci_high = stats.t.interval(
                        0.95,
                        df=min(len(phishing_values), len(safe_values)) - 1,
                        loc=phishing_mean - safe_mean,
                        scale=se_diff,
                    )
                    stats_dict["95%_CI_difference"] = "({:.6f}, {:.6f})".format(
                        ci_low, ci_high
                    )
                    stats_dict["p_value"] = p_val

                comparison_stats[col] = stats_dict

        self.results["feature_comparison"] = comparison_stats
        return comparison_stats

    def create_individual_plots(self):
        print("Creating individual visualization plots...")

        # Create plots directory
        os.makedirs("plots", exist_ok=True)

        # Set up the plotting style
        plt.style.use("default")
        sns.set_palette("husl")

        # 1. Dataset Overview (Pie Chart)
        plt.figure(figsize=(10, 8))
        label_counts = self.clean_df["label"].value_counts()
        colors = ["#2E86AB", "#A23B72"]
        wedges, texts, autotexts = plt.pie(
            label_counts.values,
            labels=["Safe Emails", "Phishing Emails"],
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            textprops={"fontsize": 14},
        )
        plt.title(
            "Email Distribution: Safe vs Phishing",
            fontsize=18,
            fontweight="bold",
            pad=20,
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
        plt.savefig("plots/01_dataset_overview.png", dpi=300, bbox_inches="tight")
        plt.close()

        # 2. Enhanced Sentiment Analysis
        self._create_sentiment_plot()

        # 3. Psychological Manipulation Radar Chart
        self._create_radar_chart()

        # 4. Text Complexity Comparison
        self._create_text_complexity_plot()

        # 5. Punctuation Analysis
        self._create_punctuation_analysis()

        # 6. TF-IDF Term Analysis
        self._create_tfidf_plots()

        # 7. Feature Importance
        self._create_feature_importance_plot()

        # 8. Readability Scores
        self._create_readability_plot()

        # 9. URL and Email Pattern Analysis
        self._create_url_email_plot()

        # 10. Enhanced Boxplot Comparison
        self._create_enhanced_boxplot_comparison()

        print("Individual plots saved in 'plots/' directory!")

    def _create_sentiment_plot(self):
        """Create enhanced sentiment analysis plot"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # 1. Sentiment distribution comparison
        sentiment_cols = ["sentiment_neg", "sentiment_neu", "sentiment_pos"]
        sentiment_means = self.clean_df.groupby("label")[sentiment_cols].mean()

        x = np.arange(len(sentiment_cols))
        width = 0.35

        safe_means = sentiment_means.loc[0]
        phishing_means = sentiment_means.loc[1]

        ax1.bar(
            x - width / 2,
            safe_means,
            width,
            label="Safe Emails",
            color="#2E86AB",
            alpha=0.8,
        )
        ax1.bar(
            x + width / 2,
            phishing_means,
            width,
            label="Phishing Emails",
            color="#A23B72",
            alpha=0.8,
        )

        ax1.set_xlabel("Sentiment Type", fontweight="bold")
        ax1.set_ylabel("Average Score", fontweight="bold")
        ax1.set_title("Average Sentiment Scores by Email Type", fontweight="bold")
        ax1.set_xticks(x)
        ax1.set_xticklabels(["Negative", "Neutral", "Positive"])
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Compound sentiment distribution
        for label, color, name in [(0, "#2E86AB", "Safe"), (1, "#A23B72", "Phishing")]:
            data = self.clean_df[self.clean_df["label"] == label]["sentiment_compound"]
            ax2.hist(
                data,
                bins=30,
                alpha=0.7,
                label=f"{name} Emails",
                color=color,
                density=True,
            )

        ax2.set_xlabel("Compound Sentiment Score", fontweight="bold")
        ax2.set_ylabel("Density", fontweight="bold")
        ax2.set_title("Distribution of Compound Sentiment Scores", fontweight="bold")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. Sentiment correlation heatmap
        sentiment_data = self.clean_df[
            [
                "sentiment_neg",
                "sentiment_neu",
                "sentiment_pos",
                "sentiment_compound",
                "label",
            ]
        ]
        corr_matrix = sentiment_data.corr()
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="RdBu_r",
            center=0,
            ax=ax3,
            square=True,
            cbar_kws={"shrink": 0.8},
        )
        ax3.set_title("Sentiment Feature Correlation Matrix", fontweight="bold")

        # 4. Enhanced Box plot comparison
        sentiment_melted = pd.melt(
            self.clean_df,
            id_vars=["label"],
            value_vars=["sentiment_neg", "sentiment_neu", "sentiment_pos"],
            var_name="sentiment_type",
            value_name="score",
        )
        sentiment_melted["sentiment_type"] = sentiment_melted[
            "sentiment_type"
        ].str.replace("sentiment_", "")
        sentiment_melted["label"] = sentiment_melted["label"].map(
            {0: "Safe", 1: "Phishing"}
        )

        sns.boxplot(
            data=sentiment_melted,
            x="sentiment_type",
            y="score",
            hue="label",
            ax=ax4,
            palette=["#2E86AB", "#A23B72"],
            width=0.8,
        )
        ax4.set_xlabel("Sentiment Type", fontweight="bold", fontsize=12)
        ax4.set_ylabel("Score", fontweight="bold", fontsize=12)
        ax4.set_title(
            "Sentiment Score Distribution by Email Type", fontweight="bold", fontsize=14
        )
        ax4.grid(True, alpha=0.3, axis="y")
        ax4.tick_params(labelsize=11)
        ax4.legend(title="Email Type", title_fontsize=11, fontsize=10)

        plt.tight_layout()
        plt.savefig("plots/02_sentiment_analysis.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_radar_chart(self):
        """Create side-by-side radar charts for psychological manipulation tactics"""
        # Calculate means for each category
        psych_categories = [
            "urgency_words",
            "action_words",
            "financial_words",
            "fear_words",
            "reward_words",
        ]

        safe_means = []
        phishing_means = []

        for category in psych_categories:
            safe_mean = self.clean_df[self.clean_df["label"] == 0][category].mean()
            phishing_mean = self.clean_df[self.clean_df["label"] == 1][category].mean()
            safe_means.append(safe_mean)
            phishing_means.append(phishing_mean)

        # Use raw values without normalization
        # Setup side-by-side radar charts
        fig = plt.figure(figsize=(16, 8))

        # Categories for labels
        categories = [
            "Urgency\nWords",
            "Action\nWords",
            "Financial\nWords",
            "Fear\nWords",
            "Reward\nWords",
        ]
        N = len(categories)

        # Angles for each category
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle

        # Add values to complete the circle
        safe_plot = safe_means + safe_means[:1]
        phishing_plot = phishing_means + phishing_means[:1]

        # Calculate max value for consistent scaling
        max_val = max(max(safe_means), max(phishing_means))

        # Left subplot - Safe Emails
        ax1 = fig.add_subplot(121, projection="polar")
        ax1.plot(angles, safe_plot, "o-", linewidth=3, color="#2E86AB")
        ax1.fill(angles, safe_plot, alpha=0.3, color="#2E86AB")

        # Customize left chart
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(categories, fontsize=11, fontweight="bold")
        ax1.set_ylim(0, max_val * 1.1)
        # Create dynamic y-ticks based on max value
        tick_interval = max_val / 4
        y_ticks = [tick_interval * i for i in range(1, 5)]
        ax1.set_yticks(y_ticks)
        ax1.set_yticklabels([f"{tick:.3f}" for tick in y_ticks], fontsize=9)
        ax1.grid(True)
        ax1.set_title(
            "Safe Emails\nPsychological Word Usage", size=14, fontweight="bold", pad=30
        )

        # Right subplot - Phishing Emails
        ax2 = fig.add_subplot(122, projection="polar")
        ax2.plot(angles, phishing_plot, "o-", linewidth=3, color="#A23B72")
        ax2.fill(angles, phishing_plot, alpha=0.3, color="#A23B72")

        # Customize right chart
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(categories, fontsize=11, fontweight="bold")
        ax2.set_ylim(0, max_val * 1.1)
        ax2.set_yticks(y_ticks)
        ax2.set_yticklabels([f"{tick:.3f}" for tick in y_ticks], fontsize=9)
        ax2.grid(True)
        ax2.set_title(
            "Phishing Emails\nPsychological Word Usage",
            size=14,
            fontweight="bold",
            pad=30,
        )

        # Overall title
        fig.suptitle(
            "Psychological Manipulation Tactics Comparison\n(Raw Average Word Counts)",
            size=16,
            fontweight="bold",
            y=0.95,
        )

        plt.tight_layout()
        plt.savefig("plots/03_psychological_radar.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_text_complexity_plot(self):
        """Create text complexity analysis plot"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))

        # Create a copy with string labels for better visualization
        plot_df = self.clean_df.copy()
        plot_df["email_type"] = plot_df["label"].map({0: "Safe", 1: "Phishing"})

        # 1. Word count comparison
        safe_words = self.clean_df[self.clean_df["label"] == 0]["word_count"]
        phishing_words = self.clean_df[self.clean_df["label"] == 1]["word_count"]

        ax1.hist(
            safe_words,
            bins=50,
            alpha=0.7,
            label="Safe Emails",
            color="#2E86AB",
            density=True,
        )
        ax1.hist(
            phishing_words,
            bins=50,
            alpha=0.7,
            label="Phishing Emails",
            color="#A23B72",
            density=True,
        )
        ax1.set_xlabel("Word Count", fontweight="bold", fontsize=12)
        ax1.set_ylabel("Density", fontweight="bold", fontsize=12)
        ax1.set_title("Word Count Distribution", fontweight="bold", fontsize=14)
        ax1.legend(fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 1000)  # Focus on reasonable range

        # 2. Type-token ratio - Enhanced boxplot
        sns.boxplot(
            data=plot_df,
            x="email_type",
            y="type_token_ratio",
            ax=ax2,
            palette=["#2E86AB", "#A23B72"],
            width=0.6,
        )
        ax2.set_xlabel("Email Type", fontweight="bold", fontsize=12)
        ax2.set_ylabel("Type-Token Ratio", fontweight="bold", fontsize=12)
        ax2.set_title(
            "Vocabulary Richness (Type-Token Ratio)", fontweight="bold", fontsize=14
        )
        ax2.grid(True, alpha=0.3, axis="y")
        ax2.tick_params(labelsize=11)

        # 3. Average word length - Enhanced boxplot
        sns.boxplot(
            data=plot_df,
            x="email_type",
            y="avg_word_length",
            ax=ax3,
            palette=["#2E86AB", "#A23B72"],
            width=0.6,
        )
        ax3.set_xlabel("Email Type", fontweight="bold", fontsize=12)
        ax3.set_ylabel("Average Word Length", fontweight="bold", fontsize=12)
        ax3.set_title(
            "Average Word Length Distribution", fontweight="bold", fontsize=14
        )
        ax3.grid(True, alpha=0.3, axis="y")
        ax3.tick_params(labelsize=11)

        # 4. Average sentence length - Enhanced boxplot
        sns.boxplot(
            data=plot_df,
            x="email_type",
            y="avg_sentence_length",
            ax=ax4,
            palette=["#2E86AB", "#A23B72"],
            width=0.6,
        )
        ax4.set_xlabel("Email Type", fontweight="bold", fontsize=12)
        ax4.set_ylabel("Average Sentence Length", fontweight="bold", fontsize=12)
        ax4.set_title(
            "Average Sentence Length Distribution", fontweight="bold", fontsize=14
        )
        ax4.grid(True, alpha=0.3, axis="y")
        ax4.tick_params(labelsize=11)

        # Add median values as text annotations
        for ax, column in zip(
            [ax2, ax3, ax4],
            ["type_token_ratio", "avg_word_length", "avg_sentence_length"],
        ):
            safe_median = plot_df[plot_df["label"] == 0][column].median()
            phishing_median = plot_df[plot_df["label"] == 1][column].median()
            ax.text(
                0,
                safe_median,
                f"Med: {safe_median:.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#2E86AB", alpha=0.7),
            )
            ax.text(
                1,
                phishing_median,
                f"Med: {phishing_median:.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#A23B72", alpha=0.7),
            )

        plt.tight_layout()
        plt.savefig("plots/04_text_complexity.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_punctuation_analysis(self):
        """Create punctuation analysis plot"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # 1. Exclamation marks
        excl_means = self.clean_df.groupby("label")["exclamation_ratio"].mean()
        ax1.bar(
            ["Safe Emails", "Phishing Emails"],
            excl_means.values,
            color=["#2E86AB", "#A23B72"],
            alpha=0.8,
        )
        ax1.set_ylabel("Average Exclamation Ratio", fontweight="bold")
        ax1.set_title("Exclamation Mark Usage", fontweight="bold")
        ax1.grid(True, alpha=0.3)

        # 2. Question marks
        quest_means = self.clean_df.groupby("label")["question_ratio"].mean()
        ax2.bar(
            ["Safe Emails", "Phishing Emails"],
            quest_means.values,
            color=["#2E86AB", "#A23B72"],
            alpha=0.8,
        )
        ax2.set_ylabel("Average Question Mark Ratio", fontweight="bold")
        ax2.set_title("Question Mark Usage", fontweight="bold")
        ax2.grid(True, alpha=0.3)

        # 3. Overall punctuation density
        punct_means = self.clean_df.groupby("label")["punctuation_density"].mean()
        ax3.bar(
            ["Safe Emails", "Phishing Emails"],
            punct_means.values,
            color=["#2E86AB", "#A23B72"],
            alpha=0.8,
        )
        ax3.set_ylabel("Average Punctuation Density", fontweight="bold")
        ax3.set_title("Overall Punctuation Usage", fontweight="bold")
        ax3.grid(True, alpha=0.3)

        # 4. Punctuation comparison heatmap
        punct_features = [
            "exclamation_ratio",
            "question_ratio",
            "punctuation_density",
            "special_char_ratio",
        ]
        punct_comparison = self.clean_df.groupby("label")[punct_features].mean()
        sns.heatmap(
            punct_comparison,
            annot=True,
            cmap="YlOrRd",
            ax=ax4,
            cbar_kws={"shrink": 0.8},
        )
        ax4.set_title("Punctuation Features by Email Type", fontweight="bold")
        ax4.set_yticklabels(["Safe", "Phishing"], rotation=0)

        plt.tight_layout()
        plt.savefig("plots/05_punctuation_analysis.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_tfidf_plots(self):
        """Create TF-IDF analysis plots"""
        if "top_phishing_terms" not in self.results:
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

        # Top phishing terms
        phishing_terms = pd.DataFrame(self.results["top_phishing_terms"][:15])
        bars1 = ax1.barh(
            range(len(phishing_terms)),
            phishing_terms["difference"],
            color="#A23B72",
            alpha=0.8,
        )
        ax1.set_yticks(range(len(phishing_terms)))
        ax1.set_yticklabels(phishing_terms["feature"], fontsize=12)
        ax1.set_title(
            "Top Terms Associated with Phishing Emails", fontsize=16, fontweight="bold"
        )
        ax1.set_xlabel("TF-IDF Difference Score", fontweight="bold")
        ax1.grid(True, alpha=0.3)

        # Add value labels on bars
        for i, bar in enumerate(bars1):
            width = bar.get_width()
            ax1.text(
                width + 0.001,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.3f}",
                ha="left",
                va="center",
                fontweight="bold",
            )

        # Top safe terms
        safe_terms = pd.DataFrame(self.results["top_safe_terms"][:15])
        safe_terms["difference"] = safe_terms["difference"].abs()
        bars2 = ax2.barh(
            range(len(safe_terms)), safe_terms["difference"], color="#2E86AB", alpha=0.8
        )
        ax2.set_yticks(range(len(safe_terms)))
        ax2.set_yticklabels(safe_terms["feature"], fontsize=12)
        ax2.set_title(
            "Top Terms Associated with Safe Emails", fontsize=16, fontweight="bold"
        )
        ax2.set_xlabel("TF-IDF Difference Score (Absolute)", fontweight="bold")
        ax2.grid(True, alpha=0.3)

        # Add value labels on bars
        for i, bar in enumerate(bars2):
            width = bar.get_width()
            ax2.text(
                width + 0.001,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.3f}",
                ha="left",
                va="center",
                fontweight="bold",
            )

        plt.tight_layout()
        plt.savefig("plots/06_tfidf_analysis.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_feature_importance_plot(self):
        """Create feature importance plot from classification model"""
        if "model_performance" not in self.results:
            return

        importance_data = self.results["model_performance"]["feature_importance"]
        importance_df = pd.DataFrame(
            list(importance_data.items()), columns=["feature", "importance"]
        ).sort_values("importance", ascending=True)

        plt.figure(figsize=(12, 10))
        bars = plt.barh(
            importance_df["feature"],
            importance_df["importance"],
            color="#F18F01",
            alpha=0.8,
        )
        plt.xlabel("Feature Importance Score", fontweight="bold", fontsize=14)
        plt.ylabel("Features", fontweight="bold", fontsize=14)
        plt.title(
            "Feature Importance in Phishing Detection Model",
            fontweight="bold",
            fontsize=16,
        )
        plt.grid(True, alpha=0.3)

        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(
                width + 0.005,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.3f}",
                ha="left",
                va="center",
                fontweight="bold",
            )

        plt.tight_layout()
        plt.savefig("plots/07_feature_importance.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_readability_plot(self):
        """Create readability analysis plot"""
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 8))

        # Create a copy with string labels for better visualization
        plot_df = self.clean_df.copy()
        plot_df["email_type"] = plot_df["label"].map({0: "Safe", 1: "Phishing"})

        # Flesch reading ease - Enhanced boxplot
        sns.boxplot(
            data=plot_df,
            x="email_type",
            y="flesch_score",
            ax=ax1,
            palette=["#2E86AB", "#A23B72"],
            width=0.6,
        )
        ax1.set_xlabel("Email Type", fontweight="bold", fontsize=12)
        ax1.set_ylabel("Flesch Reading Ease Score", fontweight="bold", fontsize=12)
        ax1.set_title(
            "Flesch Reading Ease\n(Higher = Easier to Read)",
            fontweight="bold",
            fontsize=14,
        )
        ax1.grid(True, alpha=0.3, axis="y")
        ax1.tick_params(labelsize=11)

        # Add median annotations
        safe_median = plot_df[plot_df["label"] == 0]["flesch_score"].median()
        phishing_median = plot_df[plot_df["label"] == 1]["flesch_score"].median()
        ax1.text(
            0,
            safe_median,
            f"Med: {safe_median:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#2E86AB", alpha=0.7),
        )
        ax1.text(
            1,
            phishing_median,
            f"Med: {phishing_median:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#A23B72", alpha=0.7),
        )

        # Flesch-Kincaid grade - Enhanced boxplot
        sns.boxplot(
            data=plot_df,
            x="email_type",
            y="flesch_grade",
            ax=ax2,
            palette=["#2E86AB", "#A23B72"],
            width=0.6,
        )
        ax2.set_xlabel("Email Type", fontweight="bold", fontsize=12)
        ax2.set_ylabel("Flesch-Kincaid Grade Level", fontweight="bold", fontsize=12)
        ax2.set_title(
            "Flesch-Kincaid Grade\n(Grade Level Required)",
            fontweight="bold",
            fontsize=14,
        )
        ax2.grid(True, alpha=0.3, axis="y")
        ax2.tick_params(labelsize=11)

        # Add median annotations
        safe_median = plot_df[plot_df["label"] == 0]["flesch_grade"].median()
        phishing_median = plot_df[plot_df["label"] == 1]["flesch_grade"].median()
        ax2.text(
            0,
            safe_median,
            f"Med: {safe_median:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#2E86AB", alpha=0.7),
        )
        ax2.text(
            1,
            phishing_median,
            f"Med: {phishing_median:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#A23B72", alpha=0.7),
        )

        # Gunning Fog Index - Enhanced boxplot
        sns.boxplot(
            data=plot_df,
            x="email_type",
            y="fog_index",
            ax=ax3,
            palette=["#2E86AB", "#A23B72"],
            width=0.6,
        )
        ax3.set_xlabel("Email Type", fontweight="bold", fontsize=12)
        ax3.set_ylabel("Gunning Fog Index", fontweight="bold", fontsize=12)
        ax3.set_title(
            "Gunning Fog Index\n(Reading Difficulty)", fontweight="bold", fontsize=14
        )
        ax3.grid(True, alpha=0.3, axis="y")
        ax3.tick_params(labelsize=11)

        # Add median annotations
        safe_median = plot_df[plot_df["label"] == 0]["fog_index"].median()
        phishing_median = plot_df[plot_df["label"] == 1]["fog_index"].median()
        ax3.text(
            0,
            safe_median,
            f"Med: {safe_median:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#2E86AB", alpha=0.7),
        )
        ax3.text(
            1,
            phishing_median,
            f"Med: {phishing_median:.1f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#A23B72", alpha=0.7),
        )

        plt.tight_layout()
        plt.savefig("plots/08_readability_analysis.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_url_email_plot(self):
        """Create URL and email pattern analysis plot"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # URL count comparison
        url_means = self.clean_df.groupby("label")["url_count"].mean()
        ax1.bar(
            ["Safe Emails", "Phishing Emails"],
            url_means.values,
            color=["#2E86AB", "#A23B72"],
            alpha=0.8,
        )
        ax1.set_ylabel("Average URL Count", fontweight="bold")
        ax1.set_title("URL Usage in Emails", fontweight="bold")
        ax1.grid(True, alpha=0.3)

        # Email pattern count comparison
        email_means = self.clean_df.groupby("label")["email_pattern_count"].mean()
        ax2.bar(
            ["Safe Emails", "Phishing Emails"],
            email_means.values,
            color=["#2E86AB", "#A23B72"],
            alpha=0.8,
        )
        ax2.set_ylabel("Average Email Pattern Count", fontweight="bold")
        ax2.set_title("Email Address Patterns in Content", fontweight="bold")
        ax2.grid(True, alpha=0.3)

        # URL count distribution
        safe_urls = self.clean_df[self.clean_df["label"] == 0]["url_count"]
        phishing_urls = self.clean_df[self.clean_df["label"] == 1]["url_count"]

        ax3.hist(
            safe_urls,
            bins=range(0, 6),
            alpha=0.7,
            label="Safe Emails",
            color="#2E86AB",
            density=True,
        )
        ax3.hist(
            phishing_urls,
            bins=range(0, 6),
            alpha=0.7,
            label="Phishing Emails",
            color="#A23B72",
            density=True,
        )
        ax3.set_xlabel("URL Count", fontweight="bold")
        ax3.set_ylabel("Density", fontweight="bold")
        ax3.set_title("Distribution of URL Counts", fontweight="bold")
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Combined technical features
        tech_features = ["url_count", "email_pattern_count"]
        tech_comparison = self.clean_df.groupby("label")[tech_features].mean()
        tech_comparison.plot(kind="bar", ax=ax4, color=["#F18F01", "#C73E1D"])
        ax4.set_xlabel("Email Type (0=Safe, 1=Phishing)", fontweight="bold")
        ax4.set_ylabel("Average Count", fontweight="bold")
        ax4.set_title("Technical Pattern Usage", fontweight="bold")
        ax4.legend(["URL Count", "Email Pattern Count"])
        ax4.grid(True, alpha=0.3)
        ax4.set_xticklabels(["Safe", "Phishing"], rotation=0)

        plt.tight_layout()
        plt.savefig("plots/09_url_email_patterns.png", dpi=300, bbox_inches="tight")
        plt.close()

    def _create_enhanced_boxplot_comparison(self):
        """Create a comprehensive, highly visible boxplot comparison of key features"""
        # Select the most important features for comparison
        key_features = [
            ("type_token_ratio", "Type-Token Ratio\n(Vocabulary Richness)"),
            ("avg_word_length", "Average Word Length\n(Characters)"),
            ("exclamation_ratio", "Exclamation Mark Ratio\n(! per character)"),
            ("punctuation_density", "Punctuation Density\n(All punctuation)"),
            ("sentiment_compound", "Sentiment Compound\n(Overall sentiment)"),
            ("urgency_words", "Urgency Words\n(Count per email)"),
            ("action_words", "Action Words\n(Count per email)"),
            ("financial_words", "Financial Words\n(Count per email)"),
            ("reward_words", "Reward Words\n(Count per email)"),
        ]

        # Create a large figure with 3x3 grid
        fig, axes = plt.subplots(3, 3, figsize=(22, 18))
        axes = axes.flatten()

        # Create a copy with string labels for better visualization
        plot_df = self.clean_df.copy()
        plot_df["email_type"] = plot_df["label"].map({0: "Safe", 1: "Phishing"})

        # Create boxplots for each feature
        for i, (feature, title) in enumerate(key_features):
            ax = axes[i]

            # Create enhanced boxplot
            box_plot = sns.boxplot(
                data=plot_df,
                x="email_type",
                y=feature,
                ax=ax,
                palette=["#2E86AB", "#A23B72"],
                width=0.7,
                showfliers=True,
                fliersize=3,
                linewidth=2,
            )

            # Enhance the styling
            ax.set_xlabel("Email Type", fontweight="bold", fontsize=14)
            ax.set_ylabel(
                feature.replace("_", " ").title(), fontweight="bold", fontsize=14
            )
            ax.set_title(title, fontweight="bold", fontsize=16, pad=20)
            ax.grid(True, alpha=0.3, axis="y")
            ax.tick_params(labelsize=12)

            # Add median values as annotations with better positioning
            safe_median = plot_df[plot_df["label"] == 0][feature].median()
            phishing_median = plot_df[plot_df["label"] == 1][feature].median()

            # Calculate y-position for annotations (slightly above the median line)
            y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
            annotation_offset = y_range * 0.05

            # Safe email annotation
            ax.text(
                0,
                safe_median + annotation_offset,
                f"Median: {safe_median:.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=11,
                bbox=dict(
                    boxstyle="round,pad=0.4",
                    facecolor="#2E86AB",
                    alpha=0.8,
                    edgecolor="white",
                    linewidth=2,
                ),
            )

            # Phishing email annotation
            ax.text(
                1,
                phishing_median + annotation_offset,
                f"Median: {phishing_median:.3f}",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=11,
                bbox=dict(
                    boxstyle="round,pad=0.4",
                    facecolor="#A23B72",
                    alpha=0.8,
                    edgecolor="white",
                    linewidth=2,
                ),
            )

            # Add difference indicator
            diff = phishing_median - safe_median
            diff_percent = (diff / safe_median * 100) if safe_median != 0 else 0
            diff_color = "#A23B72" if diff > 0 else "#2E86AB"
            diff_symbol = "↑" if diff > 0 else "↓"

            ax.text(
                0.5,
                ax.get_ylim()[1] * 0.9,
                f"{diff_symbol} {diff_percent:+.1f}%",
                ha="center",
                va="top",
                fontweight="bold",
                fontsize=12,
                bbox=dict(
                    boxstyle="round,pad=0.3",
                    facecolor=diff_color,
                    alpha=0.7,
                    edgecolor="white",
                    linewidth=1,
                ),
                transform=ax.transAxes,
            )

            # Enhance box plot colors
            for patch in box_plot.artists:
                patch.set_linewidth(2)

            # Make whiskers and caps thicker
            for line in ax.lines:
                line.set_linewidth(2)

        # Overall figure styling
        plt.suptitle(
            "Enhanced Boxplot Comparison: Key Features for Phishing Detection",
            fontsize=24,
            fontweight="bold",
            y=0.98,
        )

        # Add a subtitle with interpretation guide
        fig.text(
            0.5,
            0.94,
            "Higher values in phishing emails (↑) suggest feature importance for detection. "
            "Boxes show quartiles, whiskers show range, dots are outliers.",
            ha="center",
            va="top",
            fontsize=14,
            style="italic",
        )

        plt.tight_layout(rect=[0, 0, 1, 0.92])
        plt.savefig(
            "plots/10_enhanced_boxplot_comparison.png", dpi=300, bbox_inches="tight"
        )
        plt.close()

    def build_classification_model(self):
        """Build a simple classification model to validate our features"""
        print("Building classification model for feature validation...")

        # Select features for modeling
        feature_columns = [
            "word_count",
            "type_token_ratio",
            "flesch_score",
            "sentiment_compound",
            "urgency_words",
            "action_words",
            "financial_words",
            "fear_words",
            "reward_words",
            "exclamation_ratio",
            "question_ratio",
            "punctuation_density",
            "url_count",
        ]

        # Prepare data
        X = self.clean_df[feature_columns].fillna(0)
        y = self.clean_df["label"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Train Random Forest
        rf_model = RandomForestClassifier(
            n_estimators=100, random_state=42, max_depth=10
        )
        rf_model.fit(X_train, y_train)

        # Predictions
        y_pred = rf_model.predict(X_test)

        # Store results
        self.results["model_performance"] = {
            "classification_report": classification_report(
                y_test, y_pred, output_dict=True
            ),
            "feature_importance": dict(
                zip(feature_columns, rf_model.feature_importances_)
            ),
        }

        print("Classification Report:")
        print(classification_report(y_test, y_pred))

    def save_results(self):
        """Save comprehensive analysis results"""
        print("Saving analysis results...")

        # Create plots directory
        os.makedirs("plots", exist_ok=True)

        # Save cleaned dataset with all features
        self.clean_df.to_csv("1_datasets/phishing_analysis_dataset.csv")

        # Save detailed comparison statistics
        comparison_df = pd.DataFrame(self.results["feature_comparison"]).T
        comparison_df.to_csv("4_data_analysis/feature_comparison_stats.csv")

        # Save TF-IDF results
        if "top_phishing_terms" in self.results:
            pd.DataFrame(self.results["top_phishing_terms"]).to_csv(
                "4_data_analysis/top_phishing_terms.csv", index=False
            )
            pd.DataFrame(self.results["top_safe_terms"]).to_csv(
                "4_data_analysis/top_phishing_terms.csv", index=False
            )

        # Create comprehensive text report
        self._generate_text_report()

        print("Results saved successfully!")

    def _generate_text_report(self):
        """Generate a comprehensive text report of findings"""
        report = []
        report.append("ENHANCED PHISHING EMAIL ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")

        # Dataset overview
        report.append("DATASET OVERVIEW:")
        report.append(
            f"- Total emails analyzed: {self.results['dataset_stats']['total_emails']:,}"
        )
        report.append(
            f"- Safe emails: {self.results['dataset_stats']['safe_emails']:,}"
        )
        report.append(
            f"- Phishing emails: {self.results['dataset_stats']['phishing_emails']:,}"
        )
        report.append(
            f"- Phishing percentage: {self.results['dataset_stats']['phishing_percentage']:.2f}%"
        )
        report.append("")

        # Key findings
        report.append("KEY FINDINGS:")
        report.append("-" * 20)

        if "feature_comparison" in self.results:
            comp = self.results["feature_comparison"]

            # Most distinguishing features
            sorted_features = sorted(
                comp.items(),
                key=lambda x: abs(x[1]["effect_size"])
                if not np.isnan(x[1]["effect_size"])
                else 0,
                reverse=True,
            )

            report.append("Most distinguishing features (by effect size):")
            for feature, stats in sorted_features[:12]:
                effect_size = stats["effect_size"]
                if not np.isnan(effect_size):
                    direction = "higher" if stats["difference"] > 0 else "lower"
                    report.append(
                        f"- {feature}: Phishing emails have {direction} values (effect size: {effect_size:.3f})"
                    )
            report.append("")

            # Psychological manipulation insights
            psych_features = [
                "urgency_words",
                "action_words",
                "financial_words",
                "fear_words",
                "reward_words",
            ]
            report.append("PSYCHOLOGICAL MANIPULATION TACTICS:")
            for feature in psych_features:
                if feature in comp:
                    diff = comp[feature]["difference"]
                    report.append(
                        f"- {feature.replace('_', ' ').title()}: +{diff:.2f} average count in phishing emails"
                    )
            report.append("")

            # Punctuation insights
            report.append("PUNCTUATION USAGE PATTERNS:")
            punct_features = [
                "exclamation_ratio",
                "question_ratio",
                "punctuation_density",
            ]
            for feature in punct_features:
                if feature in comp:
                    diff = comp[feature]["difference"]
                    direction = "more" if diff > 0 else "less"
                    report.append(
                        f"- {feature.replace('_', ' ').title()}: {direction} usage in phishing emails ({diff:.4f} difference)"
                    )
            report.append("")

        # TF-IDF insights
        if "top_phishing_terms" in self.results:
            report.append("TOP PHISHING-ASSOCIATED TERMS:")
            for i, term_data in enumerate(self.results["top_phishing_terms"][:15], 1):
                report.append(
                    f"{i:2d}. {term_data['feature']} (score: {term_data['difference']:.4f})"
                )
            report.append("")

        # Model performance
        if "model_performance" in self.results:
            model_stats = self.results["model_performance"]["classification_report"]
            report.append("ENHANCED CLASSIFICATION MODEL PERFORMANCE:")
            report.append(f"- Overall Accuracy: {model_stats['accuracy']:.3f}")
            report.append(
                f"- Phishing Detection Precision: {model_stats['1']['precision']:.3f}"
            )
            report.append(
                f"- Phishing Detection Recall: {model_stats['1']['recall']:.3f}"
            )
            report.append(
                f"- Phishing Detection F1-Score: {model_stats['1']['f1-score']:.3f}"
            )
            report.append("")

            # Top important features
            feature_importance = self.results["model_performance"]["feature_importance"]
            sorted_importance = sorted(
                feature_importance.items(), key=lambda x: x[1], reverse=True
            )
            report.append("TOP PREDICTIVE FEATURES:")
            for feature, importance in sorted_importance[:8]:
                report.append(f"- {feature}: {importance:.3f}")

        report.append("")
        report.append("VISUALIZATION FILES CREATED:")
        report.append("- plots/01_dataset_overview.png")
        report.append("- plots/02_sentiment_analysis.png")
        report.append("- plots/03_psychological_radar.png")
        report.append("- plots/04_text_complexity.png")
        report.append("- plots/05_punctuation_analysis.png")
        report.append("- plots/06_tfidf_analysis.png")
        report.append("- plots/07_feature_importance.png")
        report.append("- plots/08_readability_analysis.png")
        report.append("- plots/09_url_email_patterns.png")
        report.append("- plots/10_enhanced_boxplot_comparison.png (NEW!)")

        # Save report
        with open("4_data_analysis/enhanced_phishing_analysis_report.txt", "w") as f:
            f.write("\n".join(report))

    def run_complete_analysis(self):
        """Run the complete enhanced analysis pipeline"""
        print("Starting enhanced comprehensive phishing email analysis...")
        print("=" * 70)
        # Remove garbage rows like ". xls" from analysis

        # Load and clean data
        self.load_data()
        # self.clean_data()

        # Calculate features
        self.calculate_basic_features()
        self.analyze_sentiment()
        self.analyze_psychological_words()

        # Perform analyses
        self.perform_tfidf_analysis()
        self.compare_classes()

        # Build validation model
        self.build_classification_model()

        # Create individual visualizations
        self.create_individual_plots()

        # Save all results
        self.save_results()

        print("=" * 70)
        print("Enhanced analysis complete! Check the generated files:")
        print("- phishing_analysis_dataset.csv: Complete dataset with all features")
        print("- plots/: Directory containing 10 individual visualization files")
        print("- enhanced_phishing_analysis_report.txt: Comprehensive text report")
        print("- Various CSV files with detailed statistics")
        print("\nVisualization files are ready for slideshow presentation!")
        print(
            "✨ NEW: Enhanced boxplot comparison (plots/10_enhanced_boxplot_comparison.png)!"
        )
        comparison_stats = self.compare_classes()
        pd.DataFrame.from_dict(comparison_stats, orient="index").to_csv(
            "4_data_analysis/feature_comparison_stats.csv"
        )


if __name__ == "__main__":
    # Initialize and run analysis
    analyzer = PhishingAnalyzer("1_datasets/Enron_cleaned.csv")
    analyzer.run_complete_analysis()
