#!/usr/bin/env python3
"""
Parse observations from HTML file and convert to CSV format

This script extracts observation data from an HTML file
and converts it to CSV format for use with generate_solution44_table.py

Usage:
  python3 parse_observations_html.py observations.html

Output:
  observations.csv
"""

import sys
import re
from html.parser import HTMLParser

class ObservationParser(HTMLParser):
    """Parse HTML table containing observation data"""

    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.rows = []
        self.cell_data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ('td', 'th') and self.in_row:
            self.in_cell = True
            self.cell_data = []

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            if self.current_row:
                self.rows.append(self.current_row)
            self.in_row = False
        elif tag in ('td', 'th') and self.in_cell:
            self.current_row.append(''.join(self.cell_data).strip())
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.cell_data.append(data)

def extract_observations_from_html(html_content):
    """
    Extract observations from HTML content

    Tries multiple strategies:
    1. Parse HTML tables
    2. Look for specific patterns in text
    3. Extract from pre-formatted sections
    """
    observations = []

    # Strategy 1: Parse HTML tables
    parser = ObservationParser()
    parser.feed(html_content)

    for row in parser.rows:
        if len(row) >= 4:
            # Try to identify timestamp, observatory, RA, Dec
            # Common formats:
            # [timestamp, observatory, ra, dec]
            # [observatory, timestamp, ra, dec]
            # etc.

            # Look for timestamp pattern (YYYY-MM-DD HH:MM:SS or similar)
            timestamp_pattern = r'\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}:\d{2}'

            timestamp = None
            observatory = None
            ra = None
            dec = None

            for cell in row:
                # Check if this looks like a timestamp
                if re.search(timestamp_pattern, cell):
                    timestamp = cell
                # Check if this looks like an observatory code (usually 3-4 chars/digits)
                elif re.match(r'^[A-Z0-9]{3,4}$', cell.strip()):
                    observatory = cell
                # Check if this looks like RA (HH MM SS format)
                elif re.match(r'^\d{1,2}\s+\d{2}\s+\d{2}', cell):
                    if ra is None:  # First match is RA
                        ra = cell
                    else:  # Second match might be Dec (if in DMS format)
                        dec = cell
                # Check if this looks like Dec (±DD MM SS format)
                elif re.match(r'^[+-]?\d{1,2}\s+\d{2}\s+\d{2}', cell):
                    dec = cell

            if timestamp and observatory and ra and dec:
                observations.append({
                    'timestamp': timestamp,
                    'observatory': observatory,
                    'obs_ra': ra,
                    'obs_dec': dec
                })

    # Strategy 2: Look for specific patterns in text
    if not observations:
        # Try to find lines that look like observation records
        lines = html_content.split('\n')

        for line in lines:
            # Look for patterns like:
            # 2025-12-20 01:23:45  G96  11 05 53.640  +05 24 55.44
            match = re.search(
                r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
                r'([A-Z0-9]{3,4})\s+'
                r'(\d{1,2}\s+\d{2}\s+\d{2}\.\d+)\s+'
                r'([+-]?\d{1,2}\s+\d{2}\s+\d{2}\.\d+)',
                line
            )

            if match:
                observations.append({
                    'timestamp': match.group(1),
                    'observatory': match.group(2),
                    'obs_ra': match.group(3),
                    'obs_dec': match.group(4)
                })

    return observations

def write_csv(observations, output_file='observations.csv'):
    """Write observations to CSV file"""
    import csv

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'observatory', 'obs_ra', 'obs_dec'])
        writer.writeheader()
        writer.writerows(observations)

    print(f"✓ Wrote {len(observations)} observations to {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_observations_html.py observations.html")
        print()
        print("This script extracts observation data from HTML and converts to CSV")
        print("Output: observations.csv")
        sys.exit(1)

    html_file = sys.argv[1]

    print("="*80)
    print("OBSERVATION HTML PARSER")
    print("="*80)
    print()

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        print(f"Loaded {len(html_content)} bytes from {html_file}")
        print()

        observations = extract_observations_from_html(html_content)

        if observations:
            print(f"Found {len(observations)} observations:")
            print()
            for i, obs in enumerate(observations[:5], 1):  # Show first 5
                print(f"  {i}. {obs['timestamp']} @ {obs['observatory']}: "
                      f"RA={obs['obs_ra']} Dec={obs['obs_dec']}")

            if len(observations) > 5:
                print(f"  ... and {len(observations) - 5} more")

            print()

            write_csv(observations)

            print()
            print("Next step:")
            print("  python3 generate_solution44_table.py observations.csv")

        else:
            print("⚠ No observations found in HTML file")
            print()
            print("The HTML file might use a different format.")
            print("Please check the file manually or create observations.csv directly:")
            print()
            print("  timestamp,observatory,obs_ra,obs_dec")
            print("  2025-12-19 01:21:40,G96,11 05 53.640,+05 24 55.44")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print()
    print("="*80)

if __name__ == "__main__":
    main()
