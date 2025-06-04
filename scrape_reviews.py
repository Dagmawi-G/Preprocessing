import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime
import os

# Define bank app IDs (replace with actual Google Play Store IDs)
BANK_APPS = {
    'Bank1': 'com.example.bank1',
    'Bank2': 'com.example.bank2',
    'Bank3': 'com.example.bank3'
}

def scrape_reviews(app_id, bank_name, count=400):
    """Scrape reviews for a given app ID."""
    all_reviews = []
    continuation_token = None
    
    while len(all_reviews) < count:
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=min(100, count - len(all_reviews)),
                continuation_token=continuation_token
            )
            for review in result:
                all_reviews.append({
                    'review': review['content'],
                    'rating': review['score'],
                    'date': review['at'].strftime('%Y-%m-%d'),
                    'bank': bank_name,
                    'source': 'Google Play Store'
                })
        except Exception as e:
            print(f"Error scraping {bank_name}: {e}")
            break
    
    return all_reviews[:count]

def preprocess_reviews(reviews):
    """Preprocess the scraped reviews."""
    # Convert to DataFrame
    df = pd.DataFrame(reviews)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['review', 'date', 'bank'])
    
    # Handle missing data
    df = df.dropna(subset=['review', 'rating', 'date'])
    
    # Ensure date is in YYYY-MM-DD format
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%DD')
    
    return df

def main():
    # Create output directory
    os.makedirs('data', exist_ok=True)
    
    # Scrape reviews for each bank
    all_reviews = []
    for bank_name, app_id in BANK_APPS.items():
        print(f"Scraping reviews for {bank_name}...")
        reviews_data = scrape_reviews(app_id, bank_name)
        all_reviews.extend(reviews_data)
    
    # Preprocess reviews
    df = preprocess_reviews(all_reviews)
    
    # Save to CSV
    output_path = 'data/bank_reviews.csv'
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} reviews to {output_path}")
    
    # Print KPIs
    print(f"Total reviews collected: {len(df)}")
    print(f"Missing data percentage: {(1 - len(df.dropna()) / len(df)) * 100:.2f}%")

if __name__ == "__main__":
    main()