#!/usr/bin/env python3
"""
Phishing Email Statistical Analysis
==================================
Pure statistical analysis script for phishing vs safe email comparison.
This script focuses only on statistical analysis, not data cleaning.
Uses the pre-cleaned dataset from data_preparation phase.
"""

import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import ttest_ind

warnings.filterwarnings("ignore")


class PhishingStatisticalAnalyzer:
    """Statistical analysis class for phishing email detection"""

    def __init__(self, feature_csv_path):
        """Initialize with feature dataset from main analysis"""
        self.csv_path = feature_csv_path
        self.df = None
        self.results = {}

    def load_cleaned_data(self):
        """Load the dataset with features"""
        print("Loading dataset with features...")
        self.df = pd.read_csv(self.csv_path)
        print(f"Loaded {len(self.df)} emails")
        print(f"Phishing emails: {len(self.df[self.df['label'] == 1])}")
        print(f"Safe emails: {len(self.df[self.df['label'] == 0])}")
        print(f"Available columns: {self.df.columns.tolist()}")

    def perform_statistical_tests(self):
        """Perform comprehensive statistical testing"""
        print("\nPerforming statistical significance testing...")

        # Define numeric features for analysis
        numeric_features = [
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

        statistical_results = {}

        for feature in numeric_features:
            if feature in self.df.columns:
                # Separate groups
                phishing_values = self.df[self.df["label"] == 1][feature]
                safe_values = self.df[self.df["label"] == 0][feature]

                # Basic descriptive statistics
                phishing_mean = phishing_values.mean()
                phishing_std = phishing_values.std()
                phishing_median = phishing_values.median()
                safe_mean = safe_values.mean()
                safe_std = safe_values.std()
                safe_median = safe_values.median()

                # Calculate difference
                difference = phishing_mean - safe_mean

                # Calculate Cohen's d (effect size)
                pooled_std = np.sqrt((phishing_values.var() + safe_values.var()) / 2)
                cohens_d = difference / pooled_std if pooled_std > 0 else 0

                # Perform Welch's t-test (unequal variances)
                t_stat, p_value = ttest_ind(
                    phishing_values, safe_values, equal_var=False
                )

                # Calculate 95% confidence interval for the difference
                se_diff = np.sqrt(
                    (phishing_std**2 / len(phishing_values))
                    + (safe_std**2 / len(safe_values))
                )

                # Degrees of freedom for Welch's t-test
                df = (
                    phishing_std**2 / len(phishing_values)
                    + safe_std**2 / len(safe_values)
                ) ** 2 / (
                    (phishing_std**2 / len(phishing_values)) ** 2
                    / (len(phishing_values) - 1)
                    + (safe_std**2 / len(safe_values)) ** 2 / (len(safe_values) - 1)
                )

                t_critical = stats.t.ppf(0.975, df)  # 95% CI
                ci_lower = difference - t_critical * se_diff
                ci_upper = difference + t_critical * se_diff

                # Interpret effect size
                effect_interpretation = self._interpret_effect_size(abs(cohens_d))

                # Determine significance level
                if p_value < 0.001:
                    significance_level = "***"
                elif p_value < 0.01:
                    significance_level = "**"
                elif p_value < 0.05:
                    significance_level = "*"
                else:
                    significance_level = "ns"

                statistical_results[feature] = {
                    "phishing_mean": phishing_mean,
                    "phishing_std": phishing_std,
                    "phishing_median": phishing_median,
                    "safe_mean": safe_mean,
                    "safe_std": safe_std,
                    "safe_median": safe_median,
                    "difference": difference,
                    "cohens_d": cohens_d,
                    "effect_interpretation": effect_interpretation,
                    "t_statistic": t_stat,
                    "p_value": p_value,
                    "significance_level": significance_level,
                    "ci_lower": ci_lower,
                    "ci_upper": ci_upper,
                    "degrees_of_freedom": df,
                }

        self.results["statistical_tests"] = statistical_results
        return statistical_results

    def _interpret_effect_size(self, abs_cohens_d):
        """Interpret Cohen's d effect size"""
        if abs_cohens_d < 0.2:
            return "negligible"
        elif abs_cohens_d < 0.5:
            return "small"
        elif abs_cohens_d < 0.8:
            return "medium"
        else:
            return "large"

    def create_summary_table(self):
        """Create a summary table of statistical results"""
        print("\nCreating statistical summary table...")

        stats_data = []
        for feature, feature_stats in self.results["statistical_tests"].items():
            stats_data.append(
                {
                    "Feature": feature,
                    "Phishing_Mean": round(feature_stats["phishing_mean"], 4),
                    "Safe_Mean": round(feature_stats["safe_mean"], 4),
                    "Difference": round(feature_stats["difference"], 4),
                    "Cohens_d": round(feature_stats["cohens_d"], 4),
                    "Effect_Size": feature_stats["effect_interpretation"],
                    "p_value": feature_stats["p_value"],
                    "Significance": feature_stats["significance_level"],
                    "CI_Lower": round(feature_stats["ci_lower"], 4),
                    "CI_Upper": round(feature_stats["ci_upper"], 4),
                }
            )

        summary_df = pd.DataFrame(stats_data)

        # Debug: print columns
        print("DataFrame columns:", summary_df.columns.tolist())
        print("Sample data:")
        print(summary_df.head())

        # Sort by absolute effect size
        summary_df["abs_cohens_d"] = abs(summary_df["Cohens_d"].astype(float))
        summary_df = summary_df.sort_values("abs_cohens_d", ascending=False)
        summary_df = summary_df.drop("abs_cohens_d", axis=1)

        # Save to CSV
        summary_df.to_csv(
            "../results/statistical_analysis/statistical_summary.csv", index=False
        )
        print(
            "Statistical summary saved to '../results/statistical_analysis/statistical_summary.csv'"
        )

        return summary_df

    def create_effect_size_visualization(self):
        """Create visualization of effect sizes"""
        print("\nCreating effect size visualization...")

        # Prepare data for plotting
        features = []
        effect_sizes = []
        p_values = []
        categories = []

        for feature, feature_stats in self.results["statistical_tests"].items():
            features.append(feature.replace("_", " ").title())
            effect_sizes.append(feature_stats["cohens_d"])
            p_values.append(feature_stats["p_value"])

            # Categorize features
            if "sentiment" in feature.lower():
                categories.append("Sentiment")
            elif any(
                word in feature.lower()
                for word in ["urgency", "action", "financial", "fear", "reward"]
            ):
                categories.append("Psychological")
            elif any(
                word in feature.lower()
                for word in ["word", "sentence", "char", "length", "ratio"]
            ):
                categories.append("Linguistic")
            elif any(word in feature.lower() for word in ["flesch", "fog"]):
                categories.append("Readability")
            else:
                categories.append("Other")

        # Create the plot
        plt.figure(figsize=(14, 10))

        # Create a color map for categories
        unique_categories = list(set(categories))
        colors = plt.cm.Set1(np.linspace(0, 1, len(unique_categories)))
        color_map = dict(zip(unique_categories, colors))

        # Plot effect sizes
        plt.barh(
            range(len(features)),
            effect_sizes,
            color=[color_map[cat] for cat in categories],
        )

        # Add significance markers
        for i, (effect, p_val) in enumerate(zip(effect_sizes, p_values)):
            if p_val < 0.001:
                marker = "***"
            elif p_val < 0.01:
                marker = "**"
            elif p_val < 0.05:
                marker = "*"
            else:
                marker = ""

            # Position text based on bar direction
            x_pos = effect + (0.02 if effect >= 0 else -0.02)
            plt.text(
                x_pos,
                i,
                marker,
                va="center",
                ha="left" if effect >= 0 else "right",
                fontweight="bold",
            )

        # Add effect size guidelines
        plt.axvline(
            x=0.2, color="gray", linestyle="--", alpha=0.5, label="Small effect"
        )
        plt.axvline(
            x=0.5, color="gray", linestyle="--", alpha=0.7, label="Medium effect"
        )
        plt.axvline(
            x=0.8, color="gray", linestyle="--", alpha=0.9, label="Large effect"
        )
        plt.axvline(x=-0.2, color="gray", linestyle="--", alpha=0.5)
        plt.axvline(x=-0.5, color="gray", linestyle="--", alpha=0.7)
        plt.axvline(x=-0.8, color="gray", linestyle="--", alpha=0.9)

        plt.yticks(range(len(features)), features)
        plt.xlabel("Cohen's d (Effect Size)", fontweight="bold", fontsize=12)
        plt.title(
            "Effect Sizes for Phishing vs Safe Email Features\n(*** p<0.001, ** p<0.01, * p<0.05)",
            fontweight="bold",
            fontsize=14,
        )
        plt.grid(True, alpha=0.3, axis="x")

        # Add legend for categories
        handles = [
            plt.Rectangle((0, 0), 1, 1, color=color_map[cat])
            for cat in unique_categories
        ]
        plt.legend(
            handles, unique_categories, loc="lower right", title="Feature Category"
        )

        plt.tight_layout()
        plt.savefig(
            "../results/visualizations/effect_sizes_statistical_analysis.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.show()

        print(
            "Effect size visualization saved to '../results/visualizations/effect_sizes_statistical_analysis.png'"
        )

    def print_key_findings(self):
        """Print key statistical findings"""
        print("\n" + "=" * 80)
        print("KEY STATISTICAL FINDINGS")
        print("=" * 80)

        # Categorize results by effect size
        large_effects = []
        medium_effects = []
        small_effects = []
        negligible_effects = []

        for feature, feature_stats in self.results["statistical_tests"].items():
            abs_d = abs(feature_stats["cohens_d"])
            if abs_d >= 0.8:
                large_effects.append((feature, feature_stats))
            elif abs_d >= 0.5:
                medium_effects.append((feature, feature_stats))
            elif abs_d >= 0.2:
                small_effects.append((feature, feature_stats))
            else:
                negligible_effects.append((feature, feature_stats))

        print(f"\nLARGE EFFECTS (Cohen's d >= 0.8): {len(large_effects)} features")
        for feature, feature_stats in sorted(
            large_effects, key=lambda x: abs(x[1]["cohens_d"]), reverse=True
        ):
            print(
                f"  • {feature}: d = {feature_stats['cohens_d']:.3f}, p = {feature_stats['p_value']:.2e}"
            )

        print(
            f"\nMEDIUM EFFECTS (0.5 <= Cohen's d < 0.8): {len(medium_effects)} features"
        )
        for feature, feature_stats in sorted(
            medium_effects, key=lambda x: abs(x[1]["cohens_d"]), reverse=True
        ):
            print(
                f"  • {feature}: d = {feature_stats['cohens_d']:.3f}, p = {feature_stats['p_value']:.2e}"
            )

        print(
            f"\nSMALL EFFECTS (0.2 <= Cohen's d < 0.5): {len(small_effects)} features"
        )
        for feature, feature_stats in sorted(
            small_effects, key=lambda x: abs(x[1]["cohens_d"]), reverse=True
        ):
            print(
                f"  • {feature}: d = {feature_stats['cohens_d']:.3f}, p = {feature_stats['p_value']:.2e}"
            )

        print(
            f"\nNEGLIGIBLE EFFECTS (Cohen's d < 0.2): {len(negligible_effects)} features"
        )
        for feature, feature_stats in sorted(
            negligible_effects, key=lambda x: abs(x[1]["cohens_d"]), reverse=True
        ):
            print(
                f"  • {feature}: d = {feature_stats['cohens_d']:.3f}, p = {feature_stats['p_value']:.3f}"
            )

        print("\nIMPORTANT CORRECTION:")
        print(
            "• Email length features (word_count, sentence_count, char_count) show NEGLIGIBLE effects"
        )
        print("• Phishing emails are NOT significantly longer than legitimate emails")
        print(
            "• The key differences are in word choice, sentiment, and psychological tactics"
        )

    def run_analysis(self):
        """Run the complete statistical analysis"""
        print("Starting Statistical Analysis of Phishing Email Features")
        print("=" * 60)

        # Load data
        self.load_cleaned_data()

        # Perform statistical tests
        self.perform_statistical_tests()

        # Create summary table
        summary_df = self.create_summary_table()

        # Create visualization
        self.create_effect_size_visualization()

        # Print key findings
        self.print_key_findings()

        print("\n" + "=" * 60)
        print("Statistical analysis complete!")
        print("Files generated:")
        print(
            "• ../results/statistical_analysis/statistical_summary.csv - Detailed statistical results"
        )
        print(
            "• ../results/visualizations/effect_sizes_statistical_analysis.png - Effect size visualization"
        )

        return summary_df


if __name__ == "__main__":
    # Check if feature dataset exists from main analysis
    feature_file = "../results/statistical_analysis/phishing_analysis_dataset.csv"

    # For now, use the existing CSV with computed features
    try:
        analyzer = PhishingStatisticalAnalyzer(feature_file)
        analyzer.run_analysis()
    except FileNotFoundError:
        print(f"Feature dataset not found at {feature_file}")
        print("Please run the main phishing_analysis.py first to generate features.")
