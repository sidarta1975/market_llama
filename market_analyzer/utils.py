# market_analyzer/utils.py
from datetime import datetime

def generate_timestamp():
    """ Generates an ISO formatted timestamp string. """
    return datetime.now().isoformat()

def create_report_filename(base_name, period, date_str, format='txt'):
    """ Creates a standardized report filename. """
    return f"{base_name}_{period}_{date_str}.{format}"