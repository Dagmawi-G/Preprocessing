# Bank Reviews Scraping Project

## Overview
This project scrapes reviews from the Google Play Store for three banking apps, preprocesses the data, and saves it as a CSV file. The goal is to collect at least 400 reviews per bank (1,200 total) with minimal missing data.

## Methodology
1. **Setup**: Initialize a GitHub repository with a `.gitignore` and `requirements.txt`. Work on the `task-1` branch with frequent, meaningful commits.
2. **Scraping**: Use the `google-play-scraper` library to collect reviews, ratings, dates, and app names for three banking apps. Target 400+ reviews per bank.
3. **Preprocessing**:
   - Remove duplicate reviews based on content, date, and bank.
   - Handle missing data by dropping rows with missing critical fields (review, rating, date).
   - Normalize dates to YYYY-MM-DD format.
4. **Output**: Save the preprocessed data as a CSV file with columns: `review`, `rating`, `date`, `bank`, `source`.
5. **KPIs**:
   - Collect 1,200+ reviews.
   - Ensure <5% missing data.
   - Maintain an organized Git repository.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   git checkout task-1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `BANK_APPS` in `scrape_reviews.py` with actual Google Play Store app IDs.
4. Run the script:
   ```bash
   python scrape_reviews.py
   ```

## Output
- The script generates a `bank_reviews.csv` file in the `data/` directory.
- The CSV contains columns: `review`, `rating`, `date`, `bank`, `source`.

## Notes
- Replace `com.example.bank1`, etc., in `scrape_reviews.py` with actual app IDs from the Google Play Store.
- The script handles errors gracefully and prints KPIs (total reviews and missing data percentage).