import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from config import DB_NAME


def load_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT 
        b.id,
        b.rating,
        b.reviews,
        b.price_level,
        b.latitude,
        b.longitude,
        AVG(r.sentiment) as avg_sentiment
    FROM businesses b
    LEFT JOIN reviews r ON b.id = r.business_id
    GROUP BY b.id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def train_model(df):
    df = df.dropna()

    X = df[['reviews', 'price_level', 'latitude', 'longitude', 'avg_sentiment']]
    y = df['rating']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)

    print(f"Model trained. MSE: {mse:.4f}")

    return model


def run_modeling():
    print("Loading data...")
    df = load_data()

    print("Training model...")
    model = train_model(df)

    print("Modeling complete.")


if __name__ == "__main__":
    run_modeling()