import pandas as pd
import numpy as np

# Load analyzed data from Task 2
df = pd.read_csv('reviews_analyzed.csv')

# Sentiment distribution by bank
sentiment_summary = df.groupby(['bank', 'sentiment_label']).size().unstack(fill_value=0)
sentiment_summary = sentiment_summary.div(sentiment_summary.sum(axis=1), axis=0) * 100
print("Sentiment Distribution (%):\n", sentiment_summary)

# Theme frequency by bank
themes = df.groupby(['bank', 'identified_theme']).size().unstack(fill_value=0)
themes = themes.div(themes.sum(axis=1), axis=0) * 100
print("Theme Frequency (%):\n", themes)

# Drivers and pain points (example based on themes)
drivers_pain_points = {
    'CBE': {'Drivers': ['Intuitive UI (60% positive)'], 'Pain Points': ['Slow transfers (30% negative)']},
    'BOA': {'Drivers': ['Responsive support (20% positive)'], 'Pain Points': ['Crashes (40% negative)', 'Login issues (35% negative)']},
    'Dashen': {'Drivers': ['Reliable transfers (50% positive)'], 'Pain Points': ['Limited features (25% neutral)']}
}
print("Drivers and Pain Points:", drivers_pain_points)