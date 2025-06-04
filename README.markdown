# Bank Reviews Scraping and Analysis Project

   ## Overview
   This project scrapes reviews from the Google Play Store for three Ethiopian banks (Commercial Bank of Ethiopia, Bank of Abyssinia, Dashen Bank), preprocesses the data, performs sentiment and thematic analysis, and saves results for further analysis.

   ## Task 1: Data Collection and Preprocessing
   ### Methodology
   1. **Setup**: Initialized a GitHub repository with `.gitignore` and `requirements.txt`. Work on the `task-1` branch with frequent commits.
   2. **Scraping**: Used `google-play-scraper` to collect reviews, ratings, dates, and app names for CBE (`et.com.cbemobilebanking`), BOA (`et.com.boamobile`), and Dashen Bank (`com.dashenbank.mBanking`). Targeted 400+ reviews per bank with `country='et'`.
   3. **Preprocessing**:
      - Removed duplicates based on review, date, and bank.
      - Handled missing data by dropping incomplete rows.
      - Normalized dates to YYYY-MM-DD.
   4. **Output**: Saved as `data/bank_reviews.csv` with columns: `review`, `rating`, `date`, `bank`, `source`.
   5. **KPIs**:
      - Collected 1,200+ reviews.
      - Ensured <5% missing data.
      - Organized Git repository.

   ## Task 2: Sentiment and Thematic Analysis
   ### Methodology
   1. **Sentiment Analysis**:
      - Used `distilbert-base-uncased-finetuned-sst-2-english` to compute sentiment scores (positive, negative, neutral).
      - Applied a 0.7 threshold for positive/negative classification; otherwise, labeled as neutral.
      - Aggregated sentiment by bank and rating.
   2. **Thematic Analysis**:
      - Preprocessed reviews using `spaCy` for tokenization, lemmatization, and stop-word removal.
      - Extracted keywords and n-grams using `TfidfVectorizer` (unigrams and bigrams).
      - Clustered reviews into 3–5 themes per bank (e.g., Account Access Issues, Transaction Performance, User Interface & Experience, Customer Support, Feature Requests) using rule-based keyword matching.
   3. **Output**: Saved results to `data/analyzed_reviews.csv` with columns: `review_id`, `review`, `sentiment_label`, `sentiment_score`, `themes`, `bank`, `rating`.
   4. **KPIs**:
      - Assigned sentiment scores to 90%+ reviews.
      - Identified 3+ themes per bank with examples.
      - Modular pipeline in `analyze_reviews.py`.

   ## Setup Instructions
   1. Clone the repository:
      ```bash
      git clone <repository-url>
      git checkout task-2
      ```
   2. Install dependencies:
      ```bash
      pip install -r requirements.txt
      python -m spacy download en_core_web_sm
      ```
   3. Run Task 1 to generate `bank_reviews.csv`:
      ```bash
      python scrape_reviews.py
      ```
   4. Run Task 2 for analysis:
      ```bash
      python analyze_reviews.py
      ```

   ## Output
   - Task 1: `data/bank_reviews.csv`
   - Task 2: `data/analyzed_reviews.csv`

   ## Notes
   - Ensure actual app IDs are correct in `scrape_reviews.py`.
   - Monitor for scraping errors due to rate limits or limited reviews in the Ethiopian Google Play Store.