# market_analyzer/scheduler.py
import logging
import sqlite3
import time
from datetime import datetime, timedelta

import schedule

from market_analyzer import (data_analyzer, data_fetcher, db_manager,
                             email_notifier, report_generator)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_monitoring_schedule(reporting_job=None, weekly_email_job=None):
    """Sets up the schedule for data fetching, analysis, and reporting."""
    monitored_sources = db_manager.get_monitored_sources()

    for source in monitored_sources:
        if source['monitoring_frequency'] == 'daily':
            schedule.every().day.at("08:00").do(data_fetching_job, source=source)  # Example time: 8 AM daily
        elif source['monitoring_frequency'] == 'weekly':
            schedule.every().monday.at("09:00").do(data_fetching_job, source=source)  # Example: Mondays at 9 AM weekly
        logging.info(f"Scheduled data fetching for {source['source_name']} ({source['monitoring_frequency']})")

    schedule.every().day.at("10:00").do(analysis_job)  # Daily analysis at 10 AM
    schedule.every().day.at("11:00").do(reporting_job)  # Daily reporting at 11 AM
    schedule.every().monday.at("12:00").do(weekly_email_job)  # Weekly email on Mondays at 12 PM

    logging.info("Scheduling complete.")

def data_fetching_job(source):
    """Job to fetch data for a specific source."""
    logging.info(f"Starting data fetching for {source['source_name']}")
    data_fetcher.fetch_data_for_source(source)
    logging.info(f"Data fetching completed for {source['source_name']}")

def analysis_job():
    """Job to analyze new raw data snapshots."""
    logging.info("Starting data analysis job")
    monitored_sources = db_manager.get_monitored_sources()
    for source in monitored_sources:
        last_checked_timestamp_str = source['last_checked_timestamp']
        if last_checked_timestamp_str:
            last_checked_timestamp = datetime.fromisoformat(last_checked_timestamp_str)
            time_delta = timedelta(hours=24) if source['monitoring_frequency'] == 'daily' else timedelta(days=7)  # Based on frequency
            cutoff_timestamp = last_checked_timestamp - time_delta  # Get snapshots fetched since last analysis

            conn = db_manager.create_connection()
            snapshot_ids_to_analyze =  # Initialize as an empty list
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT snapshot_id FROM RawDataSnapshots
                        WHERE source_id =? AND timestamp >=?
                    """, (source['source_id'], cutoff_timestamp.isoformat()))
                    # Extract the 'snapshot_id' from the fetched rows
                    snapshot_ids_to_analyze = [row for row in cursor.fetchall()]
                except sqlite3.Error as e:
                    logging.error(f"Database error fetching snapshot IDs for analysis: {e}")
                finally: