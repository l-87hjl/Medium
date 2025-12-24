#!/usr/bin/env python3
"""
High-precision O-C residuals analysis for C/2025 N1 (ATLAS)
Compares JPL Solution 44 predictions vs actual December 19 observation
"""

import requests
from datetime import datetime
import math

def query_horizons(command, center, time_str):
    """
    Query JPL Horizons API with proper parameters

    Args:
        command: SPK-ID of the object (e.g., '1004083;')
        center: Observer location code (e.g., '@G96')
        time_str: UT time in format 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Response text from Horizons API
    """
    base_url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    params = {
        'format': 'text',
        'COMMAND': f"'{command}'",
        'OBJ_DATA': "'YES'",
        'MAKE_EPHEM': "'YES'",
        'EPHEM_TYPE': "'OBSERVER'",
        'CENTER': f"'{center}'",
        'TLIST': f"'{time_str}'",
        'QUANTITIES': "'1,3,36,37'",  # RA/Dec, Rates, 3-sigma uncertainties
        'TIME_DIGITS': "'SECONDS'",
        'EXTRA_PREC': "'YES'",
        'CSV_FORMAT': "'NO'"
    }

    print("Querying JPL Horizons API...")
    print(f"Object: {command}")
    print(f"Observer: {center}")
    print(f"Time: {time_str}")
    print()

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    return response.text

def parse_ra_dec(ra_str, dec_str):
    """
    Convert RA/Dec strings to decimal degrees

    Args:
        ra_str: RA in format "HH MM SS.sss" or "HH:MM:SS.sss"
        dec_str: Dec in format "+DD MM SS.ss" or "+DD:MM:SS.ss"

    Returns:
        Tuple of (ra_deg, dec_deg)
    """
    # Parse RA (hours, minutes, seconds)
    ra_parts = ra_str.replace(':', ' ').split()
    ra_h = float(ra_parts[0])
    ra_m = float(ra_parts[1])
    ra_s = float(ra_parts[2])
    ra_deg = (ra_h + ra_m/60.0 + ra_s/3600.0) * 15.0  # Convert hours to degrees

    # Parse Dec (degrees, arcminutes, arcseconds)
    dec_parts = dec_str.replace(':', ' ').split()
    dec_sign = 1 if dec_parts[0][0] != '-' else -1
    dec_d = abs(float(dec_parts[0]))
    dec_m = float(dec_parts[1])
    dec_s = float(dec_parts[2])
    dec_deg = dec_sign * (dec_d + dec_m/60.0 + dec_s/3600.0)

    return ra_deg, dec_deg

def calculate_residuals(obs_ra_deg, obs_dec_deg, calc_ra_deg, calc_dec_deg):
    """
    Calculate O-C residuals in arcseconds

    Args:
        obs_ra_deg, obs_dec_deg: Observed position in decimal degrees
        calc_ra_deg, calc_dec_deg: Calculated position in decimal degrees

    Returns:
        Tuple of (ra_residual_arcsec, dec_residual_arcsec, total_separation_arcsec)
    """
    # RA residual with cos(dec) correction
    ra_diff_deg = obs_ra_deg - calc_ra_deg
    dec_avg_rad = math.radians((obs_dec_deg + calc_dec_deg) / 2.0)
    ra_residual_arcsec = ra_diff_deg * 3600.0 * math.cos(dec_avg_rad)

    # Dec residual
    dec_diff_deg = obs_dec_deg - calc_dec_deg
    dec_residual_arcsec = dec_diff_deg * 3600.0

    # Total angular separation
    total_separation_arcsec = math.sqrt(ra_residual_arcsec**2 + dec_residual_arcsec**2)

    return ra_residual_arcsec, dec_residual_arcsec, total_separation_arcsec

def main():
    # Step 1: Query JPL Horizons for calculated position
    print("="*80)
    print("COMET C/2025 N1 (ATLAS) - SOLUTION 44 RESIDUALS ANALYSIS")
    print("December 19, 2025 'Final Exam' Observation")
    print("="*80)
    print()

    command = "1004083;"  # SPK-ID for C/2025 N1 (ATLAS)
    center = "@G96"  # Mt. Lemmon Survey
    obs_time = "2025-12-19 01:21:40"  # UT

    try:
        horizons_response = query_horizons(command, center, obs_time)

        # Save raw response
        with open('horizons_response.txt', 'w') as f:
            f.write(horizons_response)
        print("✓ Horizons response saved to horizons_response.txt")
        print()

        # Parse the ephemeris table
        lines = horizons_response.split('\n')

        # Find the ephemeris data (between $$SOE and $$EOE markers)
        in_ephemeris = False
        ephem_data = []

        for line in lines:
            if '$$SOE' in line:
                in_ephemeris = True
                continue
            elif '$$EOE' in line:
                in_ephemeris = False
                break
            elif in_ephemeris and line.strip():
                ephem_data.append(line)

        if not ephem_data:
            print("ERROR: Could not find ephemeris data in response")
            print("\nSearching for relevant data in response...")
            for i, line in enumerate(lines):
                if 'R.A.' in line or 'DEC' in line or '2025' in line:
                    print(f"Line {i}: {line}")
            return

        # Parse the ephemeris line
        # Format: Date (UT), R.A. (ICRF), DEC (ICRF), dRA*cosD, d(DEC)/dt, Unc_RA, Unc_DEC, POS_3sigma
        print("Parsing calculated (C) position from JPL Horizons...")
        for line in ephem_data:
            print(f"Ephemeris line: {line}")

        # The data line should contain the position
        data_line = ephem_data[0] if ephem_data else ""

        # Parse the calculated position
        # This will need to be adjusted based on actual format
        parts = data_line.split()

        if len(parts) >= 6:
            calc_ra_str = f"{parts[2]} {parts[3]} {parts[4]}"  # Typically format: HH MM SS.sss
            calc_dec_str = f"{parts[5]} {parts[6]} {parts[7]}"  # Typically format: +DD MM SS.ss

            print(f"Calculated RA: {calc_ra_str}")
            print(f"Calculated Dec: {calc_dec_str}")
            print()

            # Look for POS_3sigma in the line or nearby
            pos_3sigma = None
            for part in parts:
                try:
                    val = float(part)
                    if 0.01 < val < 100:  # Reasonable range for 3-sigma in arcseconds
                        pos_3sigma = val
                except:
                    pass

            # Step 2: Define observed position
            print("OBSERVED POSITION (from December 19 MPEC):")
            obs_ra_str = "11 05 53.640"  # 11h 05m 53.640s
            obs_dec_str = "+05 24 55.44"  # +05° 24' 55.44"
            print(f"RA:  {obs_ra_str}")
            print(f"Dec: {obs_dec_str}")
            print()

            # Step 3: Convert to decimal degrees
            obs_ra_deg, obs_dec_deg = parse_ra_dec(obs_ra_str, obs_dec_str)
            calc_ra_deg, calc_dec_deg = parse_ra_dec(calc_ra_str, calc_dec_str)

            print("COORDINATE CONVERSION:")
            print(f"Observed:   RA = {obs_ra_deg:.8f}°, Dec = {obs_dec_deg:.8f}°")
            print(f"Calculated: RA = {calc_ra_deg:.8f}°, Dec = {calc_dec_deg:.8f}°")
            print()

            # Step 4: Calculate residuals
            ra_res, dec_res, total_sep = calculate_residuals(
                obs_ra_deg, obs_dec_deg, calc_ra_deg, calc_dec_deg
            )

            print("="*80)
            print("RESIDUALS (O-C):")
            print("="*80)
            print(f"RA residual:  {ra_res:+10.3f} arcsec  (with cos(dec) correction)")
            print(f"Dec residual: {dec_res:+10.3f} arcsec")
            print(f"Total separation: {total_sep:10.3f} arcsec = {total_sep/3600.0:.6f}°")
            print()

            if pos_3sigma:
                print(f"JPL 3-sigma uncertainty: {pos_3sigma:.3f} arcsec")
                sigma_ratio = total_sep / pos_3sigma
                print(f"Residual / 3-sigma: {sigma_ratio:.1f}×")
                print()

                if total_sep > pos_3sigma:
                    print("⚠️  VERDICT: SOLUTION 44 FAILED")
                    print(f"   The observed position is {sigma_ratio:.1f}× beyond the 3-sigma")
                    print(f"   predicted error margin. This is a statistically significant")
                    print(f"   prediction failure.")
                else:
                    print("✓ VERDICT: Within predicted uncertainty")
            else:
                print("Note: Could not extract POS_3sigma from response")
                print("      Manual verification needed")

            print()
            print("="*80)

        else:
            print("ERROR: Unexpected ephemeris format")
            print(f"Data line: {data_line}")
            print(f"Parts: {parts}")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
