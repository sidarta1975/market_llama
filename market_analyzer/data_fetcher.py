from datetime import datetime

import requests

from market_analyzer import db_manager

def fetch_website_content(url):
    """Fetches content from a website URL."""
    try:
        response = requests.get(url, headers={'User-Agent': 'MarketAnalyzerBot/1.0'})  # Added User-Agent to mimic browser
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.content.decode('utf-8', errors='ignore')  # Decode content, ignoring errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def fetch_social_media_data(source_type):
    """Placeholder for fetching social media data. Needs API keys and platform-specific logic."""
    print(f"Fetching social media data from {source_type} is not fully implemented yet.")
    # Implement your social media data fetching logic here
    #...
    return  # Return an empty list for now

def fetch_data_for_source(source):
    """Fetches data based on source type and saves to database."""
    global raw_content
    source_id = source['source_id']
    source_type = source['source_type']
    source_url = source['source_url']

    current_timestamp = datetime.now().isoformat()

    if source_type == 'website':
        raw_content = fetch_website_content(source_url)
    elif source_type in ['x.com', 'instagram', 'facebook', 'linkedin', 'tiktok']:
        fetch_social_media_data(source_type)
    else:
        print(f"Unsupported source type: {source_type} for source ID: {source_id}")
        return

    if raw_content is not None:
        snapshot_id = db_manager.save_raw_data_snapshot(source_id, current_timestamp, raw_content)
        if snapshot_id:
            print(f"Successfully fetched and saved data for source ID: {source_id}, Snapshot ID: {snapshot_id}")
            db_manager.update_last_checked_timestamp(source_id, current_timestamp)
        else:
            print(f"Failed to save raw data to database for source ID: {source_id}")
    else:
        print(f"Failed to fetch data for source ID: {source_id} from URL: {source_url}")

#... (rest of the code remains the same)