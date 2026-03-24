import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sqlite3
import pandas as pd
from config import DB_NAME, PROCESSED_DATA_PATH

def load_data():
    conn = sqlite3.connect(DB_NAME)

    businesses = pd.read_sql_query("SELECT * FROM businesses", conn)
    reviews = pd.read_sql_query("SELECT * FROM reviews", conn)

    conn.close()

    return businesses, reviews


def clean_business_data(df):
    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df['rating'] = df['rating'].fillna(df['rating'].mean())
    df['reviews'] = df['reviews'].fillna(0)

    return df


def feature_engineering(business_df, reviews_df):
    # Average review length per business
    reviews_df['review_length'] = reviews_df['review_text'].apply(len)

    review_features = reviews_df.groupby('business_id').agg({
        'review_length': 'mean'
    }).rename(columns={'review_length': 'avg_review_length'}).reset_index()

    # Merge with business data
    merged_df = business_df.merge(review_features, left_on='id', right_on='business_id', how='left')

    # Fill missing values
    merged_df['avg_review_length'] = merged_df['avg_review_length'].fillna(0)

    # Create new features
    merged_df['review_to_rating_ratio'] = merged_df['reviews'] / (merged_df['rating'] + 1e-5)

    return merged_df


def save_processed_data(df):
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    file_path = os.path.join(PROCESSED_DATA_PATH, "processed_data.csv")

    df.to_csv(file_path, index=False)
    print(f"Processed data saved at {file_path}")


def run_preprocessing():
    print("Loading data...")
    businesses, reviews = load_data()

    print("Cleaning data...")
    businesses = clean_business_data(businesses)

    print("Engineering features...")
    processed_df = feature_engineering(businesses, reviews)

    print("Saving processed data...")
    save_processed_data(processed_df)

    print("Preprocessing complete.")


if __name__ == "__main__":
    run_preprocessing()