# market_analyzer/db_manager.py
import sqlite3
from market_analyzer import config

def create_connection():
    """ Create a database connection to the SQLite database specified in config.py """
    conn = None
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        if conn:
            conn.close()
        return None

def create_tables():
    """ Create tables in the database if they do not exist. """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MonitoredSources (
                    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_type TEXT NOT NULL,
                    source_name TEXT NOT NULL,
                    source_url TEXT NOT NULL UNIQUE,
                    last_checked_timestamp TEXT,
                    monitoring_frequency TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS RawDataSnapshots (
                    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    raw_content TEXT,
                    FOREIGN KEY (source_id) REFERENCES MonitoredSources(source_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS AnalysisResults (
                    analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    snapshot_id INTEGER NOT NULL,
                    analysis_type TEXT NOT NULL,
                    analysis_timestamp TEXT NOT NULL,
                    analysis_result_json TEXT,
                    FOREIGN KEY (snapshot_id) REFERENCES RawDataSnapshots(snapshot_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Reports (
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_type TEXT NOT NULL,
                    report_period TEXT NOT NULL,
                    source_id INTEGER,
                    report_date TEXT NOT NULL,
                    report_file_txt TEXT,
                    report_file_gdoc TEXT,
                    FOREIGN KEY (source_id) REFERENCES MonitoredSources(source_id)
                )
            """)
            conn.commit()
            print("Database tables created or already exist.")
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
        finally:
            conn.close()
    else:
        print("Cannot create database connection.")

def add_monitored_source(source_type, source_name, source_url, monitoring_frequency):
    """ Add a new monitored source to the MonitoredSources table. """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO MonitoredSources (source_type, source_name, source_url, monitoring_frequency)
                VALUES (?, ?, ?, ?)
            """, (source_type, source_name, source_url, monitoring_frequency))
            conn.commit()
            return cursor.lastrowid # Return the ID of the new source
        except sqlite3.Error as e:
            print(f"Error adding monitored source: {e}")
        finally:
            conn.close()
    return None

def get_monitored_sources():
    """ Fetch all monitored sources from the MonitoredSources table. """
    conn = create_connection()
    sources = []
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM MonitoredSources")
            rows = cursor.fetchall()
            for row in rows:
                sources.append({
                    'source_id': row[0],
                    'source_type': row[1],
                    'source_name': row[2],
                    'source_url': row[3],
                    'last_checked_timestamp': row[4],
                    'monitoring_frequency': row[5]
                })
        except sqlite3.Error as e:
            print(f"Error fetching monitored sources: {e}")
        finally:
            conn.close()
    return sources

def save_raw_data_snapshot(source_id, timestamp, raw_content):
    """ Save raw data snapshot to RawDataSnapshots table. """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO RawDataSnapshots (source_id, timestamp, raw_content)
                VALUES (?, ?, ?)
            """, (source_id, timestamp, raw_content))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error saving raw data snapshot: {e}")
        finally:
            conn.close()
    return None

def save_analysis_result(snapshot_id, analysis_type, analysis_timestamp, analysis_result_json):
    """ Save analysis result to AnalysisResults table. """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO AnalysisResults (snapshot_id, analysis_type, analysis_timestamp, analysis_result_json)
                VALUES (?, ?, ?, ?)
            """, (snapshot_id, analysis_type, analysis_timestamp, analysis_result_json))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error saving analysis result: {e}")
        finally:
            conn.close()
    return None

def save_report(report_type, report_period, source_id, report_date, report_file_txt, report_file_gdoc):
    """ Save report metadata to Reports table. """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Reports (report_type, report_period, source_id, report_date, report_file_txt, report_file_gdoc)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (report_type, report_period, source_id, report_date, report_file_txt, report_file_gdoc))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error saving report: {e}")
        finally:
            conn.close()
    return None

def update_last_checked_timestamp(source_id, timestamp):
    """ Update the last_checked_timestamp for a monitored source. """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE MonitoredSources
                SET last_checked_timestamp = ?
                WHERE source_id = ?
            """, (timestamp, source_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating last checked timestamp: {e}")
        finally:
            conn.close()

# Add more database interaction functions as needed (e.g., fetching raw data for analysis, fetching analysis results for reports).

if __name__ == '__main__':
    create_tables() # Run this to initialize tables when first setting up
    # Example of adding a monitored source
    # source_id = add_monitored_source('website', 'Competitor A Website', 'https://www.competitorA.com', 'daily')
    # if source_id:
    #     print(f"Added new source with ID: {source_id}")
    # sources = get_monitored_sources()
    # print("Monitored Sources:", sources)


def get():
    return None