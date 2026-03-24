# 🚀 Real-Time Local Business Survival Intelligence System

## 📊 Overview

The **Real-Time Local Business Survival Intelligence System** is a data-driven analytics platform designed to evaluate and predict the performance of local businesses.

It combines **data analysis, geospatial insights, sentiment evaluation, and AI-powered querying** to help identify:

* Underperforming businesses
* Market trends
* Strategic opportunities for growth

This project simulates how modern business intelligence tools can assist decision-making at a local level.

---

## 🧠 Key Features

### 📈 Live Analytics Dashboard

* Total business insights
* Average rating & sentiment tracking
* Interactive visualizations using Plotly

### 🗺️ Geospatial Mapping

* Business distribution visualization
* Location-based clustering
* Map-based exploration of business density

### 💬 AI Chat Interface

* Ask questions about your data in natural language
* Example queries:

  * “Which businesses are underperforming?”
  * “What is the average sentiment?”
  * “Show the best rated businesses”

⚠️ Includes a **fallback rule-based system** if AI is unavailable

---

### 🔍 Data Processing Pipeline

* Data collection & preprocessing
* Sentiment analysis
* Feature engineering
* Recommendation generation

---

## 🏗️ Project Structure

```
.
├── dashboard/
│   ├── app.py              # Streamlit dashboard
│   ├── map.html           # Map visualization
│
├── src/
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── modeling.py
│   ├── geo_analysis.py
│   ├── sentiment_analysis.py
│   ├── recommendation_engine.py
│
├── database/
│   └── db_setup.py
│
├── data/
│   └── processed/
│       ├── processed_data.csv
│       ├── recommendations.csv
│
├── business_data.db
├── config.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Real-Time-Local-Business-Survival-Intelligence-System.git
cd Real-Time-Local-Business-Survival-Intelligence-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

(Optional)

```
YOUTUBE_API_KEY=your_youtube_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run dashboard/app.py
```

Then open:

```
http://localhost:8501
```

---

## 🧪 Example Queries (AI Chat)

* Which businesses are underperforming?
* What is the average sentiment?
* Show the best business
* Where are businesses concentrated?

---

## ⚠️ Notes

* If OpenAI API is unavailable or quota is exceeded, the system switches to **basic analytical responses**
* Ensure your API key is valid and has available quota

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Pandas**
* **Plotly**
* **SQLite**
* **OpenAI API**
* **Geospatial Analysis**

---

## 🚧 Future Improvements

* Real-time data ingestion (Google Maps API, Yelp, etc.)
* Advanced ML models for prediction
* Business survival scoring system
* Deployment (Streamlit Cloud / AWS / Docker)

---

## 👤 Author

**Suraj Rajvanshi**

---

## ⭐ Final Thought

This project demonstrates how **data + AI + visualization** can be combined to build intelligent systems that go beyond static dashboards — enabling real-time insights and decision-making.

---
