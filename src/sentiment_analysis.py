import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import DB_NAME


def load_reviews():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, review_text FROM reviews WHERE sentiment IS NULL")
    reviews = cursor.fetchall()

    conn.close()
    return reviews


def update_sentiment(review_id, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE reviews SET sentiment = ? WHERE id = ?",
        (score, review_id)
    )

    conn.commit()
    conn.close()


def analyze_sentiment():
    analyzer = SentimentIntensityAnalyzer()
    reviews = load_reviews()

    print(f"Processing {len(reviews)} reviews...")

    if len(reviews) == 0:
        print("No reviews found with NULL sentiment. Skipping.")
        return

    for review_id, text in reviews:
        score = analyzer.polarity_scores(text)['compound']
        print(f"Review: {text} | Score: {score}")
        update_sentiment(review_id, score)

    print("Sentiment analysis complete.")


if __name__ == "__main__":
    analyze_sentiment()