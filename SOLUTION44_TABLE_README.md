# Generate JPL Solution 44 Comparison Table

This toolkit generates an HTML comparison table showing observed positions vs JPL Solution 44 predictions for C/2025 N1 (ATLAS) at multiple timestamps and observatories.

## Quick Start

### Method 1: From observations HTML file

If you have the observations HTML file (e.g., from https://l-87hjl.github.io/Medium/observations_20251220-23.html):

```bash
# Step 1: Download the HTML file (or you may already have it)
# If downloading: save it as observations_20251220-23.html

# Step 2: Parse it to extract observations
python3 parse_observations_html.py observations_20251220-23.html

# This creates: observations.csv

# Step 3: Generate the comparison table
python3 generate_solution44_table.py observations.csv

# This creates: solution44_comparison_table.html
```

### Method 2: Create CSV manually

If you know the observations:

```bash
# Step 1: Create observations.csv with this format:
# timestamp,observatory,obs_ra,obs_dec
# 2025-12-19 01:21:40,G96,11 05 53.640,+05 24 55.44
# 2025-12-20 02:30:15,703,11 06 12.345,+05 25 10.20

# Use the template:
cp observations_template.csv my_observations.csv
# Edit my_observations.csv with your data

# Step 2: Generate the table
python3 generate_solution44_table.py my_observations.csv
```

### Method 3: Test with template data

Try it with the example data:

```bash
python3 generate_solution44_table.py observations_template.csv
```

## Files Included

| File | Purpose |
|------|---------|
| `generate_solution44_table.py` | Main script - queries JPL and generates HTML table |
| `parse_observations_html.py` | Extracts observations from HTML files |
| `observations_template.csv` | Example CSV file showing format |
| `SOLUTION44_TABLE_README.md` | This file - usage instructions |

## CSV Format

The observations CSV must have these columns:

```csv
timestamp,observatory,obs_ra,obs_dec
```

**Column Descriptions:**

- **timestamp**: UT time in format `YYYY-MM-DD HH:MM:SS`
  - Example: `2025-12-19 01:21:40`

- **observatory**: MPC observatory code (3-4 characters)
  - Example: `G96` (Mt. Lemmon), `703` (Catalina), `568` (Mauna Kea)

- **obs_ra**: Observed Right Ascension in `HH MM SS.SSS` format
  - Example: `11 05 53.640`

- **obs_dec**: Observed Declination in `±DD MM SS.SS` format
  - Example: `+05 24 55.44` or `-12 30 45.12`

## Output HTML Table

The generated HTML table includes:

### Columns

1. **Timestamp**: Observation time (UT)
2. **Obs**: Observatory code
3. **Observed RA/Dec**: The actual observation
4. **Calculated RA/Dec**: What Solution 44 predicted
5. **Residuals**: O-C differences in arcseconds
   - ΔRA (with cos(dec) correction)
   - ΔDec
   - Total (Pythagorean sum)
6. **3σ**: Solution 44's 3-sigma uncertainty
7. **σ ratio**: How many sigmas off (Total / 3σ)

### Color Coding

- **Green**: Within 3-sigma (good prediction)
- **Orange**: 1-3× beyond 3-sigma (marginal)
- **Red**: >3× beyond 3-sigma (prediction failure)

## How It Works

1. **Reads observations** from CSV file
2. **Queries JPL Horizons** for each timestamp/observatory combination
3. **Extracts calculated positions** from Horizons response
4. **Calculates residuals** (O-C) with proper cos(dec) correction
5. **Assesses significance** by comparing to 3-sigma uncertainty
6. **Generates HTML table** with color-coded results

## Example Workflow

Let's say you want to check observations from December 20-23, 2025:

```bash
# 1. You have observations in a file
cat > my_obs.csv << 'EOF'
timestamp,observatory,obs_ra,obs_dec
2025-12-20 01:30:00,G96,11 06 10.123,+05 25 08.45
2025-12-21 02:15:00,703,11 07 40.567,+05 27 30.12
2025-12-22 03:00:00,568,11 09 05.890,+05 30 15.67
2025-12-23 01:45:00,G96,11 10 30.234,+05 32 45.23
EOF

# 2. Generate the table
python3 generate_solution44_table.py my_obs.csv

# 3. Open the result
# solution44_comparison_table.html
```

## Requirements

- Python 3.6+
- `requests` library (for querying JPL Horizons)
- Internet access (to query JPL Horizons API)

Install requirements:
```bash
pip install requests
```

## Troubleshooting

### "No ephemeris data found"

**Cause**: The timestamp might be outside Solution 44's valid range, or JPL might be using a different solution now.

**Solution**:
- Verify the timestamp is correct
- Check that Solution 44 is still active (JPL updates solutions frequently)
- Try the web interface to confirm: https://ssd.jpl.nasa.gov/horizons/app.html

### "Cannot find COMMAND object"

**Cause**: The object ID (1004083) might not be recognized.

**Solution**:
- Try alternative IDs: `C/2025 N1`, `3I`, `ATLAS`
- Check JPL Small-Body Database: https://ssd.jpl.nasa.gov/sbdb.cgi

### Network errors

**Cause**: Can't reach JPL servers or firewall blocking requests.

**Solution**:
- Check internet connection
- Try manually querying one observation via web interface
- Use a different network if behind restrictive firewall

### "Parse error"

**Cause**: The Horizons response format changed or isn't what we expected.

**Solution**:
- Check the saved response in the error message
- Update the parsing logic in `generate_solution44_table.py`
- Report the issue with the response format

## Advanced Usage

### Custom output filename

```python
# Edit generate_solution44_table.py, change this line:
output_file = 'my_custom_table.html'
```

### Different object

```python
# Edit generate_solution44_table.py, change COMMAND:
'COMMAND': "'YOUR_SPK_ID;'"
```

### Add more quantities

```python
# Edit QUANTITIES parameter:
'QUANTITIES': "'1,3,9,20,36,37'"  # Add more data
```

See JPL Horizons manual for available quantities:
https://ssd.jpl.nasa.gov/horizons/manual.html

## Understanding the Results

### Good Predictions (Green)

```
Total: 0.25 arcsec
3σ: 0.31 arcsec
Ratio: 0.8×
```

Solution 44 predicted this position accurately.

### Marginal (Orange)

```
Total: 0.50 arcsec
3σ: 0.31 arcsec
Ratio: 1.6×
```

Slightly beyond 3-sigma, but not a catastrophic failure.

### Failed Predictions (Red)

```
Total: 17000 arcsec
3σ: 0.31 arcsec
Ratio: 54839×
```

Solution 44 completely failed to predict this position.

## Interpreting σ Ratios

| Ratio | Meaning |
|-------|---------|
| < 1.0 | Within 3-sigma (expected ~99.7% of time) |
| 1-3 | Beyond 3-sigma but not catastrophic |
| 3-10 | Significant prediction failure |
| 10-100 | Severe failure |
| > 100 | Catastrophic failure - model is wrong |

## Example Output

The HTML table will look like this:

```
C/2025 N1 (ATLAS) - JPL Solution 44 Comparison Table

Timestamp           Obs  Observed RA    Observed Dec   Calculated RA  Calculated Dec   ΔRA      ΔDec     Total    3σ      σ ratio
2025-12-19 01:21:40 G96  11 05 53.640   +05 24 55.44   11 05 53.650   +05 24 55.40    -0.125   +0.040   0.131    0.310   0.4×
2025-12-20 02:30:15 703  11 06 12.345   +05 25 10.20   11 06 12.340   +05 25 10.25    +0.063   -0.050   0.080    0.315   0.3×
...
```

## Related Tools

This toolkit complements the other comet analysis tools:

- **`comet_residuals_analysis.py`**: Analyzes a single observation
- **`generate_solution44_table.py`**: Analyzes multiple observations (this tool)

## Data Sources

- **Observed positions**: Your input CSV (from MPEC, observations, etc.)
- **Calculated positions**: JPL Horizons System (Solution 44)
- **Observatory codes**: MPC Observatory Code List

## Citation

If you use this analysis:

```
C/2025 N1 (ATLAS) Solution 44 Multi-Observation Analysis
Generated: [date]
Observed: [date range]
Calculated: JPL Horizons Solution 44 (2025-12-17)
Analysis toolkit: [repository URL]
```

## Support

For issues with:
- **This toolkit**: Check the scripts and documentation
- **JPL Horizons**: See https://ssd.jpl.nasa.gov/horizons/
- **MPC codes**: See https://minorplanetcenter.net/iau/lists/ObsCodesF.html

---

**Last Updated**: December 2025
**Compatible with**: C/2025 N1 (ATLAS) / 3I/ATLAS
**JPL Solution**: #44 (2025-12-17)
