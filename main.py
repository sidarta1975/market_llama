# market_analyzer/main.py
from market_analyzer import db_manager, scheduler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_application():
    """ Initializes the database and starts the scheduler. """
    logging.info("Initializing Market Analyzer Application...")
    db_manager.create_tables() # Ensure database tables are created

    # --- INSERT WEBSITES AND SOCIAL MEDIA ADDRESSES HERE ---
    website_urls = [
        "https://juridico.ai/",
        "https://lawx.ai/"
        # Add more website URLs here
    ]

    social_media_urls = [
        "https://x.com/juridicoai",
        "https://x.com/competitor_x_account_1", # Replace with real competitor X account
        "https://www.instagram.com/competitor_instagram_account_1/", # Example for Instagram, you can add more social media types later
        # Add more social media URLs here
    ]
    # -------------------------------------------------------

    initial_sources = []
    for url in website_urls:
        initial_sources.append({
            'source_type': 'website',
            'source_name': f'Website - {url}', # Generate a name, can be improved
            'source_url': url,
            'monitoring_frequency': 'daily' # Default daily for websites
        })

    for url in social_media_urls:
        source_type = 'x.com' # Default to x.com for social media for now, can be expanded
        if "instagram.com" in url: # Example to handle different social media types if needed, expand as required
            source_type = 'instagram'
        elif "facebook.com" in url:
            source_type = 'facebook'
        elif "linkedin.com" in url:
            source_type = 'linkedin'
        elif "tiktok.com" in url:
            source_type = 'tiktok'

        initial_sources.append({
            'source_type': source_type,
            'source_name': f'Social Media ({source_type}) - {url}', # Generate a name
            'source_url': url,
            'monitoring_frequency': 'weekly' # Default weekly for social media
        })

    existing_sources = db_manager.get_monitored_sources()
    existing_urls = {source['source_url'] for source in existing_sources}

    for source_data in initial_sources:
        if source_data['source_url'] not in existing_urls:
            source_id = db_manager.add_monitored_source(
                source_data['source_type'],
                source_data['source_name'],
                source_data['source_url'],
                source_data['monitoring_frequency']
            )
            if source_id:
                logging.info(f"Added monitored source: {source_data['source_name']} with ID: {source_id}")
        else:
            logging.info(f"Monitored source {source_data['source_name']} with URL {source_data['source_url']} already exists.")

    logging.info("Database and monitored sources initialized.")
    scheduler.run_scheduler() # Start the scheduler to begin periodic tasks

if __name__ == '__main__':
    initialize_application()