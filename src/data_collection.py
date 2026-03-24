import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
import random
import sqlite3
from config import DB_NAME, DEFAULT_LOCATION

def get_mock_business_data(n=20):
    businesses = []

    for i in range(n):
        business = {
            "name": f"Restaurant_{i}",
            "rating": round(random.uniform(2.5, 5.0), 1),
            "reviews": random.randint(50, 2000),
            "price_level": random.randint(1, 4),
            "latitude": DEFAULT_LOCATION["lat"] + random.uniform(-0.05, 0.05),
            "longitude": DEFAULT_LOCATION["lon"] + random.uniform(-0.05, 0.05)
        }
        businesses.append(business)

    return businesses


def get_mock_reviews(business_id, n=10):
    sample_reviews = [
        "Great food but slow service",
        "Amazing experience!",
        "Too expensive for the quality",
        "Loved the ambience",
        "Would not recommend",
        "Fantastic taste and quick delivery"
    ]

    return [
        {
            "business_id": business_id,
            "review_text": random.choice(sample_reviews)
        }
        for _ in range(n)
    ]


def save_to_db(businesses):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for b in businesses:
        cursor.execute("""
        INSERT INTO businesses (name, rating, reviews, price_level, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (b["name"], b["rating"], b["reviews"], b["price_level"], b["latitude"], b["longitude"]))

        business_id = cursor.lastrowid

        reviews = get_mock_reviews(business_id)
        for r in reviews:
            cursor.execute("""
            INSERT INTO reviews (business_id, review_text, sentiment)
            VALUES (?, ?, NULL)
            """, (r["business_id"], r["review_text"]))

    conn.commit()
    conn.close()


def run_pipeline():
    print("Fetching data...")
    businesses = get_mock_business_data(30)

    print("Saving to database...")
    save_to_db(businesses)

    print("Done.")


if __name__ == "__main__":
    run_pipeline()