from flask import Flask, request, jsonify
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tavily import TavilyClient
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
client = genai.Client(api_key="AIzaSyBalORoGfHqdiodododdkkE9HFFzdFmmDEH8")
SERPAPI_API_KEY = "abcxysuiosd1234iddk"
# Endpoint to fetch trend data for given keywords
@app.route("/trend_data", methods=["POST"])
def trend_data():
    data = request.get_json()
    description = data.get("description", "")
    category = data.get("category", "")
    location = data.get("location", "Worldwide")
    timeframe = data.get("timeframe", "today 12-m")

    if not description:
        return jsonify({"error": "Description is required."}), 400

    # Generate keywords using SerpAPI
    keywords = generate_keywords(description, category, location)

    trend_results = {}
    for keyword in keywords:
        trend_info = fetch_trend_data(keyword, location, timeframe)
        trend_results[keyword] = trend_info

    return jsonify({"trend_data": trend_results})

# Endpoint to get similar keyword suggestions
@app.route("/similar_suggestions", methods=["POST"])
def similar_suggestions():
    data = request.get_json()
    keyword = data.get("keyword", "")
    location = data.get("location", "Worldwide")

    if not keyword:
        return jsonify({"error": "Keyword is required."}), 400

    suggestions = fetch_related_keywords(keyword, location)
    return jsonify({"similar_suggestions": suggestions})

# Endpoint to analyze trend data using Gemini API
@app.route("/trend_analysis", methods=["POST"])
def trend_analysis():
    data = request.get_json()
    keyword = data.get("keyword", "")
    trend_data = data.get("trend_data", [])

    if not keyword or not trend_data:
        return jsonify({"error": "Keyword and trend data are required."}), 400

    # Prepare prompt for Gemini API
    historical_values = ", ".join([f"{item['date']}: {item['value']}" for item in trend_data[-5:]])
    prompt = f"""
    Analyze the following trend data for '{keyword}':
    Recent historical data: {historical_values}
    Provide:
    1. A brief summary of recent trend behavior.
    2. Explanation of why this trend might be changing.
    3. Recommend two new related topics/categories for further exploration.
    Structure the response clearly.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(temperature=0.1),
        contents=prompt,
    )
    return jsonify({"analysis": response.text.strip()})

# Helper function to generate keywords using SerpAPI
def generate_keywords(description, category, location):
    params = {
        "engine": "google_trends",
        "q": description,
        "geo": "" if location == "Worldwide" else location,
        "api_key": SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    related_queries = results.get("related_queries", {}).get("top", [])
    keywords = [item["query"] for item in related_queries[:5]]
    return keywords

# Helper function to fetch trend data using SerpAPI
def fetch_trend_data(keyword, location, timeframe):
    params = {
        "engine": "google_trends",
        "q": keyword,
        "geo": "" if location == "Worldwide" else location,
        "date": timeframe,
        "api_key": SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    timeline_data = results.get("interest_over_time", {}).get("timeline_data", [])
    historical = [{"date": item["date"], "value": item["values"][0]["extracted_value"]} for item in timeline_data]
    return historical

# Helper function to fetch related keywords using SerpAPI
def fetch_related_keywords(keyword, location):
    params = {
        "engine": "google_trends",
        "q": keyword,
        "geo": "" if location == "Worldwide" else location,
        "api_key": SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    related_queries = results.get("related_queries", {}).get("top", [])
    suggestions = [item["query"] for item in related_queries[:10]]
    return suggestions

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
