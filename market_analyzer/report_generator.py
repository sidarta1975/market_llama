# market_analyzer/report_generator.py
import json
from datetime import datetime

from market_analyzer import db_manager, config


def generate_individual_report(source_id, report_period):
    """Generates a report for a specific monitored source."""
    source = get_source_info(source_id)
    if not source:
        return None, None  # No source info, cannot generate report

    report_date_str = datetime.now().strftime("%Y%m%d")
    report_name = f"{source['source_name']}_{report_period}_{report_date_str}"

    report_content = f"Market Analysis Report for {source['source_name']} ({source['source_type']})\n"
    report_content += f"Report Period: {report_period.replace('_', ' ').title()}\n"
    report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # --- Fetch Analysis Data ---
    analysis_results = fetch_analysis_for_report_period(source_id, report_period)
    if not analysis_results:
        report_content += "No analysis data available for this period.\n"
    else:
        for analysis in analysis_results:
            report_content += f"Analysis Type: {analysis['analysis_type'].replace('_', ' ').title()}\n"
            analysis_data = json.loads(analysis['analysis_result_json'])
            report_content += f"Analysis Timestamp: {analysis['analysis_timestamp']}\n"
            report_content += f"Results: {json.dumps(analysis_data, indent=4)}\n\n"

    # --- Save Text Report ---
    txt_report_path = f"{config.REPORT_DIR_TXT}/{report_name}.txt"
    with open(txt_report_path, 'w') as f:
        f.write(report_content)

    # --- Google Doc Report (Conceptual - basic text report created) ---
    gdoc_report_path = None  # In a full implementation, you'd create Google Doc here and set path

    # --- Save Report Metadata to DB ---
    db_manager.save_report(
        report_type='individual_website' if source['source_type'] == 'website' else 'individual_social_media',
        report_period=report_period,
        source_id=source_id,
        report_date=report_date_str,
        report_file_txt=txt_report_path,
        report_file_gdoc=gdoc_report_path
    )

    return txt_report_path, gdoc_report_path

def generate_global_report(report_period):
    """Generates a global report summarizing all monitored sources."""
    report_date_str = datetime.now().strftime("%Y%m%d")
    report_name = f"Global_Market_Tendencies_{report_period}_{report_date_str}"

    report_content = "Global Market Tendency Analysis Report\n"
    report_content += f"Report Period: {report_period.replace('_', ' ').title()}\n"
    report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    monitored_sources = db_manager.get_monitored_sources()
    for source in monitored_sources:
        report_content += f"--- Source: {source['source_name']} ({source['source_type']}) ---\n"
        analysis_results = fetch_analysis_for_report_period(source['source_id'], report_period)
        if analysis_results:
            for analysis in analysis_results:
                report_content += f"  Analysis Type: {analysis['analysis_type'].replace('_', ' ').title()}\n"
                analysis_data = json.loads(analysis['analysis_result_json'])
                report_content += f"  Analysis Timestamp: {analysis['analysis_timestamp']}\n"
                report_content += f"  Results: {json.dumps(analysis_data, indent=4)}\n\n"
        else:
            report_content += "  No analysis data available for this period.\n\n"

    # --- Save Text Report ---
    txt_report_path = f"{config.REPORT_DIR_TXT}/{report_name}.txt"
    with open(txt_report_path, 'w') as f:
        f.write(report_content)

    # --- Google Doc Report (Conceptual) ---
    gdoc_report_path = None  # In a full implementation, Google Doc generation logic here

    # --- Save Report Metadata to DB ---
    db_manager.save_report(
        report_type='global',
        report_period=report_period,
        source_id=None,
        report_date=report_date_str,
        report_file_txt=txt_report_path,
        report_file_gdoc=gdoc_report_path
    )

    return txt_report_path, gdoc_report_path

def get_source_info(source_id):
    """Helper function to get source information by ID."""
    sources = db_manager.get