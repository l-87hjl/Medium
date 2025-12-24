#!/usr/bin/env python3
"""
Test script to verify JPL Horizons API query works correctly
Run this first to test your connection and query syntax
"""

import requests
import sys

def test_horizons_query():
    """
    Test JPL Horizons API with the exact query for C/2025 N1 (ATLAS)
    """
    print("="*80)
    print("JPL HORIZONS API TEST")
    print("="*80)
    print()

    # The exact URL - Method 1: Let requests handle encoding
    base_url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    params = {
        'format': 'text',
        'COMMAND': "'1004083;'",           # C/2025 N1 (ATLAS) SPK-ID
        'OBJ_DATA': "'YES'",
        'MAKE_EPHEM': "'YES'",
        'EPHEM_TYPE': "'OBSERVER'",
        'CENTER': "'@G96'",                # Mt. Lemmon Survey
        'TLIST': "'2025-12-19 01:21:40'",  # Exact observation time
        'QUANTITIES': "'1,3,36,37'",       # RA/Dec, rates, uncertainties
        'TIME_DIGITS': "'SECONDS'",
        'EXTRA_PREC': "'YES'",
        'CSV_FORMAT': "'NO'"
    }

    print("Query Parameters:")
    print(f"  Object: C/2025 N1 (ATLAS) [1004083]")
    print(f"  Observer: Mt. Lemmon Survey [@G96]")
    print(f"  Time: 2025-12-19 01:21:40 UT")
    print(f"  Quantities: 1 (RA/Dec), 3 (Rates), 36-37 (Uncertainties)")
    print()

    # Construct full URL for display
    param_str = "&".join([f"{k}={v}" for k, v in params.items()])
    full_url = f"{base_url}?{param_str}"

    print("Full URL (copy this to browser if script fails):")
    print(full_url)
    print()

    # Try the query
    print("Sending request to JPL Horizons...")
    print()

    try:
        response = requests.get(base_url, params=params, timeout=30)

        if response.status_code == 200:
            print("✓ SUCCESS! Query returned data.")
            print()

            # Save the response
            with open('horizons_test_response.txt', 'w') as f:
                f.write(response.text)
            print("Response saved to: horizons_test_response.txt")
            print()

            # Parse the response
            lines = response.text.split('\n')

            # Find the ephemeris data
            in_ephemeris = False
            ephemeris_lines = []

            for line in lines:
                if '$$SOE' in line:
                    in_ephemeris = True
                    continue
                elif '$$EOE' in line:
                    in_ephemeris = False
                    break
                elif in_ephemeris and line.strip():
                    ephemeris_lines.append(line)

            if ephemeris_lines:
                print("="*80)
                print("EPHEMERIS DATA FOUND:")
                print("="*80)
                for line in ephemeris_lines:
                    print(line)
                print()

                # Try to parse the values
                print("="*80)
                print("EXTRACTING VALUES:")
                print("="*80)

                data_line = ephemeris_lines[0]
                parts = data_line.split()

                if len(parts) >= 10:
                    # Typical format: Date Time RA(h m s) Dec(d m s) rates uncertainties
                    # This is approximate - actual format may vary
                    print(f"Date/Time: {parts[0]} {parts[1]}")
                    print(f"RA (approx): {parts[3]} {parts[4]} {parts[5]}")
                    print(f"Dec (approx): {parts[6]} {parts[7]} {parts[8]}")
                    print()
                    print("⚠️  IMPORTANT: Verify the exact column positions in the full response file.")
                    print("   The column headers are shown before the $$SOE marker.")
                else:
                    print(f"Found {len(parts)} parts in data line")
                    print("Raw data:", data_line)

                print()
                print("="*80)
                print("NEXT STEPS:")
                print("="*80)
                print("1. Open horizons_test_response.txt")
                print("2. Find the line between $$SOE and $$EOE")
                print("3. Extract the RA, Dec, and POS_3sigma values")
                print("4. Enter them into comet_residuals_manual_entry.py")
                print("5. Run: python3 comet_residuals_manual_entry.py")
                print()

            else:
                print("⚠️  WARNING: No ephemeris data found between $$SOE and $$EOE markers")
                print()
                print("This might mean:")
                print("- The query succeeded but no ephemeris was generated")
                print("- Check horizons_test_response.txt for error messages")
                print("- The time might be outside the solution's valid range")
                print()

            return True

        else:
            print(f"✗ ERROR: HTTP {response.status_code}")
            print()
            print("Response:")
            print(response.text[:500])
            print()
            return False

    except requests.exceptions.Timeout:
        print("✗ ERROR: Request timed out")
        print()
        print("The JPL server might be slow or unreachable.")
        print("Try again later or use the web interface:")
        print("https://ssd.jpl.nasa.gov/horizons/app.html")
        print()
        return False

    except requests.exceptions.RequestException as e:
        print(f"✗ ERROR: Request failed")
        print(f"   {type(e).__name__}: {e}")
        print()
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- Proxy/firewall blocking the request")
        print("- JPL server temporarily down")
        print()
        print("Try using the web interface instead:")
        print("https://ssd.jpl.nasa.gov/horizons/app.html")
        print()
        return False

def show_manual_instructions():
    """
    Show instructions for using the web interface
    """
    print()
    print("="*80)
    print("MANUAL QUERY INSTRUCTIONS (Web Interface)")
    print("="*80)
    print()
    print("If the automated query doesn't work, use the web interface:")
    print()
    print("1. Go to: https://ssd.jpl.nasa.gov/horizons/app.html")
    print()
    print("2. Enter these settings:")
    print("   Target Body: C/2025 N1  (or 1004083)")
    print("   Observer Location: G96")
    print("   Time Start: 2025-12-19 01:21:40")
    print("   Time Stop: 2025-12-19 01:21:40")
    print()
    print("3. Click 'Table Settings':")
    print("   - Check: 1 (RA & DEC)")
    print("   - Check: 3 (Rates)")
    print("   - Check: 36 (1-sigma uncertainties)")
    print("   - Check: 37 (3-sigma uncertainty)")
    print("   - Set: EXTRA_PREC = YES")
    print("   - Set: TIME_DIGITS = SECONDS")
    print()
    print("4. Click 'Generate Ephemeris'")
    print()
    print("5. Look for the data between $$SOE and $$EOE markers")
    print()
    print("6. Extract:")
    print("   - RA (format: HH MM SS.SSS)")
    print("   - Dec (format: ±DD MM SS.SS)")
    print("   - POS_3sigma (a number in arcseconds)")
    print()
    print("7. Enter these values into comet_residuals_manual_entry.py")
    print()
    print("="*80)

if __name__ == "__main__":
    print()
    success = test_horizons_query()

    if not success:
        show_manual_instructions()

    print()
    print("="*80)
    print("TEST COMPLETE")
    print("="*80)
    print()

    sys.exit(0 if success else 1)
