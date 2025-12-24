#!/usr/bin/env python3
"""
Manual Data Entry Version - C/2025 N1 (ATLAS) Residuals Analysis

Use this script when you have manually obtained the JPL Horizons data
and want to calculate the O-C residuals.

Instructions:
1. Query JPL Horizons using the parameters in comet_analysis_manual.md
2. Extract the calculated RA, Dec, and POS_3sigma values
3. Enter them below in the CALCULATED DATA section
4. Run this script: python3 comet_residuals_manual_entry.py
"""

import math

# =============================================================================
# OBSERVED DATA (from December 19, 2025 MPEC)
# =============================================================================
OBS_RA_HMS = "11 05 53.640"  # 11h 05m 53.640s
OBS_DEC_DMS = "+05 24 55.44"  # +05° 24' 55.44"
OBS_TIME = "2025-12-19 01:21:40 UT"
OBSERVER = "G96 (Mt. Lemmon Survey)"

# =============================================================================
# CALCULATED DATA (from JPL Horizons Solution 44)
# Enter the values you obtained from the Horizons query below
# =============================================================================

# Option 1: Enter in HMS/DMS format (easier to copy from Horizons)
CALC_RA_HMS = "XX XX XX.XXX"  # Format: "HH MM SS.SSS"
CALC_DEC_DMS = "+XX XX XX.XX"  # Format: "+DD MM SS.SS"

# Option 2: Or enter directly in decimal degrees (comment out Option 1 if using this)
# CALC_RA_DEG = None   # decimal degrees
# CALC_DEC_DEG = None  # decimal degrees

# 3-sigma positional uncertainty from Horizons (arcseconds)
POS_3SIGMA = None  # arcseconds (e.g., 0.31)

# =============================================================================
# CALCULATION FUNCTIONS
# =============================================================================

def hms_to_degrees(hms_str):
    """
    Convert RA from HH MM SS.SSS format to decimal degrees

    Args:
        hms_str: String in format "HH MM SS.SSS"

    Returns:
        RA in decimal degrees
    """
    parts = hms_str.split()
    if len(parts) != 3:
        raise ValueError(f"Invalid HMS format: {hms_str}")

    h = float(parts[0])
    m = float(parts[1])
    s = float(parts[2])

    # Convert to degrees (15 degrees per hour)
    degrees = (h + m/60.0 + s/3600.0) * 15.0
    return degrees

def dms_to_degrees(dms_str):
    """
    Convert Dec from ±DD MM SS.SS format to decimal degrees

    Args:
        dms_str: String in format "±DD MM SS.SS"

    Returns:
        Dec in decimal degrees
    """
    parts = dms_str.split()
    if len(parts) != 3:
        raise ValueError(f"Invalid DMS format: {dms_str}")

    sign = 1 if parts[0][0] != '-' else -1
    d = abs(float(parts[0]))
    m = float(parts[1])
    s = float(parts[2])

    degrees = sign * (d + m/60.0 + s/3600.0)
    return degrees

def degrees_to_hms(degrees):
    """
    Convert decimal degrees to HH:MM:SS.SSS format

    Args:
        degrees: RA in decimal degrees

    Returns:
        String in format "HH:MM:SS.SSS"
    """
    hours = degrees / 15.0
    h = int(hours)
    m_frac = (hours - h) * 60.0
    m = int(m_frac)
    s = (m_frac - m) * 60.0

    return f"{h:02d}:{m:02d}:{s:06.3f}"

def degrees_to_dms(degrees):
    """
    Convert decimal degrees to ±DD:MM:SS.SS format

    Args:
        degrees: Dec in decimal degrees

    Returns:
        String in format "±DD:MM:SS.SS"
    """
    sign = '+' if degrees >= 0 else '-'
    abs_deg = abs(degrees)

    d = int(abs_deg)
    m_frac = (abs_deg - d) * 60.0
    m = int(m_frac)
    s = (m_frac - m) * 60.0

    return f"{sign}{d:02d}:{m:02d}:{s:05.2f}"

def calculate_residuals(obs_ra_deg, obs_dec_deg, calc_ra_deg, calc_dec_deg):
    """
    Calculate O-C residuals in arcseconds

    Args:
        obs_ra_deg: Observed RA in decimal degrees
        obs_dec_deg: Observed Dec in decimal degrees
        calc_ra_deg: Calculated RA in decimal degrees
        calc_dec_deg: Calculated Dec in decimal degrees

    Returns:
        Tuple of (ra_residual_arcsec, dec_residual_arcsec, total_separation_arcsec)
    """
    # RA difference in degrees
    ra_diff_deg = obs_ra_deg - calc_ra_deg

    # Apply cos(dec) correction using average declination
    dec_avg_rad = math.radians((obs_dec_deg + calc_dec_deg) / 2.0)
    ra_residual_arcsec = ra_diff_deg * 3600.0 * math.cos(dec_avg_rad)

    # Dec difference in arcseconds
    dec_diff_deg = obs_dec_deg - calc_dec_deg
    dec_residual_arcsec = dec_diff_deg * 3600.0

    # Total angular separation (Pythagorean theorem)
    total_separation_arcsec = math.sqrt(ra_residual_arcsec**2 + dec_residual_arcsec**2)

    return ra_residual_arcsec, dec_residual_arcsec, total_separation_arcsec

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    print("="*80)
    print("COMET C/2025 N1 (ATLAS) - SOLUTION 44 RESIDUALS ANALYSIS")
    print("Manual Data Entry Version")
    print("="*80)
    print()

    # Parse observed position
    print("OBSERVED POSITION (from December 19, 2025 MPEC):")
    print(f"Time:     {OBS_TIME}")
    print(f"Observer: {OBSERVER}")
    print(f"RA:       {OBS_RA_HMS}")
    print(f"Dec:      {OBS_DEC_DMS}")

    obs_ra_deg = hms_to_degrees(OBS_RA_HMS)
    obs_dec_deg = dms_to_degrees(OBS_DEC_DMS)

    print(f"\nConverted to decimal:")
    print(f"RA  = {obs_ra_deg:.8f}°")
    print(f"Dec = {obs_dec_deg:.8f}°")
    print()

    # Check if calculated data has been entered
    if CALC_RA_HMS == "XX XX XX.XXX" or CALC_DEC_DMS == "+XX XX XX.XX":
        print("="*80)
        print("⚠️  CALCULATED DATA NOT YET ENTERED")
        print("="*80)
        print()
        print("Please follow these steps:")
        print()
        print("1. Query JPL Horizons System:")
        print("   URL: https://ssd.jpl.nasa.gov/horizons/app.html")
        print("   Target: C/2025 N1  or  1004083")
        print("   Observer: G96")
        print("   Time: 2025-12-19 01:21:40")
        print("   Quantities: 1,3,36,37")
        print("   Options: EXTRA_PREC=YES, TIME_DIGITS=SECONDS")
        print()
        print("2. Extract from the ephemeris table:")
        print("   - Calculated RA (HH MM SS.SSS)")
        print("   - Calculated Dec (±DD MM SS.SS)")
        print("   - POS_3sigma value (arcseconds)")
        print()
        print("3. Edit this file (comet_residuals_manual_entry.py):")
        print("   - Update CALC_RA_HMS")
        print("   - Update CALC_DEC_DMS")
        print("   - Update POS_3SIGMA")
        print()
        print("4. Run this script again")
        print()
        print("="*80)
        return

    # Parse calculated position
    print("CALCULATED POSITION (from JPL Horizons Solution 44):")
    print(f"RA:  {CALC_RA_HMS}")
    print(f"Dec: {CALC_DEC_DMS}")

    calc_ra_deg = hms_to_degrees(CALC_RA_HMS)
    calc_dec_deg = dms_to_degrees(CALC_DEC_DMS)

    print(f"\nConverted to decimal:")
    print(f"RA  = {calc_ra_deg:.8f}°")
    print(f"Dec = {calc_dec_deg:.8f}°")
    print()

    # Calculate residuals
    ra_res, dec_res, total_sep = calculate_residuals(
        obs_ra_deg, obs_dec_deg, calc_ra_deg, calc_dec_deg
    )

    print("="*80)
    print("RESIDUALS (Observed minus Calculated)")
    print("="*80)
    print()
    print(f"ΔRA  = {ra_res:+12.3f} arcsec  (with cos(dec) correction)")
    print(f"ΔDec = {dec_res:+12.3f} arcsec")
    print()
    print(f"Total angular separation = {total_sep:12.3f} arcsec")
    print(f"                         = {total_sep/60.0:12.3f} arcmin")
    print(f"                         = {total_sep/3600.0:12.6f}°")
    print()

    # Compare to 3-sigma
    if POS_3SIGMA is not None and POS_3SIGMA > 0:
        print("="*80)
        print("SIGNIFICANCE ANALYSIS")
        print("="*80)
        print()
        print(f"JPL 3-sigma uncertainty (POS_3sigma): {POS_3SIGMA:.3f} arcsec")
        print()

        sigma_ratio = total_sep / POS_3SIGMA
        print(f"Ratio (Total / 3-sigma): {sigma_ratio:.2f}×")
        print()

        if total_sep <= POS_3SIGMA:
            print("✓ VERDICT: WITHIN PREDICTED UNCERTAINTY")
            print()
            print(f"   The observed position is {sigma_ratio:.2f}× the 3-sigma margin,")
            print("   which is within the predicted error bounds.")
            print("   Solution 44 successfully predicted the comet's position.")
        else:
            print("⚠️  VERDICT: OUTSIDE PREDICTED UNCERTAINTY")
            print()
            print(f"   The observed position is {sigma_ratio:.2f}× the 3-sigma margin,")
            print("   which is BEYOND the predicted error bounds.")
            print()

            # Interpret the significance level
            if sigma_ratio < 3:
                conf = "~68-95%"
                severity = "moderate"
            elif sigma_ratio < 10:
                conf = "~99.7%"
                severity = "significant"
            elif sigma_ratio < 100:
                conf = ">99.99%"
                severity = "severe"
            else:
                conf = "overwhelmingly high"
                severity = "catastrophic"

            print(f"   Statistical confidence: {conf}")
            print(f"   Failure severity: {severity}")
            print()
            print("   This indicates Solution 44 failed to predict the comet's")
            print("   position within its stated uncertainty bounds.")

            # Physical interpretation
            distance_km = total_sep * 149597870.7 * 1000 / 206265  # Approximate at 1 AU
            print()
            print(f"   At ~1 AU distance, this residual corresponds to:")
            print(f"   ~{distance_km:,.0f} km positional error")

        print()
        print("="*80)
    else:
        print("Note: POS_3SIGMA not provided - cannot assess significance")
        print("      Please update POS_3SIGMA in the script")

    # Save results
    output_file = "residuals_analysis_results.txt"
    with open(output_file, 'w') as f:
        f.write("C/2025 N1 (ATLAS) - Solution 44 Residuals Analysis\n")
        f.write("="*80 + "\n\n")
        f.write(f"Analysis Date: {OBS_TIME}\n")
        f.write(f"Observer: {OBSERVER}\n\n")
        f.write("OBSERVED:\n")
        f.write(f"  RA  = {obs_ra_deg:.8f}° = {OBS_RA_HMS}\n")
        f.write(f"  Dec = {obs_dec_deg:.8f}° = {OBS_DEC_DMS}\n\n")
        f.write("CALCULATED (Solution 44):\n")
        f.write(f"  RA  = {calc_ra_deg:.8f}° = {CALC_RA_HMS}\n")
        f.write(f"  Dec = {calc_dec_deg:.8f}° = {CALC_DEC_DMS}\n\n")
        f.write("RESIDUALS (O-C):\n")
        f.write(f"  ΔRA  = {ra_res:+.3f} arcsec\n")
        f.write(f"  ΔDec = {dec_res:+.3f} arcsec\n")
        f.write(f"  Total = {total_sep:.3f} arcsec = {total_sep/3600.0:.6f}°\n\n")
        if POS_3SIGMA:
            f.write(f"3-SIGMA: {POS_3SIGMA:.3f} arcsec\n")
            f.write(f"RATIO: {sigma_ratio:.2f}×\n\n")
            f.write(f"VERDICT: {'WITHIN' if total_sep <= POS_3SIGMA else 'OUTSIDE'} predicted uncertainty\n")

    print(f"\nResults saved to: {output_file}")
    print()

if __name__ == "__main__":
    main()
