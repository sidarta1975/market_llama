import json
import sqlite3
from datetime import datetime

import requests

from market_analyzer import db_manager
from market_analyzer.config import OLLAMA_API_URL

def analyze_with_ollama(prompt):
    """Sends a prompt to Ollama and returns the response."""
    try:
        url = OLLAMA_API_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            "model": "llama3.2",  # Use your actual Llama model name
            "prompt": prompt
        }
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()

        # Iterate over the response stream and extract the text
        text = ""
        for line in response.iter_lines():
            if line:
                try:
                    decoded_line = line.decode('utf-8')
                    json_response = json.loads(decoded_line)
                    text += json_response.get("response", "")
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")
                    continue

        return text

    except requests.exceptions.RequestException as e:
        print(f"Ollama API Error: {e}")
        return None

def perform_sentiment_analysis(content):
    """Performs sentiment analysis on content using Ollama."""
    prompt = f"Analyze the sentiment of the following text and return the sentiment (positive, negative, or neutral) and a score from -1 to 1 (negative to positive):\n\n{content}\n\nResponse should be in JSON format like: {{'sentiment': '...', 'score':...}}"
    return analyze_with_ollama(prompt)

def perform_topic_extraction(content):
    """Extracts key topics from content using Ollama."""
    prompt = f"Extract the main topics and keywords from the following text. Return a JSON array of topics and keywords:\n\n{content}\n\nResponse should be in JSON format like: {{'topics': ['topic1', 'topic2',...], 'keywords': ['keyword1', 'keyword2',...]}}"
    return analyze_with_ollama(prompt)

def analyze_raw_data_snapshot(snapshot_id=None, raw_content=None):
    """Analyzes a raw data snapshot using Ollama and saves results."""
    if not raw_content:
        conn = db_manager.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT raw_content FROM RawDataSnapshots WHERE snapshot_id =?", (snapshot_id,))
                result = cursor.fetchone()
                if result:
                    raw_content = result  # Extract the raw_content string from the fetched row
            except sqlite3.Error as e:
                print(f"Database error fetching raw content: {e}")
            finally:
                conn.close()

    if not raw_content:
        print(f"No raw content found for snapshot ID: {snapshot_id}")
        return

    analysis_timestamp = datetime.now().isoformat()

    analysis_results = {}

    # Perform Sentiment Analysis
    sentiment_result = perform_sentiment_analysis(raw_content)
    if sentiment_result:
        analysis_results['sentiment_analysis'] = sentiment_result

    # Perform Topic Extraction
    topic_extraction_result = perform_topic_extraction(raw_content)
    if topic_extraction_result:
        analysis_results['topic_extraction'] = topic_extraction_result

    # Save analysis results (and potentially update last_checked_timestamp)
    if analysis_results:
        for analysis_type, result in analysis_results.items():
            db_manager.save_analysis_result(snapshot_id, analysis_type, analysis_timestamp, result)

    return analysis_results