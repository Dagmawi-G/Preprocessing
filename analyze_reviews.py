import pandas as pd
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Load spaCy model for English
nlp = spacy.load("en_core_web_sm")

# Load DistilBERT for sentiment analysis
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    tokenizer="distilbert-base-uncased-finetuned-sst-2-english",
    framework="pt",
    truncation=True,
    max_length=512
)

# Define themes and associated keywords (rule-based clustering)
THEME_KEYWORDS = {
    'Account Access Issues': ['login', 'log in', 'authentication', 'password', 'error', 'access', 'locked'],
    'Transaction Performance': ['transfer', 'slow', 'loading', 'transaction', 'payment', 'delay', 'timeout'],
    'User Interface & Experience': ['ui', 'interface', 'design', 'navigation', 'user-friendly', 'layout'],
    'Customer Support': ['support', 'help', 'response', 'customer service', 'contact'],
    'Feature Requests': ['feature', 'add', 'fingerprint', 'biometric', 'budget', 'notification']
}

def preprocess_text(text):
    """Preprocess text for NLP analysis."""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def get_sentiment(text):
    """Compute sentiment score and label using DistilBERT."""
    try:
        result = sentiment_analyzer(text)[0]
        label = result['label'].lower()  # 'POSITIVE' or 'NEGATIVE'
        score = result['score']
        # Convert to positive/negative/neutral based on score
        if label == 'positive' and score >= 0.7:
            return 'positive', score
        elif label == 'negative' and score >= 0.7:
            return 'negative', score
        else:
            return 'neutral', score
    except Exception as e:
        print(f"Error analyzing sentiment for text: {text[:50]}... {e}")
        return 'neutral', 0.0

def extract_keywords(texts, max_features=100):
    """Extract significant keywords and n-grams using TF-IDF."""
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),  # Unigrams and bigrams
        stop_words='english'
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    return vectorizer.get_feature_names_out()

def assign_themes(review, keywords):
    """Assign themes to a review based on keyword matching."""
    themes = []
    review_lower = review.lower()
    for theme, theme_keywords in THEME_KEYWORDS.items():
        if any(keyword in review_lower for keyword in theme_keywords):
            themes.append(theme)
    return themes if themes else ['Other']

def main():
    # Load the CSV from Task 1
    input_path = 'data/bank_reviews.csv'
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"{input_path} not found. Run Task 1 first.")
    
    df = pd.read_csv(input_path)
    
    # Preprocess reviews
    df['processed_review'] = df['review'].apply(preprocess_text)
    
    # Perform sentiment analysis
    df['sentiment_label'], df['sentiment_score'] = zip(*df['review'].apply(get_sentiment))
    
    # Extract keywords
    keywords = extract_keywords(df['processed_review'].tolist())
    print(f"Extracted keywords: {keywords[:20]}")  # Print first 20 for reference
    
    # Assign themes
    df['themes'] = df['review'].apply(lambda x: assign_themes(x, keywords))
    
    # Create review_id
    df['review_id'] = df.index + 1
    
    # Select and reorder columns
    output_df = df[['review_id', 'review', 'sentiment_label', 'sentiment_score', 'themes', 'bank', 'rating']]
    
    # Save results to CSV
    os.makedirs('data', exist_ok=True)
    output_path = 'data/analyzed_reviews.csv'
    output_df.to_csv(output_path, index=False)
    print(f"Saved analysis to {output_path}")
    
    # Aggregate sentiment by bank and rating
    sentiment_summary = df.groupby(['bank', 'rating', 'sentiment_label']).size().unstack(fill_value=0)
    print("\nSentiment Summary by Bank and Rating:")
    print(sentiment_summary)
    
    # Print theme counts per bank
    theme_counts = df.explode('themes').groupby(['bank', 'themes']).size().unstack(fill_value=0)
    print("\nTheme Counts by Bank:")
    print(theme_counts)
    
    # KPIs
    print(f"\nTotal reviews analyzed: {len(df)}")
    print(f"Sentiment scores assigned: {(df['sentiment_label'] != 'neutral').sum() / len(df) * 100:.2f}%")
    print(f"Themes identified per bank:")
    for bank in df['bank'].unique():
        bank_themes = theme_counts.loc[bank]
        print(f"{bank}: {list(bank_themes[bank_themes > 0].index)}")

if __name__ == "__main__":
    main()