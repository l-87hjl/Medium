# C/2025 N1 (ATLAS) Residuals Analysis - Manual Calculation Guide

## Objective
Determine whether JPL Solution 44's predicted position for C/2025 N1 (ATLAS) on December 19, 2025 matches the actual observed position within the model's stated 3-sigma uncertainty.

## Data Sources

### Observed Position (O) - December 19, 2025 MPEC
- **Time**: 2025-12-19 01:21:40 UT
- **RA**: 11h 05m 53.640s
- **Dec**: +05° 24' 55.44"
- **Observer**: G96 (Mt. Lemmon Survey)
- **Source**: Minor Planet Electronic Circular (MPEC)

### Calculated Position (C) - JPL Horizons Solution 44
To obtain this data, query JPL Horizons with:

**Method 1: Web Interface**
1. Go to https://ssd.jpl.nasa.gov/horizons/app.html
2. Enter target: `C/2025 N1` or `1004083`
3. Set observer: `G96` (Mt. Lemmon Survey)
4. Set time: `2025-12-19 01:21:40` UT
5. Select quantities: 1 (RA/Dec), 3 (Rates), 36,37 (Uncertainties)
6. Enable: EXTRA_PREC=YES, TIME_DIGITS=SECONDS

**Method 2: API Query**
```
https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='1004083;'&CENTER='@G96'&TLIST='2025-12-19 01:21:40'&QUANTITIES='1,3,36,37'&TIME_DIGITS='SECONDS'&EXTRA_PREC='YES'
```

**Expected Output Fields:**
- Calculated RA (hours, minutes, seconds)
- Calculated Dec (degrees, arcminutes, arcseconds)
- dRA*cosD (RA rate in arcsec/hour)
- d(DEC)/dt (Dec rate in arcsec/hour)
- Unc_RA (RA uncertainty in arcseconds)
- Unc_DEC (Dec uncertainty in arcseconds)
- POS_3sigma (total 3-sigma positional uncertainty in arcseconds)

## Calculation Steps

### Step 1: Convert Coordinates to Decimal Degrees

**Observed Position:**
```
RA = (11h + 05m/60 + 53.640s/3600) × 15°/hour
   = (11 + 0.083333 + 0.014900) × 15
   = 11.098233 × 15
   = 166.473500°

Dec = 05° + 24'/60 + 55.44"/3600
    = 5° + 0.400000° + 0.015400°
    = 5.415400°
```

**Calculated Position:**
```
[To be filled in from JPL Horizons query]
RA_calc = ? °
Dec_calc = ? °
```

### Step 2: Calculate Residuals (O - C)

**RA Residual (with cos(Dec) correction):**
```
ΔRA = (RA_obs - RA_calc) × cos(Dec_avg) × 3600 arcsec/degree

where Dec_avg = (Dec_obs + Dec_calc) / 2
```

**Dec Residual:**
```
ΔDec = (Dec_obs - Dec_calc) × 3600 arcsec/degree
```

**Total Angular Separation:**
```
Total = √(ΔRA² + ΔDec²) arcseconds
```

### Step 3: Compare to 3-Sigma Uncertainty

**Significance Test:**
```
σ_ratio = Total_separation / POS_3sigma

If σ_ratio > 1.0:
    → Observed position is OUTSIDE the 3-sigma error ellipse
    → Solution 44 failed to predict the position within stated uncertainty

If σ_ratio ≤ 1.0:
    → Observed position is within predicted uncertainty
    → Solution 44 successfully predicted the position
```

## Mathematical Notes

### Why the cos(Dec) Correction?

RA is measured in hours/degrees along the celestial equator. As you move toward the poles, lines of constant RA converge. At declination δ, the physical angular separation for a given RA difference is:

```
Δθ_RA = ΔRA × cos(δ)
```

This ensures we're measuring actual angular distance on the sky, not just coordinate differences.

### Precision Requirements

- Use at least 6 decimal places for degree calculations
- Carry full precision through all intermediate steps
- Round only the final result for reporting

### Example Calculation (Template)

```
OBSERVED (O):
  RA  = 166.473500°  (11h 05m 53.640s)
  Dec =   5.415400°  (+05° 24' 55.44")

CALCULATED (C) [from JPL Horizons]:
  RA  = ______.__°  (__h __m __.___s)
  Dec = ______.__°  (±__° __' __.__")
  POS_3sigma = ______.__ arcsec

RESIDUALS (O-C):
  ΔRA  = (166.473500 - ___.___)° × cos(___.__°) × 3600
       = ____________ arcsec

  ΔDec = (5.415400 - ___.___)° × 3600
       = ____________ arcsec

  Total = √(ΔRA² + ΔDec²)
        = ____________ arcsec
        = ____________ degrees

SIGNIFICANCE:
  σ_ratio = Total / POS_3sigma
          = ________ / ________
          = ________ ×

  Conclusion: [Within/Outside] 3-sigma bounds
```

## Interpretation

### If the observation falls within 3-sigma:
- Solution 44 successfully predicted the comet's position
- The orbital model is working as expected
- The uncertainty estimates are realistic

### If the observation falls outside 3-sigma:
- Solution 44 failed to predict the position within its stated uncertainty
- Possible causes:
  - Non-gravitational forces (outgassing) stronger than modeled
  - Insufficient arc of observations before prediction
  - Model convergence was illusory
  - Systematic errors in the orbital determination

For a statistically significant failure, we'd expect:
- σ_ratio > 3 (beyond 3-sigma) indicates ~99.7% confidence of model failure
- σ_ratio > 10 indicates a catastrophic prediction failure
- σ_ratio > 1000 indicates the model was fundamentally wrong

## Historical Context

According to the analysis prompt, Solution 44 was published on December 17, 2025, claiming convergence on the comet's orbit. The December 19 observation serves as a "final exam" - an independent test of whether the solution could actually predict the comet's position.

If the predicted failure (~17,000 arcsec ≈ 4.7°) is confirmed, it would indicate that:
1. The December 17 "convergence" was premature
2. Solution 44 could fit existing data but not predict new positions
3. The subsequent 5,000+ observations were not refinements but corrections
