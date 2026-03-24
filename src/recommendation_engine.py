import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sqlite3
import pandas as pd
from config import DB_NAME


def load_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT 
        b.name,
        b.rating,
        b.reviews,
        b.price_level,
        AVG(r.sentiment) as avg_sentiment
    FROM businesses b
    LEFT JOIN reviews r ON b.id = r.business_id
    GROUP BY b.id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def generate_recommendations(df):
    recommendations = []

    for _, row in df.iterrows():
        insights = []

        if row['rating'] < 3.5:
            insights.append("Improve overall service quality")

        if row['avg_sentiment'] < 0:
            insights.append("Customer sentiment is negative—investigate complaints")

        if row['reviews'] < 100:
            insights.append("Increase marketing to attract more customers")

        if row['price_level'] >= 3 and row['rating'] < 4:
            insights.append("Pricing may be too high for perceived value")

        if len(insights) == 0:
            insights.append("Business performing well")

        recommendations.append({
            "name": row['name'],
            "rating": row['rating'],
            "sentiment": row['avg_sentiment'],
            "recommendation": " | ".join(insights)
        })

    return pd.DataFrame(recommendations)


def run_recommendation_engine():
    print("Loading data...")
    df = load_data()

    print("Generating recommendations...")
    result = generate_recommendations(df)

    print("\nSample Recommendations:\n")
    print(result.head())

    result.to_csv("data/processed/recommendations.csv", index=False)
    print("\nSaved to data/processed/recommendations.csv")


if __name__ == "__main__":
    run_recommendation_engine()