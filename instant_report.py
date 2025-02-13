import json
from datetime import datetime

from market_analyzer import (config, data_analyzer, data_fetcher,
                             db_manager, report_generator)

def generate_instant_report(source_id=None, report_period='last_7_days'):
    """Generates an instant report for a given source or all sources."""

    if source_id:
        # Generate report for a specific source
        txt_path, gdoc_path = report_generator.generate_individual_report(
            source_id, report_period)
        if txt_path:
            print(f"Individual report generated at: {txt_path}")
        else:
            print("Failed to generate individual report.")
    else:
        # Generate global report
        report_content = "Global Market Tendency Analysis Report\n"
        report_content += f"Report Period: Last 7 Days\n"
        report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        monitored_sources = db_manager.get_monitored_sources()
        for source in monitored_sources:
            report_content += f"--- Source: {source['source_name']} ({source['source_type']}) ---\n"

            if source['source_type'] == 'website':
                # Fetch website content
                raw_content = data_fetcher.fetch_website_content(
                    source['source_url'])
                if raw_content:
                    # Perform analysis and add to report
                    analysis_results = data_analyzer.analyze_raw_data_snapshot(
                        raw_content=raw_content)
                    report_content += format_analysis_results(
                        analysis_results)
                else:
                    report_content += "  No data available.\n\n"
            elif source['source_type'] in [
                    'x.com', 'instagram', 'facebook', 'linkedin', 'tiktok'
            ]:
                # Fetch last 5 social media posts
                posts = fetch_last_n_social_media_posts(
                    source['source_url'], source['source_type'], n=5)
                if posts:
                    for post in posts:
                        # Perform analysis for each post and add to report
                        analysis_results = data_analyzer.analyze_raw_data_snapshot(
                            raw_content=post)
                        report_content += format_analysis_results(
                            analysis_results)
                else:
                    report_content += "  No posts available.\n\n"
            else:
                report_content += "  Unsupported source type.\n\n"

        # Save global report
        txt_report_path = f"{config.REPORT_DIR_TXT}/Global_Market_Tendencies_instant_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(txt_report_path, 'w') as f:
            f.write(report_content)

        print(f"Global report generated at: {txt_report_path}")


def fetch_last_n_social_media_posts(source_url, source_type, n=5):
    """Fetches the last N posts for a social media source."""
    # Placeholder - Replace with actual social media API calls
    print(
        f"Fetching last {n} posts from {source_url} ({source_type}) - Not yet implemented"
    )
    return  # Return an empty list for now

def format_analysis_results(analysis_results):
    """Formats analysis results for the report."""
    formatted_results = ""
    if analysis_results:
        for analysis_type, result in analysis_results.items():
            formatted_results += f"  Analysis Type: {analysis_type.replace('_', ' ').title()}\n"
            formatted_results += f"  Results: {json.dumps(result, indent=4)}\n\n"
    return formatted_results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate instant market analysis reports.")
    parser.add_argument(
        "--source_id",
        type=int,
        help="Source ID to generate a report for (optional)")
    parser.add_argument(
        "--report_period",
        type=str,
        default='last_7_days',
        choices=['last_7_days', 'whole_period'],
        help="Report period (default: last_7_days)")
    args = parser.parse_args()

    generate_instant_report(args.source_id, args.report_period)