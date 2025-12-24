# Prompt for Gemini/ChatGPT to Run Solution 44 Analysis

Copy and paste this entire prompt into Gemini or ChatGPT (or any AI with code execution + internet access):

---

# Task: Generate JPL Solution 44 Comparison Table for C/2025 N1 (ATLAS)

I need you to query JPL Horizons and generate a comparison table showing how well Solution 44 predicted actual observations of comet C/2025 N1 (ATLAS) from December 20-23, 2025.

## Step 1: Install Requirements

```python
import subprocess
subprocess.run(["pip", "install", "requests"], check=True)
```

## Step 2: Load Observation Data

Here are 73 observations from MPEC Y151:

```python
observations_csv = """timestamp,observatory,obs_ra,obs_dec
2025-12-20 00:08:53.00,C23,10 42 32.822,+07 23 50.46
2025-12-20 00:19:39.96,C23,10 42 30.684,+07 24 00.90
2025-12-20 01:30:59.27,Z92,10 42 16.76,+07 25 11.6
2025-12-20 01:46:10.88,Z92,10 42 13.72,+07 25 26.4
2025-12-20 02:00:31.42,Z92,10 42 10.95,+07 25 41.1
2025-12-20 08:48:40.98,W50,10 40 50.892,+07 32 23.86
2025-12-20 08:49:26.00,W50,10 40 50.738,+07 32 24.58
2025-12-20 08:50:23.97,W50,10 40 50.554,+07 32 25.51
2025-12-20 08:51:08.04,W50,10 40 50.407,+07 32 26.66
2025-12-20 08:51:52.96,W50,10 40 50.256,+07 32 27.06
2025-12-20 08:52:51.02,W50,10 40 50.083,+07 32 28.03
2025-12-20 08:53:36.04,W50,10 40 49.925,+07 32 28.79
2025-12-20 08:54:20.02,W50,10 40 49.769,+07 32 29.36
2025-12-20 08:55:17.99,W50,10 40 49.591,+07 32 30.26
2025-12-20 08:56:03.00,W50,10 40 49.445,+07 32 30.98
2025-12-20 08:56:46.98,W50,10 40 49.294,+07 32 31.96
2025-12-20 08:57:44.96,W50,10 40 49.106,+07 32 32.75
2025-12-20 08:58:29.97,W50,10 40 48.958,+07 32 33.68
2025-12-20 08:59:14.04,W50,10 40 48.823,+07 32 34.30
2025-12-20 09:02:49.00,W50,10 40 48.058,+07 32 38.22
2025-12-20 09:03:34.01,W50,10 40 47.964,+07 32 38.76
2025-12-20 09:04:19.98,W50,10 40 47.808,+07 32 40.52
2025-12-20 09:08:27.00,W50,10 40 46.990,+07 32 43.48
2025-12-20 09:09:21.00,W50,10 40 46.814,+07 32 44.16
2025-12-20 09:10:15.00,W50,10 40 46.649,+07 32 45.24
2025-12-20 09:11:29.99,W50,10 40 46.390,+07 32 46.39
2025-12-20 09:12:23.99,W50,10 40 46.207,+07 32 47.15
2025-12-20 09:13:17.04,W50,10 40 46.034,+07 32 48.23
2025-12-20 09:17:11.96,W50,10 40 45.262,+07 32 52.08
2025-12-20 09:18:31.97,W50,10 40 45.012,+07 32 53.23
2025-12-20 09:19:25.97,W50,10 40 44.834,+07 32 54.42
2025-12-20 09:23:22.01,W50,10 40 44.054,+07 32 58.09
2025-12-21 03:12:55.87,C82,10 37 13.66,+07 50 31.5
2025-12-21 03:14:46.46,C82,10 37 13.29,+07 50 33.3
2025-12-21 03:16:55.20,C82,10 37 12.86,+07 50 35.3
2025-12-21 03:22:26.98,C82,10 37 11.77,+07 50 40.7
2025-12-21 03:29:51.07,C82,10 37 10.30,+07 50 48.0
2025-12-21 03:59:29.96,D68,10 37 04.411,+07 51 16.56
2025-12-21 04:16:00.97,D68,10 37 01.133,+07 51 32.98
2025-12-21 04:34:10.99,D68,10 36 57.506,+07 51 51.16
2025-12-21 08:38:20.98,V21,10 36 09.602,+07 55 52.10
2025-12-21 08:59:25.96,V21,10 36 05.405,+07 56 12.70
2025-12-21 09:20:26.97,V21,10 36 01.238,+07 56 33.11
2025-12-21 09:41:29.01,V21,10 35 57.070,+07 56 54.13
2025-12-21 10:02:28.98,V21,10 35 52.906,+07 57 14.87
2025-12-21 10:03:21.63,703,10 35 52.969,+07 57 14.87
2025-12-21 10:06:13.95,703,10 35 52.382,+07 57 17.93
2025-12-21 10:09:06.70,703,10 35 51.688,+07 57 21.31
2025-12-21 10:11:59.71,703,10 35 51.022,+07 57 24.59
2025-12-21 20:13:45.00,Q14,10 33 51.758,+08 07 15.38
2025-12-21 20:22:36.98,Q14,10 33 49.932,+08 07 24.46
2025-12-21 23:16:20.98,B72,10 33 15.839,+08 10 13.08
2025-12-22 00:39:32.03,B72,10 32 59.312,+08 11 35.24
2025-12-22 01:11:10.23,B72,10 32 52.980,+08 12 06.53
2025-12-22 01:26:44.98,B72,10 32 49.889,+08 12 21.84
2025-12-22 01:44:05.02,B72,10 32 46.430,+08 12 38.87
2025-12-22 09:49:23.38,U94,10 31 10.10,+08 20 36.1
2025-12-22 09:55:40.42,U94,10 31 08.90,+08 20 41.9
2025-12-22 10:01:56.42,U94,10 31 07.64,+08 20 47.9
2025-12-22 10:08:14.43,U94,10 31 06.38,+08 20 53.9
2025-12-22 16:44:23.74,Q21,10 29 47.599,+08 27 22.23
2025-12-22 16:50:27.00,Q21,10 29 46.577,+08 27 27.06
2025-12-22 16:56:30.26,Q21,10 29 45.573,+08 27 32.02
2025-12-22 17:02:31.96,Q21,10 29 44.566,+08 27 37.21
2025-12-22 21:41:06.98,M73,10 28 48.571,+08 32 13.56
2025-12-22 21:47:20.03,M73,10 28 47.066,+08 32 21.12
2025-12-22 21:53:57.00,M73,10 28 45.514,+08 32 28.57
2025-12-22 22:00:17.03,M73,10 28 44.105,+08 32 35.63
2025-12-22 22:06:30.03,M73,10 28 42.679,+08 32 42.54
2025-12-23 02:24:07.86,R17,10 27 52.140,+08 36 50.11
2025-12-23 02:44:31.06,R17,10 27 48.055,+08 37 09.95
2025-12-23 03:04:54.02,R17,10 27 43.975,+08 37 29.93
2025-12-23 03:25:15.89,R17,10 27 39.893,+08 37 49.98"""

# Save to file
with open('observations.csv', 'w') as f:
    f.write(observations_csv)

print("✓ Loaded 73 observations")
```

## Step 3: Run the Analysis

Execute this complete script:

```python
import requests
import csv
import math
import time
from datetime import datetime

def query_horizons(timestamp, observatory):
    """Query JPL Horizons for Solution 44 prediction"""
    base_url = "https://ssd.jpl.nasa.gov/api/horizons.api"

    if not observatory.startswith('@'):
        observatory = f'@{observatory}'

    params = {
        'format': 'text',
        'COMMAND': "'1004083;'",
        'OBJ_DATA': "'YES'",
        'MAKE_EPHEM': "'YES'",
        'EPHEM_TYPE': "'OBSERVER'",
        'CENTER': f"'{observatory}'",
        'TLIST': f"'{timestamp}'",
        'QUANTITIES': "'1,3,36,37'",
        'TIME_DIGITS': "'SECONDS'",
        'EXTRA_PREC': "'YES'",
        'CSV_FORMAT': "'NO'"
    }

    try:
        response = requests.get(base_url, params=params, timeout=30)
        if response.status_code != 200:
            return {'error': f'HTTP {response.status_code}'}

        lines = response.text.split('\n')
        in_ephemeris = False

        for line in lines:
            if '$$SOE' in line:
                in_ephemeris = True
                continue
            elif '$$EOE' in line:
                break
            elif in_ephemeris and line.strip():
                parts = line.split()
                if len(parts) >= 10:
                    try:
                        calc_ra = f"{parts[2]} {parts[3]} {parts[4]}"
                        calc_dec = f"{parts[5]} {parts[6]} {parts[7]}"

                        pos_3sigma = None
                        for part in parts[8:]:
                            try:
                                val = float(part)
                                if 0.001 < val < 1000:
                                    pos_3sigma = val
                                    break
                            except:
                                continue

                        return {
                            'calc_ra': calc_ra,
                            'calc_dec': calc_dec,
                            'pos_3sigma': pos_3sigma
                        }
                    except Exception as e:
                        return {'error': f'Parse error: {e}'}

        return {'error': 'No ephemeris data found'}

    except Exception as e:
        return {'error': str(e)}

def hms_to_degrees(hms_str):
    """Convert HH MM SS to degrees"""
    parts = hms_str.split()
    h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
    return (h + m/60.0 + s/3600.0) * 15.0

def dms_to_degrees(dms_str):
    """Convert ±DD MM SS to degrees"""
    parts = dms_str.split()
    sign = 1 if parts[0][0] != '-' else -1
    d = abs(float(parts[0]))
    m = float(parts[1])
    s = float(parts[2])
    return sign * (d + m/60.0 + s/3600.0)

def calculate_residuals(obs_ra, obs_dec, calc_ra, calc_dec):
    """Calculate O-C residuals in arcseconds"""
    obs_ra_deg = hms_to_degrees(obs_ra)
    obs_dec_deg = dms_to_degrees(obs_dec)
    calc_ra_deg = hms_to_degrees(calc_ra)
    calc_dec_deg = dms_to_degrees(calc_dec)

    dec_avg_rad = math.radians((obs_dec_deg + calc_dec_deg) / 2.0)
    ra_res = (obs_ra_deg - calc_ra_deg) * 3600.0 * math.cos(dec_avg_rad)
    dec_res = (obs_dec_deg - calc_dec_deg) * 3600.0
    total = math.sqrt(ra_res**2 + dec_res**2)

    return ra_res, dec_res, total

# Read observations
observations = []
with open('observations.csv', 'r') as f:
    reader = csv.DictReader(f)
    observations = list(reader)

print(f"Processing {len(observations)} observations...")
print()

results = []
for i, obs in enumerate(observations, 1):
    print(f"[{i}/{len(observations)}] {obs['timestamp']} @ {obs['observatory']}...", end=' ')

    result = query_horizons(obs['timestamp'], obs['observatory'])

    if 'error' not in result:
        # Calculate residuals
        try:
            ra_res, dec_res, total = calculate_residuals(
                obs['obs_ra'], obs['obs_dec'],
                result['calc_ra'], result['calc_dec']
            )
            result['ra_res'] = ra_res
            result['dec_res'] = dec_res
            result['total_res'] = total

            if result['pos_3sigma']:
                result['sigma_ratio'] = total / result['pos_3sigma']

            print(f"✓ Total: {total:.1f}\" 3σ: {result['pos_3sigma']:.3f}\" Ratio: {result.get('sigma_ratio', 0):.0f}×")
        except Exception as e:
            result['error'] = f'Calc error: {e}'
            print(f"ERROR: {e}")
    else:
        print(f"ERROR: {result['error']}")

    results.append(result)

    # Be nice to JPL servers
    time.sleep(0.5)

print()
print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print()

# Generate summary
successful = [r for r in results if 'error' not in r and 'total_res' in r]
failed = [r for r in results if 'error' in r]

print(f"Successfully analyzed: {len(successful)}/{len(observations)}")
print(f"Failed queries: {len(failed)}")
print()

if successful:
    total_residuals = [r['total_res'] for r in successful]
    sigma_ratios = [r['sigma_ratio'] for r in successful if 'sigma_ratio' in r]

    print("RESIDUAL STATISTICS:")
    print(f"  Min: {min(total_residuals):.2f} arcsec")
    print(f"  Max: {max(total_residuals):.2f} arcsec")
    print(f"  Mean: {sum(total_residuals)/len(total_residuals):.2f} arcsec")
    print(f"  Median: {sorted(total_residuals)[len(total_residuals)//2]:.2f} arcsec")
    print()

    if sigma_ratios:
        print("SIGMA RATIO STATISTICS:")
        print(f"  Min: {min(sigma_ratios):.1f}×")
        print(f"  Max: {max(sigma_ratios):.1f}×")
        print(f"  Mean: {sum(sigma_ratios)/len(sigma_ratios):.1f}×")
        print()

        within_3sigma = sum(1 for r in sigma_ratios if r <= 1.0)
        beyond_3sigma = sum(1 for r in sigma_ratios if r > 1.0)
        catastrophic = sum(1 for r in sigma_ratios if r > 100.0)

        print("PREDICTION QUALITY:")
        print(f"  Within 3σ (good): {within_3sigma}/{len(sigma_ratios)} ({100*within_3sigma/len(sigma_ratios):.1f}%)")
        print(f"  Beyond 3σ (failed): {beyond_3sigma}/{len(sigma_ratios)} ({100*beyond_3sigma/len(sigma_ratios):.1f}%)")
        print(f"  Catastrophic (>100×): {catastrophic}/{len(sigma_ratios)} ({100*catastrophic/len(sigma_ratios):.1f}%)")
        print()

        print("VERDICT:")
        if within_3sigma / len(sigma_ratios) > 0.9:
            print("  ✓ Solution 44 SUCCESSFULLY predicted these observations")
            print("  ✓ The orbital model was working correctly")
        elif catastrophic / len(sigma_ratios) > 0.5:
            print("  ✗ Solution 44 CATASTROPHICALLY FAILED to predict these observations")
            print("  ✗ The claimed 'convergence' on Dec 17 was illusory")
        else:
            print("  ⚠ Solution 44 showed MIXED performance")
            print("  ⚠ Some predictions good, others failed")

# Show detailed table for first 10 and last 10 observations
print()
print("="*80)
print("DETAILED RESULTS (first 10 and last 10 observations)")
print("="*80)
print()

for idx in list(range(min(10, len(observations)))) + list(range(max(10, len(observations)-10), len(observations))):
    if idx == 10 and len(observations) > 20:
        print(f"... [{len(observations)-20} observations omitted] ...")
        print()
        continue

    obs = observations[idx]
    result = results[idx]

    print(f"[{idx+1}] {obs['timestamp']} @ {obs['observatory']}")
    print(f"    Observed:   RA={obs['obs_ra']:20s} Dec={obs['obs_dec']}")

    if 'error' in result:
        print(f"    ✗ ERROR: {result['error']}")
    else:
        print(f"    Calculated: RA={result.get('calc_ra', 'N/A'):20s} Dec={result.get('calc_dec', 'N/A')}")
        if 'total_res' in result:
            status = "✓" if result.get('sigma_ratio', 999) <= 1.0 else "✗"
            print(f"    {status} Residual: {result['total_res']:.2f}\" (ΔRA={result['ra_res']:+.2f}\" ΔDec={result['dec_res']:+.2f}\")")
            print(f"    3σ: {result.get('pos_3sigma', 'N/A'):.3f}\" | Ratio: {result.get('sigma_ratio', 'N/A'):.1f}×")
    print()
```

## What to Report Back

Please provide:

1. **Summary Statistics**: Min/Max/Mean residuals and sigma ratios
2. **Prediction Quality**: Percentage within 3σ, beyond 3σ, and catastrophic failures
3. **Verdict**: Did Solution 44 succeed or fail?
4. **Pattern Analysis**:
   - Do residuals increase over time (Dec 20 → Dec 23)?
   - Are certain observatories worse than others?
   - Is there a systematic bias (all positive or all negative)?

## Expected Results

Based on claims, if Solution 44 failed:
- Residuals should be **~17,000 arcsec** (4.7°)
- Sigma ratios should be **~50,000×**
- Nearly **100% catastrophic failures**

If Solution 44 worked:
- Residuals should be **<1 arcsec**
- Sigma ratios should be **<1.0×**
- Nearly **100% within 3σ**

## Important Notes

- The script queries JPL's live Horizons system
- It includes 0.5s delays between queries (be nice to their servers)
- Expected runtime: 2-3 minutes for 73 queries
- If you get errors, try reducing the observation count first to test

---

**After running this, please share the complete output, especially the summary statistics and verdict!**
