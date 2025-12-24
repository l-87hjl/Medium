# JPL Horizons API Query Examples

## The Exact Query for C/2025 N1 (ATLAS)

### Method 1: Direct URL (Copy-Paste Ready)

```
https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='1004083;'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='@G96'&TLIST='2025-12-19 01:21:40'&QUANTITIES='1,3,36,37'&TIME_DIGITS='SECONDS'&EXTRA_PREC='YES'&CSV_FORMAT='NO'
```

**Important**: Copy this entire URL and paste it into your browser. The browser will automatically handle the URL encoding.

### Method 2: Fully URL-Encoded Version

If the above doesn't work (some environments require manual encoding), use this:

```
https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND=%271004083%3B%27&OBJ_DATA=%27YES%27&MAKE_EPHEM=%27YES%27&EPHEM_TYPE=%27OBSERVER%27&CENTER=%27%40G96%27&TLIST=%272025-12-19%2001%3A21%3A40%27&QUANTITIES=%271%2C3%2C36%2C37%27&TIME_DIGITS=%27SECONDS%27&EXTRA_PREC=%27YES%27&CSV_FORMAT=%27NO%27
```

**URL Encoding Reference:**
- Single quote `'` → `%27`
- Space ` ` → `%20`
- Colon `:` → `%3A`
- Semicolon `;` → `%3B`
- At sign `@` → `%40`
- Comma `,` → `%2C`

### Method 3: Using curl (Command Line)

```bash
curl -G "https://ssd.jpl.nasa.gov/api/horizons.api" \
  --data-urlencode "format=text" \
  --data-urlencode "COMMAND='1004083;'" \
  --data-urlencode "OBJ_DATA='YES'" \
  --data-urlencode "MAKE_EPHEM='YES'" \
  --data-urlencode "EPHEM_TYPE='OBSERVER'" \
  --data-urlencode "CENTER='@G96'" \
  --data-urlencode "TLIST='2025-12-19 01:21:40'" \
  --data-urlencode "QUANTITIES='1,3,36,37'" \
  --data-urlencode "TIME_DIGITS='SECONDS'" \
  --data-urlencode "EXTRA_PREC='YES'" \
  --data-urlencode "CSV_FORMAT='NO'" \
  > horizons_response.txt
```

The `--data-urlencode` flag automatically handles the URL encoding for you.

### Method 4: Using Python requests Library

```python
import requests

url = "https://ssd.jpl.nasa.gov/api/horizons.api"

params = {
    'format': 'text',
    'COMMAND': "'1004083;'",
    'OBJ_DATA': "'YES'",
    'MAKE_EPHEM': "'YES'",
    'EPHEM_TYPE': "'OBSERVER'",
    'CENTER': "'@G96'",
    'TLIST': "'2025-12-19 01:21:40'",
    'QUANTITIES': "'1,3,36,37'",
    'TIME_DIGITS': "'SECONDS'",
    'EXTRA_PREC': "'YES'",
    'CSV_FORMAT': "'NO'"
}

response = requests.get(url, params=params)
print(response.text)
```

Python's `requests` library handles URL encoding automatically.

## Breaking Down the Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `format` | `text` | Return plain text (not JSON) |
| `COMMAND` | `'1004083;'` | SPK-ID for C/2025 N1 (ATLAS) - note the semicolon! |
| `OBJ_DATA` | `'YES'` | Include object metadata |
| `MAKE_EPHEM` | `'YES'` | Generate ephemeris |
| `EPHEM_TYPE` | `'OBSERVER'` | Observer-based ephemeris (not vector) |
| `CENTER` | `'@G96'` | Observer location: G96 = Mt. Lemmon Survey |
| `TLIST` | `'2025-12-19 01:21:40'` | Single time point (not a range) |
| `QUANTITIES` | `'1,3,36,37'` | What to output (see below) |
| `TIME_DIGITS` | `'SECONDS'` | Time precision to seconds |
| `EXTRA_PREC` | `'YES'` | Maximum decimal precision |
| `CSV_FORMAT` | `'NO'` | Plain text table format |

### Quantities Explained

The `QUANTITIES='1,3,36,37'` parameter specifies what data to include:

- **1**: Astrometric RA and DEC
- **3**: Rates of change (dRA*cosD, dDEC/dt)
- **36**: 1-sigma RA and DEC uncertainties
- **37**: 3-sigma positional uncertainty (POS_3sigma)

## Expected Response Format

When you query successfully, you'll get a response like this:

```
*******************************************************************************
Ephemeris / API_USER Mon Dec 19 01:21:40 2025 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: C/2025 N1 (ATLAS)               {source: JPL#44}
Center body name: Earth (399)                     {source: DE441}
Center-site name: Mt. Lemmon Survey, Arizona
*******************************************************************************
Start time      : A.D. 2025-Dec-19 01:21:40.0000 UT
Stop  time      : A.D. 2025-Dec-19 01:21:40.0000 UT
Step-size       : DISCRETE TIME LIST
*******************************************************************************
...
$$SOE
 2025-Dec-19 01:21:40.0000 *  HH MM SS.SSS +DD MM SS.SS  dRA*cosD  d(DEC)/dt  Unc_RA Unc_DEC POS_3sig
$$EOE
...
*******************************************************************************
```

The key data is between the `$$SOE` (Start Of Ephemeris) and `$$EOE` (End Of Ephemeris) markers.

### What to Extract

From the ephemeris line, you need:

1. **RA**: The hours, minutes, seconds (e.g., `11 05 53.640`)
2. **Dec**: The degrees, arcminutes, arcseconds (e.g., `+05 24 55.44`)
3. **POS_3sig**: The 3-sigma uncertainty in arcseconds (e.g., `0.310`)

## Example Response (Hypothetical)

```
$$SOE
 2025-Dec-19 01:21:40.0000 *  11 05 53.640 +05 24 55.44  +123.456  -789.012  0.150  0.145  0.310
$$EOE
```

In this example:
- **RA**: 11h 05m 53.640s
- **Dec**: +05° 24' 55.44"
- **dRA*cosD**: +123.456 arcsec/hour
- **d(DEC)/dt**: -789.012 arcsec/hour
- **Unc_RA**: 0.150 arcsec (1-sigma)
- **Unc_DEC**: 0.145 arcsec (1-sigma)
- **POS_3sig**: 0.310 arcsec (3-sigma total)

## Common Errors and Solutions

### Error: "BATVAR: syntax or missing closing quote in TLIST"

**Cause**: The TLIST parameter wasn't properly quoted or encoded.

**Solution**: Make sure single quotes wrap the time string:
```
TLIST='2025-12-19 01:21:40'
```

If manually encoding, use:
```
TLIST=%272025-12-19%2001%3A21%3A40%27
```

### Error: "Cannot find COMMAND object"

**Cause**: Missing semicolon after SPK-ID.

**Solution**: Include the semicolon:
```
COMMAND='1004083;'    ← CORRECT
COMMAND='1004083'     ← WRONG
```

### Error: "No matches found for CENTER"

**Cause**: Observer code not prefixed with `@`.

**Solution**:
```
CENTER='@G96'    ← CORRECT
CENTER='G96'     ← WRONG
```

## Alternative: Web Interface

If the API is giving you trouble, use the web interface:

**URL**: https://ssd.jpl.nasa.gov/horizons/app.html

**Steps**:

1. **Target Body**
   - Search for: `C/2025 N1` or `1004083`
   - Select: "C/2025 N1 (ATLAS)"

2. **Observer Location**
   - Type: `G96`
   - Select: "Mt. Lemmon Survey"

3. **Time Specification**
   - Start time: `2025-12-19 01:21:40`
   - Stop time: `2025-12-19 01:21:40` (same)
   - Step size: `1 d` (doesn't matter for single time)

4. **Table Settings**
   - Click "Table Settings"
   - Quantities: Select `1` (RA/Dec), `3` (rates), `36` (1-sig unc), `37` (3-sig unc)
   - Extra precision: `YES`
   - Time digits: `SECONDS`

5. **Generate Ephemeris**
   - Click "Generate Ephemeris"
   - Read the table between `$$SOE` and `$$EOE`

## Testing Your Query

To verify your query is working:

### Test 1: Get Any Response

Try the simplest query first:
```
https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='1004083;'
```

This should return basic information about the object.

### Test 2: Add Ephemeris

Add the ephemeris parameters:
```
https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='1004083;'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='@G96'
```

This should generate an ephemeris (but for the default time range).

### Test 3: Full Query

Use the complete query from the top of this document.

## Quick Reference Card

**Copy-Paste Template:**

```
BASE: https://ssd.jpl.nasa.gov/api/horizons.api

PARAMETERS:
format=text
COMMAND='[OBJECT_ID];'
CENTER='@[OBSERVER_CODE]'
TLIST='[YYYY-MM-DD HH:MM:SS]'
QUANTITIES='1,3,36,37'
TIME_DIGITS='SECONDS'
EXTRA_PREC='YES'
MAKE_EPHEM='YES'
EPHEM_TYPE='OBSERVER'
OBJ_DATA='YES'
CSV_FORMAT='NO'
```

**For C/2025 N1 at G96 on Dec 19:**

```
OBJECT_ID = 1004083
OBSERVER_CODE = G96
YYYY-MM-DD HH:MM:SS = 2025-12-19 01:21:40
```

## Verification Checklist

Before running your analysis, verify:

- [ ] URL includes `COMMAND='1004083;'` (with semicolon)
- [ ] Observer is `CENTER='@G96'` (with @ symbol)
- [ ] Time is `TLIST='2025-12-19 01:21:40'` (exact match)
- [ ] Quantities include `'1,3,36,37'` (uncertainties)
- [ ] `EXTRA_PREC='YES'` is set
- [ ] `TIME_DIGITS='SECONDS'` is set
- [ ] Response contains `$$SOE` and `$$EOE` markers
- [ ] Data line has RA, Dec, and POS_3sigma values

## Need Help?

If you're still getting errors:

1. Try the web interface first (easier to debug)
2. Copy the exact URL from Method 1 above
3. Check for typos in the SPK-ID (1004083)
4. Verify the date/time format exactly
5. Make sure quotes are included around parameter values

The most common issue is forgetting the semicolon after the object ID or the @ before the observer code!
