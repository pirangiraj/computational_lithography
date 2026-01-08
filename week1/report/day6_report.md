# Day 6 — Mack Development Model and Final Resist Profiles

## 1. Role of Development in Lithography

After exposure and post-exposure bake, photoresist is developed in alkaline
solution. The final printed geometry depends on how fast different regions of
resist dissolve.

Unlike threshold models, development is a rate-driven kinetic process that
depends on local chemical state.

---

## 2. Mack Development Model

The Mack model relates dissolution rate to PAC concentration:

R(M) = Rmax / (1 + (M / M0)^n)

Where:
- M is PAC concentration
- Rmax is maximum dissolution rate
- M0 is PAC at mid-rate
- n controls resist contrast

This produces strong nonlinearity:
- low PAC clears rapidly
- high PAC remains nearly insoluble

---

## 3. From Rate to Final Geometry

If development time is T and resist thickness is d:

Resist clears where:

R(M) · T > d

Thus, printed resist pattern is obtained by thresholding the integrated
dissolution depth rather than optical intensity.

---

## 4. Simulation Flow

1. Generate mask and PSF
2. Compute aerial image (optical convolution)
3. Apply Dill model to compute PAC concentration
4. Compute dissolution rate using Mack model
5. Apply development threshold to obtain final resist pattern
6. Measure critical dimension (CD)

Script used:
- `scripts/day6_mack_model.py`

---

## 5. Results

Saved in:
- `results/day6_results/`

Key outputs:
- `aerial.png`
- `pac.png`
- `rate.png`
- `printed.png`
- `profiles.png`
- `profiles_interactive.html`
- `cd_measurement.txt`

---

## 6. Observations

- Optical blur broadens features in aerial image.
- PAC distribution smooths chemical response.
- Mack model sharply amplifies contrast at edges.
- Final printed resist shows steeper edges than aerial image alone.
- CD is sensitive to resist and development parameters.

---

## 7. Relevance to OPC and Process Calibration

OPC engines require calibrated resist models to predict printed contours under
process variations.

Mack parameters are extracted from experimental data and embedded into compact
resist models used for:
- OPC correction
- hotspot detection
- process window optimization

Therefore, resist development modeling is critical for accurate lithography
simulation.

---

## 8. Next Step

Next, process window analysis will be performed by sweeping dose and focus to
evaluate edge placement error (EPE) sensitivity, forming the basis of OPC
verification metrics.
