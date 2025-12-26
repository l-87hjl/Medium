# JPL Horizons Ephemeris Lookup Tool

Query JPL Horizons for precise ephemeris data including position, proper motion, and 3-sigma uncertainties for any celestial object from any observatory location.

## Features

- **Observatory Code Support**: Any MPC observatory code (b67, G96, 568, etc.)
- **MPC Timestamp Format**: Standard MPC decimal day format (YYYY MM DD.dddddd)
- **Comprehensive Data**: RA/DEC, proper motion, 3-sigma uncertainties, error ellipse parameters
- **Multiple Interfaces**: Web page, Python CLI, or local server

## Output Data

For each query, you'll receive:

- **Epoch and Solution Number** (from JPL database)
- **UTC Time** (converted from MPC timestamp)
- **RA (ICRF/J2000)** - Right Ascension
- **DEC (ICRF/J2000)** - Declination
- **dRA*cosD** - Proper motion in RA (arcsec/hr)
- **d(DEC)/dt** - Proper motion in DEC (arcsec/hr)
- **RA_3sigma** - 3-sigma uncertainty in RA (arcsec)
- **DEC_3sigma** - 3-sigma uncertainty in DEC (arcsec)
- **SMAA_3sig** - Semi-major axis of error ellipse (arcsec)
- **SMIA_3sig** - Semi-minor axis of error ellipse (arcsec)
- **Theta** - Position angle of error ellipse (deg, East of North)

## Usage Options

### Option 1: Web Interface (Simple but may have CORS issues)

**File**: `jpl_horizons_lookup.html`

1. Open `jpl_horizons_lookup.html` in your web browser
2. Fill in the form:
   - **Object ID**: `1004083` (or `C/2025 N1`)
   - **Observatory Code**: `G96`
   - **MPC Timestamp**: `2025 12 19.007280`
3. Click "Query JPL Horizons"

**Note**: Uses a CORS proxy (corsproxy.io) which may be unreliable. If you get errors, use Option 2 or 3.

---

### Option 2: Python Command-Line Tool (Recommended)

**File**: `jpl_horizons_query.py`

**Installation**:
```bash
pip install requests
```

**Usage**:
```bash
# Interactive mode
python jpl_horizons_query.py

# Command-line mode
python jpl_horizons_query.py 1004083 G96 "2025 12 19.007280"
```

**Example**:
```bash
$ python jpl_horizons_query.py 1004083 G96 "2025 12 19.007280"

======================================================================
JPL HORIZONS QUERY TOOL
======================================================================

Querying JPL Horizons...
  Object: 1004083
  Observatory: G96
  MPC Time: 2025 12 19.007280
  UTC Time: 2025-12-19 00:10:29.000

✓ Raw response saved to: horizons_query_1004083_G96.txt

======================================================================
EPHEMERIS DATA
======================================================================

Solution:     JPL#44
Epoch (JD):   2460718.5
UTC Time:     2025-12-19 00:10:29

Parameter            Value                     Unit
----------------------------------------------------------------------
RA (ICRF)            11 05 53.640             HH MM SS.sss
DEC (ICRF)           +05 24 55.44             DD MM SS.ss
dRA*cosD             -145.32                  arcsec/hr
d(DEC)/dt            +32.18                   arcsec/hr
RA_3sigma            0.45                     arcsec
DEC_3sigma           0.38                     arcsec
SMAA_3sig            0.52                     arcsec
SMIA_3sig            0.31                     arcsec
Theta                127.3                    deg (E of N)
======================================================================
```

---

### Option 3: Local Server (For Web Interface without CORS issues)

**File**: `jpl_horizons_server.py`

**Installation**:
```bash
pip install flask flask-cors requests
```

**Usage**:

1. **Start the server**:
```bash
python jpl_horizons_server.py
```

2. **Update the web page** to use the local server:

Open `jpl_horizons_lookup.html` and modify line ~257:
```javascript
// Change this:
const baseUrl = 'https://ssd.jpl.nasa.gov/api/horizons.api';

// To this:
const baseUrl = 'http://localhost:5000/api/horizons';
```

Also comment out or remove the CORS proxy code (lines ~278-281):
```javascript
// Remove these lines:
// const corsProxy = 'https://corsproxy.io/?';
// const url = corsProxy + encodeURIComponent(horizonsUrl);

// Use this instead:
const url = horizonsUrl;
```

3. **Open the web page** in your browser while the server is running

---

## Example Queries

### C/2025 N1 (ATLAS) from Mt. Lemmon
```bash
python jpl_horizons_query.py "C/2025 N1" G96 "2025 12 19.007280"
```

### Comet from Lemmon Observatory (b67)
```bash
python jpl_horizons_query.py 1004083 b67 "2025 12 20.134567"
```

### Asteroid from Mauna Kea (568)
```bash
python jpl_horizons_query.py 433 568 "2025 12 25.500000"
```

## MPC Timestamp Format

The MPC timestamp format is: **YYYY MM DD.dddddd**

Where:
- `YYYY` = Year
- `MM` = Month
- `DD.dddddd` = Day with fractional part

**Examples**:
- `2025 12 19.007280` = 2025-12-19 at 00:10:29 UTC (0.007280 days after midnight)
- `2025 12 19.500000` = 2025-12-19 at 12:00:00 UTC (noon)
- `2025 12 19.999999` = 2025-12-19 at 23:59:59 UTC (end of day)

**Conversion**:
- 0.25 days = 06:00:00 (6 AM)
- 0.50 days = 12:00:00 (noon)
- 0.75 days = 18:00:00 (6 PM)

## Technical Details

### API Parameters
- **QUANTITIES**: `'1,3,36,37'` (RA/Dec, Rates, 3-sigma uncertainties)
- **EXTRA_PREC**: `'YES'` (high precision output)
- **TIME_DIGITS**: `'SECONDS'` (timestamp precision)
- **EPHEM_TYPE**: `'OBSERVER'` (observer ephemeris)

### Observatory Codes
Common MPC observatory codes:
- **G96**: Mt. Lemmon Survey, Arizona
- **b67**: LemmonMount, Arizona
- **568**: Mauna Kea, Hawaii
- **Q21**: Utsunomiya, Japan
- **M73**: Abu Dhabi Astronomical Observatory
- **W68**: Cerro Tololo, Chile
- **I41**: Zwicky Transient Facility (ZTF), California

[Full list available at MPC](https://minorplanetcenter.net/iau/lists/ObsCodesF.html)

## Troubleshooting

### CORS Errors in Web Interface
- **Solution 1**: Use the Python CLI tool (`jpl_horizons_query.py`)
- **Solution 2**: Run the local server (`jpl_horizons_server.py`)
- **Solution 3**: Use a browser extension to disable CORS (not recommended for production)

### "No ephemeris data found"
- Check that the object ID is valid (use SPK-ID for best results)
- Verify the timestamp is within a reasonable range
- Ensure the observatory code is valid

### Connection Timeout
- Check your internet connection
- JPL Horizons may be temporarily unavailable
- Try again in a few moments

## Files

- `jpl_horizons_lookup.html` - Web interface
- `jpl_horizons_query.py` - Command-line tool
- `jpl_horizons_server.py` - Local proxy server
- `JPL_HORIZONS_LOOKUP_README.md` - This file

## License

Part of the C/2025 N1 (ATLAS) analysis toolkit.
