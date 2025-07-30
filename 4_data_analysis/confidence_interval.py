import pandas as pd

df = pd.read_csv("4_data_analysis/feature_comparison_stats.csv", index_col=0)
significant = df[df["p_value"] < 0.05]
print(significant[["effect_size", "p_value", "95%_CI_difference"]])

# this shows confidence interval for sentiment_neg making it statistically significant (and we know it has high cohen effect)
