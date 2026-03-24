import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from openai import OpenAI
client = OpenAI(api_key=("OPENAI_API_KEY"))

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from config import DB_NAME


# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT 
        b.name,
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


# -------------------------------
# Dashboard UI
# -------------------------------
st.set_page_config(page_title="Business Intelligence System", layout="wide")

st.title("📊 Local Business Intelligence Dashboard")

df = load_data()

# -------------------------------
# Metrics
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Businesses", len(df))
col2.metric("Average Rating", round(df['rating'].mean(), 2))
col3.metric("Avg Sentiment", round(df['avg_sentiment'].mean(), 2))


# -------------------------------
# Charts
# -------------------------------
st.subheader("📈 Ratings Distribution")
fig = px.histogram(df, x="rating", nbins=10)
st.plotly_chart(fig, use_container_width=True)

st.subheader("💬 Sentiment vs Rating")
fig2 = px.scatter(df, x="avg_sentiment", y="rating", hover_name="name")
st.plotly_chart(fig2, use_container_width=True)


# -------------------------------
# Map
# -------------------------------
st.subheader("🗺️ Business Locations")
fig3 = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    hover_name="name",
    hover_data=["rating", "avg_sentiment"],
    zoom=12,
    height=500
)

fig3.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig3, use_container_width=True)


# -------------------------------
# AI Chatbot (Simple Rule-Based)
# -------------------------------
st.subheader("🤖 Ask Your Data")

user_query = st.text_input("Ask a question about businesses:")

# def ai_chat(query, df):
#     context = df.head(50).to_string()

#     prompt = f"""
# You are a business data analyst.

# Here is the dataset:
# {context}

# User question: {query}

# Give a clear, actionable answer.
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content

def ai_chat(query, df):
    try:
        context = df.head(50).to_string()

        prompt = f"""
You are a business data analyst.

Here is the dataset:
{context}

User question: {query}

Give a clear, actionable answer based on the data.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful business analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"
    
def simple_ai(query, df):
    query = query.lower()

    if "best" in query:
        best = df.sort_values(by="rating", ascending=False).iloc[0]
        return f"Best business is {best['name']} with rating {best['rating']}"

    elif "worst" in query:
        worst = df.sort_values(by="rating").iloc[0]
        return f"Worst business is {worst['name']} with rating {worst['rating']}"

    elif "sentiment" in query:
        return f"Average sentiment is {round(df['avg_sentiment'].mean(), 2)}"

    elif "underperform" in query:
        under = df[df['rating'] < 3.5]
        if len(under) == 0:
            return "No significantly underperforming businesses found."
        formatted = "\n".join(
    [f"{row['name']} (Rating: {row['rating']})" for _, row in under.iterrows()]
)

        return f"Underperforming businesses:\n\n{formatted}"

    else:
        return "Try asking about best, worst, sentiment, or underperforming businesses."
    
def display_underperforming(df):
    under = df[df['rating'] < 3.5]

    if under.empty:
        st.success("No significantly underperforming businesses found.")
        return

    st.subheader("⚠️ Underperforming Businesses")

    for _, row in under.iterrows():
        st.markdown(f"""
**{row['name']}**
- Rating: {row['rating']}
- Sentiment: {round(row['avg_sentiment'], 2)}
""")
        st.divider()        

if user_query:
    try:
        response = ai_chat(user_query, df)

        if "AI Error" in response:
            st.warning("AI unavailable, using basic analysis.")

            if "underperform" in user_query.lower():
                display_underperforming(df)
            else:
                st.success(simple_ai(user_query, df))

        else:
            st.success(response)

    except:
        if "underperform" in user_query.lower():
            display_underperforming(df)
        else:
            st.success(simple_ai(user_query, df))