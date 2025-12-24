#!/usr/bin/env python3
"""
Parse MPEC observations from the provided format to CSV
"""

import csv
import math

def fractional_day_to_time(year, month, day_frac):
    """
    Convert fractional day to HH:MM:SS

    Args:
        year: Year (int)
        month: Month (int)
        day_frac: Day with fractional part (float)

    Returns:
        String in format "YYYY-MM-DD HH:MM:SS"
    """
    day = int(day_frac)
    frac = day_frac - day

    # Convert fraction to hours
    hours_frac = frac * 24
    hours = int(hours_frac)

    # Convert remainder to minutes
    minutes_frac = (hours_frac - hours) * 60
    minutes = int(minutes_frac)

    # Convert remainder to seconds
    seconds = (minutes_frac - minutes) * 60

    return f"{year:04d}-{month:02d}-{day:02d} {hours:02d}:{minutes:02d}:{seconds:05.2f}"

# Raw observation data
raw_data = """2025 12 20.006169	10 42 32.822	+07 23 50.46	13.3 R	C23 – Olmen	MPEC Y151
2025 12 20.013657	10 42 30.684	+07 24 00.90	13.4 R	C23 – Olmen	MPEC Y151
2025 12 20.063186	10 42 16.76	+07 25 11.6	13.3 G	Z92 – Almalex Observatory, Leeds	MPEC Y151
2025 12 20.073737	10 42 13.72	+07 25 26.4	12.9 G	Z92 – Almalex Observatory, Leeds	MPEC Y151
2025 12 20.083697	10 42 10.95	+07 25 41.1	13.0 G	Z92 – Almalex Observatory, Leeds	MPEC Y151
2025 12 20.367141	10 40 50.892	+07 32 23.86	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.367662	10 40 50.738	+07 32 24.58	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.368333	10 40 50.554	+07 32 25.51	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.368843	10 40 50.407	+07 32 26.66	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.369363	10 40 50.256	+07 32 27.06	14.7 V	W50 – Apex	MPEC Y151
2025 12 20.370035	10 40 50.083	+07 32 28.03	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.370556	10 40 49.925	+07 32 28.79	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.371065	10 40 49.769	+07 32 29.36	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.371736	10 40 49.591	+07 32 30.26	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.372257	10 40 49.445	+07 32 30.98	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.372766	10 40 49.294	+07 32 31.96	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.373437	10 40 49.106	+07 32 32.75	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.373958	10 40 48.958	+07 32 33.68	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.374468	10 40 48.823	+07 32 34.30	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.376956	10 40 48.058	+07 32 38.22	14.7 V	W50 – Apex	MPEC Y151
2025 12 20.377477	10 40 47.964	+07 32 38.76	14.7 V	W50 – Apex	MPEC Y151
2025 12 20.378009	10 40 47.808	+07 32 40.52	14.7 V	W50 – Apex	MPEC Y151
2025 12 20.380868	10 40 46.990	+07 32 43.48	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.381493	10 40 46.814	+07 32 44.16	14.7 V	W50 – Apex	MPEC Y151
2025 12 20.382118	10 40 46.649	+07 32 45.24	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.382986	10 40 46.390	+07 32 46.39	14.7 V	W50 – Apex	MPEC Y151
2025 12 20.383611	10 40 46.207	+07 32 47.15	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.384225	10 40 46.034	+07 32 48.23	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.386944	10 40 45.262	+07 32 52.08	14.7 V	W50 – Apex	MPEC Y151
2025 12 20.387870	10 40 45.012	+07 32 53.23	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.388495	10 40 44.834	+07 32 54.42	14.8 V	W50 – Apex	MPEC Y151
2025 12 20.391227	10 40 44.054	+07 32 58.09	14.8 V	W50 – Apex	MPEC Y151
2025 12 21.13398	10 37 13.66	+07 50 31.5	14.6 V	C82 – Osservatorio Astronomico Nastro Verde, Sorrento	MPEC Y151
2025 12 21.13526	10 37 13.29	+07 50 33.3	14.6 V	C82 – Osservatorio Astronomico Nastro Verde, Sorrento	MPEC Y151
2025 12 21.13675	10 37 12.86	+07 50 35.3	14.5 V	C82 – Osservatorio Astronomico Nastro Verde, Sorrento	MPEC Y151
2025 12 21.14059	10 37 11.77	+07 50 40.7	14.5 V	C82 – Osservatorio Astronomico Nastro Verde, Sorrento	MPEC Y151
2025 12 21.14573	10 37 10.30	+07 50 48.0	14.6 V	C82 – Osservatorio Astronomico Nastro Verde, Sorrento	MPEC Y151
2025 12 21.166319	10 37 04.411	+07 51 16.56	14.6 G	D68 – Osservatorio Galileo, Padova	MPEC Y151
2025 12 21.177789	10 37 01.133	+07 51 32.98	14.7 G	D68 – Osservatorio Galileo, Padova	MPEC Y151
2025 12 21.190405	10 36 57.506	+07 51 51.16	13.6 G	D68 – Osservatorio Galileo, Padova	MPEC Y151
2025 12 21.359965	10 36 09.602	+07 55 52.10	14.23 G	V21 – Cewanee Observatory at DSNM	MPEC Y151
2025 12 21.374606	10 36 05.405	+07 56 12.70	14.19 G	V21 – Cewanee Observatory at DSNM	MPEC Y151
2025 12 21.389201	10 36 01.238	+07 56 33.11	14.22 G	V21 – Cewanee Observatory at DSNM	MPEC Y151
2025 12 21.403808	10 35 57.070	+07 56 54.13	14.19 G	V21 – Cewanee Observatory at DSNM	MPEC Y151
2025 12 21.418391	10 35 52.906	+07 57 14.87	14.27 G	V21 – Cewanee Observatory at DSNM	MPEC Y151
2025 12 21.419004	10 35 52.969	+07 57 14.87	11.94 G	703 – Catalina Sky Survey	MPEC Y151
2025 12 21.421288	10 35 52.382	+07 57 17.93	11.65 G	703 – Catalina Sky Survey	MPEC Y151
2025 12 21.423573	10 35 51.688	+07 57 21.31	11.83 G	703 – Catalina Sky Survey	MPEC Y151
2025 12 21.425858	10 35 51.022	+07 57 24.59	11.86 G	703 – Catalina Sky Survey	MPEC Y151
2025 12 21.842882	10 33 51.758	+08 07 15.38	15.1 V	Q14 – Goto Astronomical Observatory in Yatsugatake	MPEC Y151
2025 12 21.849294	10 33 49.932	+08 07 24.46	15.0 V	Q14 – Goto Astronomical Observatory in Yatsugatake	MPEC Y151
2025 12 21.969664	10 33 15.839	+08 10 13.08	14.9 G	B72 – Soerth Observatory	MPEC Y151
2025 12 22.027454	10 32 59.312	+08 11 35.24	15.0 G	B72 – Soerth Observatory	MPEC Y151
2025 12 22.049549	10 32 52.980	+08 12 06.53	15.0 G	B72 – Soerth Observatory	MPEC Y151
2025 12 22.060336	10 32 49.889	+08 12 21.84	15.0 G	B72 – Soerth Observatory	MPEC Y151
2025 12 22.072396	10 32 46.430	+08 12 38.87	15.0 G	B72 – Soerth Observatory	MPEC Y151
2025 12 22.40929	10 31 10.10	+08 20 36.1	 	U94 – iTelescope Observatory, Beryl Junction	MPEC Y151
2025 12 22.41362	10 31 08.90	+08 20 41.9	13.4 G	U94 – iTelescope Observatory, Beryl Junction	MPEC Y151
2025 12 22.41794	10 31 07.64	+08 20 47.9	13.6 G	U94 – iTelescope Observatory, Beryl Junction	MPEC Y151
2025 12 22.42228	10 31 06.38	+08 20 53.9	13.2 G	U94 – iTelescope Observatory, Beryl Junction	MPEC Y151
2025 12 22.697488	10 29 47.599	+08 27 22.23	14.7 G	Q21 – Southern Utsunomiya	MPEC Y151
2025 12 22.701007	10 29 46.577	+08 27 27.06	14.8 G	Q21 – Southern Utsunomiya	MPEC Y151
2025 12 22.704525	10 29 45.573	+08 27 32.02	15.0 G	Q21 – Southern Utsunomiya	MPEC Y151
2025 12 22.708032	10 29 44.566	+08 27 37.21	15.1 G	Q21 – Southern Utsunomiya	MPEC Y151
2025 12 22.903553	10 28 48.571	+08 32 13.56	13.7 V	M73 – Eden Emirates Observatory, Abu Dhabi	MPEC Y151
2025 12 22.908704	10 28 47.066	+08 32 21.12	13.6 V	M73 – Eden Emirates Observatory, Abu Dhabi	MPEC Y151
2025 12 22.914132	10 28 45.514	+08 32 28.57	13.6 V	M73 – Eden Emirates Observatory, Abu Dhabi	MPEC Y151
2025 12 22.919028	10 28 44.105	+08 32 35.63	13.6 V	M73 – Eden Emirates Observatory, Abu Dhabi	MPEC Y151
2025 12 22.923958	10 28 42.679	+08 32 42.54	13.5 V	M73 – Eden Emirates Observatory, Abu Dhabi	MPEC Y151
2025 12 23.100091	10 27 52.140	+08 36 50.11	13.75 w	R17 – ATLAS-TDO	MPEC Y151
2025 12 23.114246	10 27 48.055	+08 37 09.95	13.65 w	R17 – ATLAS-TDO	MPEC Y151
2025 12 23.128398	10 27 43.975	+08 37 29.93	13.58 w	R17 – ATLAS-TDO	MPEC Y151
2025 12 23.142545	10 27 39.893	+08 37 49.98	13.62 w	R17 – ATLAS-TDO	MPEC Y151"""

observations = []

for line in raw_data.strip().split('\n'):
    # Split by tab
    parts = line.split('\t')

    if len(parts) < 6:
        continue

    # Parse date
    date_parts = parts[0].split()
    year = int(date_parts[0])
    month = int(date_parts[1])
    day_frac = float(date_parts[2])

    timestamp = fractional_day_to_time(year, month, day_frac)

    # Parse RA (already in HH MM SS.SSS format)
    obs_ra = parts[1].strip()

    # Parse Dec (already in ±DD MM SS.SS format)
    obs_dec = parts[2].strip()

    # Parse observatory code (from the observatory field)
    obs_field = parts[4].strip()
    observatory = obs_field.split()[0]  # Get first part (the code)

    observations.append({
        'timestamp': timestamp,
        'observatory': observatory,
        'obs_ra': obs_ra,
        'obs_dec': obs_dec
    })

# Write to CSV
output_file = 'observations_20251220-23.csv'

with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['timestamp', 'observatory', 'obs_ra', 'obs_dec'])
    writer.writeheader()
    writer.writerows(observations)

print(f"✓ Parsed {len(observations)} observations")
print(f"✓ Saved to: {output_file}")
print()
print("Observatory breakdown:")

# Count by observatory
obs_counts = {}
for obs in observations:
    code = obs['observatory']
    obs_counts[code] = obs_counts.get(code, 0) + 1

for code, count in sorted(obs_counts.items()):
    print(f"  {code}: {count} observations")

print()
print("Date range:")
print(f"  First: {observations[0]['timestamp']}")
print(f"  Last:  {observations[-1]['timestamp']}")
print()
print("Next step:")
print(f"  ./generate_solution44_table.py {output_file}")
