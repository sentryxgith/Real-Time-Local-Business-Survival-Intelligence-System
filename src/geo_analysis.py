import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sqlite3
import folium
import pandas as pd
from config import DB_NAME, DEFAULT_LOCATION


def load_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT 
        b.name,
        b.rating,
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


def create_map(df):
    m = folium.Map(
        location=[DEFAULT_LOCATION["lat"], DEFAULT_LOCATION["lon"]],
        zoom_start=13
    )

    for _, row in df.iterrows():
        popup_text = f"""
        Name: {row['name']}<br>
        Rating: {row['rating']}<br>
        Sentiment: {row['avg_sentiment']}
        """

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_text
        ).add_to(m)

    m.save("dashboard/map.html")
    print("Map saved to dashboard/map.html")


def run_geo_analysis():
    print("Loading data...")
    df = load_data()

    print("Creating map...")
    create_map(df)

    print("Geo analysis complete.")


if __name__ == "__main__":
    run_geo_analysis()