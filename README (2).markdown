# Bank Reviews Scraping and Analysis Project

   ## Overview
   This project scrapes reviews from the Google Play Store for three Ethiopian banks (Commercial Bank of Ethiopia, Bank of Abyssinia, Dashen Bank), preprocesses the data, performs sentiment and thematic analysis, and stores it in an Oracle database.

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

   ## Task 3: Store Cleaned Data in Oracle
   ### Methodology
   1. **Database Setup**:
      - Used Oracle Database XE with `oracledb` to create a `bank_reviews` database.
      - Defined two tables:
        - `Banks`: `bank_id` (primary key), `bank_name` (unique).
        - `Reviews`: `review_id` (primary key), `bank_id` (foreign key), `review_text`, `rating`, `review_date`, `source`, `sentiment_label`, `sentiment_score`, `themes`.
   2. **Data Insertion**:
      - Inserted unique banks into `Banks` and reviews from `analyzed_reviews.csv` into `Reviews` using `setup_database.py`.
   3. **SQL Dump**:
      - Generated `bank_reviews_dump.sql` with `CREATE TABLE` and `INSERT` statements.
   4. **KPIs**:
      - Established a working connection and insert script.
      - Populated tables with >1,000 entries.
      - Committed SQL dump to GitHub.

   ## Setup Instructions
   1. Clone the repository:
      ```bash
      git clone <repository-url>
      git checkout task-3
      ```
   2. Install dependencies:
      ```bash
      pip install -r requirements.txt
      python -m spacy download en_core_web_sm
      ```
   3. Setup Oracle XE:
      - Install Oracle XE and create a user (`bank_user`).
      - Update `DB_USER` and `DB_PASSWORD` in `setup_database.py`.
   4. Run scripts in order:
      ```bash
      python scrape_reviews.py
      python analyze_reviews.py
      python setup_database.py
      ```

   ## Output
   - Task 1: `data/bank_reviews.csv`
   - Task 2: `data/analyzed_reviews.csv`
   - Task 3: `data/bank_reviews_dump.sql`

   ## Notes
   - Ensure actual app IDs are correct in `scrape_reviews.py`.
   - Monitor for scraping errors due to rate limits or limited reviews in the Ethiopian Google Play Store.
   - Update `DB_PASSWORD` in `setup_database.py` before running.