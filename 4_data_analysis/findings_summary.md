# Findings Summary

This study investigates the linguistic and structural signals that distinguish phishing emails from legitimate ones, and evaluates how effectively these can be used for automated detection.

## Research Question

**How do phishing emails differ from legitimate emails in terms of common linguistic patterns and language tactics?**

### Subquestions

- What specific linguistic features show measurable differences between phishing and legitimate emails?
- Are these differences statistically significant and meaningful?
- Can a machine learning model trained on these features accurately classify emails as phishing or legitimate?

---

## Hypothesis

Phishing emails exhibit distinct linguistic features—such as tone, structure, and word usage—that differ measurably from legitimate emails and can be used to accurately detect phishing attempts.

---

## What We Analyzed

- **Dataset**: 29,711 Enron emails (53.05% safe, 46.95% phishing)
- **Features**: 22 linguistic, readability, psychological, and structural variables.
- **Statistical Test**: Welch’s t-test for p-values; Cohen’s d for effect size using the report’s scale:
  - 🟥 **Large**: |d| ≥ 0.50  
  - 🟧 **Medium**: 0.30 ≤ |d| < 0.50  
  - 🟨 **Small**: 0.20 ≤ |d| < 0.30
- **Model**: Random Forest Classifier (100 trees, `class_weight='balanced'`)
  - Used for **phishing email detection** by learning patterns from linguistic and structural features.
  - Combines predictions from multiple decision trees to improve accuracy and reduce overfitting.
  - **Evaluation**: 5-fold cross-validation.

---

## Cohen’s d Effect Sizes

| Magnitude                |Features                                                                                                    |
|-------------------------|-------------------------------------------------------------------------------------------------------------|
| 🟥 **Large (≥ 0.50)**    | sentiment_neg (0.503)                                                                                        |
| 🟧 **Medium (0.30–<0.50)** | sentiment_neu (-0.489), type_token_ratio (0.372), exclamation_ratio (0.365), avg_word_length (0.340), financial_words (0.316), reward_words (0.305) |
| 🟨 **Small (0.20–<0.30)** | url_count (0.270), action_words (0.197), urgency_words (0.202), flesch_score (-0.227), sentiment_pos (0.229), email_pattern_count (-0.255) |

## Model Performance — Confusion Matrix

|                 | Predicted Phishing 🟥 | Predicted Safe 🟩 |
|-----------------|----------------------|------------------|
| **Actual Phishing 🟥** | **TP = 10,752** | **FN = 3,197** |
| **Actual Safe 🟩**     | **FP = 2,493**  | **TN = 13,268** |

**Metrics:**

- **Accuracy**: 83.5% — overall correctness.
- **Precision (Phishing)**: 86.4% — of predicted phishing emails, % actually phishing.
- **Recall (Phishing)**: 77.1% — of actual phishing emails, % correctly found.
- **F1-score**: 81.5% — balance between precision and recall.

---

## Limitations

- **Temporal Bias**: Enron dataset (2001) may not reflect modern phishing tactics.
- **Domain Specificity**: Corporate email context limits generalizability.
- **Lexicon Bias**: VADER sentiment and static keyword lists may miss nuanced or emerging manipulation.
- **Model Interpretability**: While the Random Forest achieved high accuracy, it is not highly interpretable compared to simpler models.
- **No External Validation**: Model performance was evaluated only with 5-fold cross-validation on the Enron dataset; generalization to other datasets has not been tested.

---

## Conclusion

Using the report’s Cohen’s d scale, **negative sentiment** was the only feature in the large category, with several medium and small effects observed. While many individual features are not strong enough to detect phishing alone, **in combination they form a powerful detection tool** — as demonstrated by the Random Forest model’s 83.5% accuracy in phishing email detection.  

However, since the model was only evaluated with 5-fold cross-validation on the Enron dataset, the next step should include **external validation** on more recent and diverse datasets to confirm generalizability and ensure robustness against evolving phishing tactics.

---

## Next Steps

- Perform **external validation** using datasets from different domains and recent time periods to assess real-world applicability.
- Compare the Random Forest’s performance with more interpretable models to balance accuracy and explainability.
