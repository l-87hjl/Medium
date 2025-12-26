#!/usr/bin/env python3
"""
JPL Horizons Query Tool
Standalone script to query JPL Horizons for ephemeris data
No CORS issues - runs directly from command line
"""

import requests
import sys
from datetime import datetime

def convert_mpc_timestamp(mpc_timestamp):
    """
    Convert MPC timestamp (YYYY MM DD.dddddd) to UTC timestamp

    Args:
        mpc_timestamp: String in format "YYYY MM DD.dddddd"

    Returns:
        String in format "YYYY-MM-DD HH:MM:SS.sss"
    """
    parts = mpc_timestamp.strip().split()
    if len(parts) != 3:
        raise ValueError(f"Invalid MPC timestamp format: {mpc_timestamp}")

    year = int(parts[0])
    month = int(parts[1])
    day_decimal = float(parts[2])

    day = int(day_decimal)
    fraction = day_decimal - day

    # Convert fractional day to time
    total_seconds = fraction * 24 * 60 * 60
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60

    return f"{year:04d}-{month:02d}-{day:02d} {hours:02d}:{minutes:02d}:{seconds:06.3f}"

def query_horizons(object_id, observatory_code, mpc_timestamp):
    """
    Query JPL Horizons API for ephemeris data

    Args:
        object_id: SPK-ID or object name (e.g., '1004083' or 'C/2025 N1')
        observatory_code: MPC observatory code (e.g., 'G96', 'b67')
        mpc_timestamp: MPC format timestamp (e.g., '2025 12 19.007280')

    Returns:
        Response text from Horizons API
    """
    # Convert MPC timestamp to UTC
    utc_time = convert_mpc_timestamp(mpc_timestamp)

    # Prepare observer location
    center = observatory_code if observatory_code.startswith('@') else f'@{observatory_code}'

    # Build API request
    base_url = 'https://ssd.jpl.nasa.gov/api/horizons.api'
    params = {
        'format': 'text',
        'COMMAND': f"'{object_id}'",
        'OBJ_DATA': "'YES'",
        'MAKE_EPHEM': "'YES'",
        'EPHEM_TYPE': "'OBSERVER'",
        'CENTER': f"'{center}'",
        'TLIST': f"'{utc_time}'",
        'QUANTITIES': "'1,3,36,37'",  # RA/Dec, Rates, 3-sigma uncertainties
        'TIME_DIGITS': "'SECONDS'",
        'EXTRA_PREC': "'YES'",
        'CSV_FORMAT': "'NO'"
    }

    print(f"Querying JPL Horizons...")
    print(f"  Object: {object_id}")
    print(f"  Observatory: {observatory_code}")
    print(f"  MPC Time: {mpc_timestamp}")
    print(f"  UTC Time: {utc_time}")
    print()

    try:
        response = requests.get(base_url, params=params, timeout=30)

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}")

        return response.text

    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Check your internet connection.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")

def parse_ephemeris(response_text):
    """
    Parse ephemeris data from Horizons response

    Returns:
        Dictionary with extracted ephemeris data
    """
    lines = response_text.split('\n')
    results = {}

    # Find solution and epoch info
    for line in lines:
        if 'Solution name' in line or 'SPK' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                results['solution'] = parts[1].strip()

        if 'Epoch' in line:
            # Look for JD format
            import re
            match = re.search(r'(\d{7}\.\d+)', line)
            if match:
                results['epoch_jd'] = match.group(1)

    # Extract ephemeris data between $$SOE and $$EOE
    in_ephemeris = False
    ephemeris_lines = []

    for line in lines:
        if '$$SOE' in line:
            in_ephemeris = True
            continue
        if '$$EOE' in line:
            break
        if in_ephemeris and line.strip():
            ephemeris_lines.append(line)

    if not ephemeris_lines:
        raise Exception("No ephemeris data found in response")

    # Parse the ephemeris line
    ephemeris_line = ' '.join(ephemeris_lines).strip()
    parts = ephemeris_line.split()

    if len(parts) < 8:
        raise Exception(f"Insufficient data in ephemeris output")

    # Extract fields
    idx = 0
    results['utc_time'] = f"{parts[idx]} {parts[idx+1]}"
    idx += 2

    # RA (HH MM SS.sss)
    results['ra_icrf'] = f"{parts[idx]} {parts[idx+1]} {parts[idx+2]}"
    idx += 3

    # DEC (+/-DD MM SS.ss)
    results['dec_icrf'] = f"{parts[idx]} {parts[idx+1]} {parts[idx+2]}"
    idx += 3

    # Remaining fields - rates and uncertainties
    remaining = parts[idx:]
    if len(remaining) >= 7:
        # Try to extract from the end (more reliable)
        results['theta'] = remaining[-1]
        results['smia_3sig'] = remaining[-2]
        results['smaa_3sig'] = remaining[-3]
        results['dec_3sigma'] = remaining[-4]
        results['ra_3sigma'] = remaining[-5]
        results['ddec_dt'] = remaining[-6]
        results['dra_cosd'] = remaining[-7]

    return results

def print_results(data):
    """Print results in a formatted table"""
    print("="*70)
    print("EPHEMERIS DATA")
    print("="*70)
    print()

    if 'solution' in data:
        print(f"Solution:     {data['solution']}")
    if 'epoch_jd' in data:
        print(f"Epoch (JD):   {data['epoch_jd']}")
    print(f"UTC Time:     {data['utc_time']}")
    print()

    print(f"{'Parameter':<20} {'Value':<25} {'Unit':<15}")
    print("-"*70)
    print(f"{'RA (ICRF)':<20} {data.get('ra_icrf', 'N/A'):<25} {'HH MM SS.sss':<15}")
    print(f"{'DEC (ICRF)':<20} {data.get('dec_icrf', 'N/A'):<25} {'DD MM SS.ss':<15}")
    print(f"{'dRA*cosD':<20} {data.get('dra_cosd', 'N/A'):<25} {'arcsec/hr':<15}")
    print(f"{'d(DEC)/dt':<20} {data.get('ddec_dt', 'N/A'):<25} {'arcsec/hr':<15}")
    print(f"{'RA_3sigma':<20} {data.get('ra_3sigma', 'N/A'):<25} {'arcsec':<15}")
    print(f"{'DEC_3sigma':<20} {data.get('dec_3sigma', 'N/A'):<25} {'arcsec':<15}")
    print(f"{'SMAA_3sig':<20} {data.get('smaa_3sig', 'N/A'):<25} {'arcsec':<15}")
    print(f"{'SMIA_3sig':<20} {data.get('smia_3sig', 'N/A'):<25} {'arcsec':<15}")
    print(f"{'Theta':<20} {data.get('theta', 'N/A'):<25} {'deg (E of N)':<15}")
    print("="*70)
    print()

def main():
    """Main function"""
    print("="*70)
    print("JPL HORIZONS QUERY TOOL")
    print("="*70)
    print()

    # Get input from command line or interactive
    if len(sys.argv) == 4:
        object_id = sys.argv[1]
        observatory_code = sys.argv[2]
        mpc_timestamp = sys.argv[3]
    else:
        print("Usage: python jpl_horizons_query.py <object_id> <observatory_code> <mpc_timestamp>")
        print("\nExample:")
        print("  python jpl_horizons_query.py 1004083 G96 '2025 12 19.007280'")
        print()
        print("Or enter interactively:")
        print()

        object_id = input("Object ID (SPK-ID or name): ").strip()
        observatory_code = input("Observatory code (e.g., G96, b67): ").strip()
        mpc_timestamp = input("MPC timestamp (YYYY MM DD.dddddd): ").strip()
        print()

    try:
        # Query Horizons API
        response = query_horizons(object_id, observatory_code, mpc_timestamp)

        # Save raw response
        output_file = f'horizons_query_{object_id}_{observatory_code}.txt'
        with open(output_file, 'w') as f:
            f.write(response)
        print(f"✓ Raw response saved to: {output_file}")
        print()

        # Parse and display results
        data = parse_ephemeris(response)
        print_results(data)

    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
