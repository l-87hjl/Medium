#!/usr/bin/env python3
"""
Generate JPL Solution 44 ephemeris table for multiple observations

This script queries JPL Horizons for calculated positions at each
observation timestamp/observatory combination, creating a comparison table
of observed vs calculated positions.

Usage:
  1. Create a CSV file with observations (see template below)
  2. Run: python3 generate_solution44_table.py observations.csv
  3. Output will be saved as solution44_comparison_table.html

CSV Format:
  timestamp,observatory,obs_ra,obs_dec
  2025-12-19 01:21:40,G96,11 05 53.640,+05 24 55.44
  2025-12-20 02:30:15,703,11 06 12.345,+05 25 10.20
"""

import sys
import csv
import requests
from datetime import datetime
import math

def query_horizons_single(timestamp, observatory_code):
    """
    Query JPL Horizons for a single timestamp and observatory

    Args:
        timestamp: UT time string (e.g., '2025-12-19 01:21:40')
        observatory_code: MPC observatory code (e.g., 'G96', '703')

    Returns:
        Dictionary with calculated RA, Dec, and uncertainties
    """
    base_url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    # Ensure observatory code has @ prefix
    if not observatory_code.startswith('@'):
        observatory_code = f'@{observatory_code}'

    params = {
        'format': 'text',
        'COMMAND': "'1004083;'",  # C/2025 N1 (ATLAS)
        'OBJ_DATA': "'YES'",
        'MAKE_EPHEM': "'YES'",
        'EPHEM_TYPE': "'OBSERVER'",
        'CENTER': f"'{observatory_code}'",
        'TLIST': f"'{timestamp}'",
        'QUANTITIES': "'1,3,36,37'",  # RA/Dec, Rates, Uncertainties
        'TIME_DIGITS': "'SECONDS'",
        'EXTRA_PREC': "'YES'",
        'CSV_FORMAT': "'NO'"
    }

    try:
        response = requests.get(base_url, params=params, timeout=30)

        if response.status_code != 200:
            return {'error': f'HTTP {response.status_code}'}

        # Parse the ephemeris section
        lines = response.text.split('\n')
        in_ephemeris = False

        for line in lines:
            if '$$SOE' in line:
                in_ephemeris = True
                continue
            elif '$$EOE' in line:
                break
            elif in_ephemeris and line.strip():
                # Parse the ephemeris line
                # Format varies, but typically: Date Time RA Dec Rates Uncertainties
                parts = line.split()

                if len(parts) >= 10:
                    try:
                        # Extract RA (typically parts 2-4: HH MM SS.SSS)
                        ra_h = parts[2] if len(parts) > 2 else '00'
                        ra_m = parts[3] if len(parts) > 3 else '00'
                        ra_s = parts[4] if len(parts) > 4 else '00.000'
                        calc_ra = f"{ra_h} {ra_m} {ra_s}"

                        # Extract Dec (typically parts 5-7: ±DD MM SS.SS)
                        dec_d = parts[5] if len(parts) > 5 else '+00'
                        dec_m = parts[6] if len(parts) > 6 else '00'
                        dec_s = parts[7] if len(parts) > 7 else '00.00'
                        calc_dec = f"{dec_d} {dec_m} {dec_s}"

                        # Try to find POS_3sigma (usually near the end)
                        pos_3sigma = None
                        for part in parts[8:]:
                            try:
                                val = float(part)
                                if 0.001 < val < 1000:  # Reasonable range for arcsec
                                    pos_3sigma = val
                                    break
                            except:
                                continue

                        return {
                            'calc_ra': calc_ra,
                            'calc_dec': calc_dec,
                            'pos_3sigma': pos_3sigma,
                            'raw_line': line.strip()
                        }
                    except Exception as e:
                        return {'error': f'Parse error: {e}', 'raw_line': line.strip()}

        return {'error': 'No ephemeris data found'}

    except Exception as e:
        return {'error': str(e)}

def hms_to_degrees(hms_str):
    """Convert HH MM SS.SSS to decimal degrees"""
    parts = hms_str.split()
    h = float(parts[0])
    m = float(parts[1])
    s = float(parts[2])
    return (h + m/60.0 + s/3600.0) * 15.0

def dms_to_degrees(dms_str):
    """Convert ±DD MM SS.SS to decimal degrees"""
    parts = dms_str.split()
    sign = 1 if parts[0][0] != '-' else -1
    d = abs(float(parts[0]))
    m = float(parts[1])
    s = float(parts[2])
    return sign * (d + m/60.0 + s/3600.0)

def calculate_residual(obs_ra, obs_dec, calc_ra, calc_dec):
    """Calculate O-C residual in arcseconds"""
    obs_ra_deg = hms_to_degrees(obs_ra)
    obs_dec_deg = dms_to_degrees(obs_dec)
    calc_ra_deg = hms_to_degrees(calc_ra)
    calc_dec_deg = dms_to_degrees(calc_dec)

    # RA residual with cos(dec) correction
    dec_avg_rad = math.radians((obs_dec_deg + calc_dec_deg) / 2.0)
    ra_res = (obs_ra_deg - calc_ra_deg) * 3600.0 * math.cos(dec_avg_rad)

    # Dec residual
    dec_res = (obs_dec_deg - calc_dec_deg) * 3600.0

    # Total separation
    total = math.sqrt(ra_res**2 + dec_res**2)

    return ra_res, dec_res, total

def generate_html_table(observations, results):
    """Generate HTML table with observations and Solution 44 predictions"""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>C/2025 N1 (ATLAS) - Solution 44 Comparison Table</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            font-size: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-size: 12px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .error {
            color: red;
            font-style: italic;
        }
        .good {
            color: green;
        }
        .warning {
            color: orange;
        }
        .bad {
            color: red;
        }
        .header-info {
            background-color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }
        .residual {
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>C/2025 N1 (ATLAS) - JPL Solution 44 Comparison Table</h1>

    <div class="header-info">
        <p><strong>Object:</strong> C/2025 N1 (ATLAS) / 3I/ATLAS (SPK-ID: 1004083)</p>
        <p><strong>Solution:</strong> JPL #44 (published 2025-12-17)</p>
        <p><strong>Generated:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """ UTC</p>
        <p><strong>Total Observations:</strong> """ + str(len(observations)) + """</p>
    </div>

    <table>
        <thead>
            <tr>
                <th rowspan="2">Timestamp (UT)</th>
                <th rowspan="2">Obs</th>
                <th colspan="2">Observed (O)</th>
                <th colspan="2">Calculated (C) - Solution 44</th>
                <th colspan="3">Residuals (O-C)</th>
                <th rowspan="2">3σ<br>(arcsec)</th>
                <th rowspan="2">σ ratio</th>
            </tr>
            <tr>
                <th>RA</th>
                <th>Dec</th>
                <th>RA</th>
                <th>Dec</th>
                <th>ΔRA<br>(arcsec)</th>
                <th>ΔDec<br>(arcsec)</th>
                <th>Total<br>(arcsec)</th>
            </tr>
        </thead>
        <tbody>
"""

    for i, obs in enumerate(observations):
        result = results[i]

        html += f"""            <tr>
                <td>{obs['timestamp']}</td>
                <td>{obs['observatory']}</td>
                <td>{obs['obs_ra']}</td>
                <td>{obs['obs_dec']}</td>
"""

        if 'error' in result:
            html += f"""                <td colspan="7" class="error">{result['error']}</td>
"""
        else:
            calc_ra = result.get('calc_ra', 'N/A')
            calc_dec = result.get('calc_dec', 'N/A')
            pos_3sigma = result.get('pos_3sigma')

            html += f"""                <td>{calc_ra}</td>
                <td>{calc_dec}</td>
"""

            # Calculate residuals
            try:
                ra_res, dec_res, total_res = calculate_residual(
                    obs['obs_ra'], obs['obs_dec'],
                    calc_ra, calc_dec
                )

                # Determine color coding
                if pos_3sigma:
                    sigma_ratio = total_res / pos_3sigma
                    if sigma_ratio <= 1.0:
                        color_class = "good"
                    elif sigma_ratio <= 3.0:
                        color_class = "warning"
                    else:
                        color_class = "bad"

                    sigma_str = f"{sigma_ratio:.1f}×"
                else:
                    color_class = ""
                    sigma_str = "N/A"

                html += f"""                <td class="residual {color_class}">{ra_res:+.3f}</td>
                <td class="residual {color_class}">{dec_res:+.3f}</td>
                <td class="residual {color_class}">{total_res:.3f}</td>
                <td>{pos_3sigma if pos_3sigma else 'N/A'}</td>
                <td class="{color_class}">{sigma_str}</td>
"""
            except Exception as e:
                html += f"""                <td colspan="5" class="error">Calc error: {e}</td>
"""

        html += """            </tr>
"""

    html += """        </tbody>
    </table>

    <div class="header-info" style="margin-top: 20px;">
        <p><strong>Legend:</strong></p>
        <ul>
            <li><span class="good">Green</span>: Within 3-sigma (good prediction)</li>
            <li><span class="warning">Orange</span>: 1-3× beyond 3-sigma (marginal)</li>
            <li><span class="bad">Red</span>: >3× beyond 3-sigma (prediction failure)</li>
        </ul>
        <p><strong>Notes:</strong></p>
        <ul>
            <li>RA residuals include cos(dec) correction</li>
            <li>σ ratio = Total residual / 3-sigma uncertainty</li>
            <li>Solution 44 predictions queried from JPL Horizons API</li>
        </ul>
    </div>
</body>
</html>
"""

    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_solution44_table.py observations.csv")
        print()
        print("CSV Format:")
        print("  timestamp,observatory,obs_ra,obs_dec")
        print("  2025-12-19 01:21:40,G96,11 05 53.640,+05 24 55.44")
        print()
        sys.exit(1)

    csv_file = sys.argv[1]

    print("="*80)
    print("JPL SOLUTION 44 TABLE GENERATOR")
    print("="*80)
    print()

    # Read observations from CSV
    observations = []

    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                observations.append({
                    'timestamp': row['timestamp'].strip(),
                    'observatory': row['observatory'].strip(),
                    'obs_ra': row['obs_ra'].strip(),
                    'obs_dec': row['obs_dec'].strip()
                })

        print(f"Loaded {len(observations)} observations from {csv_file}")
        print()

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Query Horizons for each observation
    results = []

    for i, obs in enumerate(observations, 1):
        print(f"[{i}/{len(observations)}] Querying: {obs['timestamp']} @ {obs['observatory']}...", end=' ')

        result = query_horizons_single(obs['timestamp'], obs['observatory'])
        results.append(result)

        if 'error' in result:
            print(f"ERROR: {result['error']}")
        else:
            print(f"✓")

        # Small delay to be nice to JPL servers
        import time
        time.sleep(0.5)

    print()
    print("Generating HTML table...")

    html = generate_html_table(observations, results)

    output_file = 'solution44_comparison_table.html'
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✓ Table saved to: {output_file}")
    print()
    print("="*80)

if __name__ == "__main__":
    main()
