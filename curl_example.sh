#!/bin/bash
#
# Simple curl command to query JPL Horizons for C/2025 N1 (ATLAS)
# Copy and paste this entire command into your terminal
#

echo "Querying JPL Horizons for C/2025 N1 (ATLAS)..."
echo "Observer: Mt. Lemmon Survey (G96)"
echo "Time: 2025-12-19 01:21:40 UT"
echo ""

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
  -o horizons_response.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Success! Response saved to: horizons_response.txt"
    echo ""
    echo "Looking for ephemeris data..."
    echo ""

    # Extract the ephemeris section
    sed -n '/\$\$SOE/,/\$\$EOE/p' horizons_response.txt | grep -v '\$\$'

    echo ""
    echo "To extract the values you need:"
    echo "  grep -A 1 '\$\$SOE' horizons_response.txt"
    echo ""
    echo "Then enter the RA, Dec, and POS_3sigma into comet_residuals_manual_entry.py"
else
    echo ""
    echo "✗ Query failed. Check your internet connection."
    echo "Or try the web interface: https://ssd.jpl.nasa.gov/horizons/app.html"
fi
