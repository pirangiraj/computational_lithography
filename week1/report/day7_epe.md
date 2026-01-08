# Day 7 — Continuous Resist Development and Sub-Pixel EPE Extraction

## 1. Why Binary Resist Models Are Insufficient

Thresholding development depth into binary images produces pixel-limited
geometry. This causes artificial quantization of CD and suppresses sensitivity
to dose and focus.

Real printed contours are defined by continuous resist dissolution depth, not
binary states.

Therefore, contour extraction must be performed on continuous resist surfaces.

---

## 2. Continuous Development Surface

From Dill exposure and Mack development:

Clear depth:
D(x,y) = R(M(x,y)) · T_dev

Printed contour occurs where:
D(x,y) = resist_thickness

Thus, edge locations correspond to level sets of a continuous function.

---

## 3. Sub-Pixel Edge Extraction

Along 1D profiles, edges are detected where:

(D[i] - d)(D[i+1] - d) < 0

Linear interpolation provides sub-pixel edge position:

x = i + (d - D[i]) / (D[i+1] - D[i])

This enables continuous variation of CD and EPE with process parameters.

---

## 4. Simulation Flow

1. Optical imaging using PSF convolution
2. Dill exposure to compute PAC concentration
3. Mack model to compute dissolution rate
4. Clear depth calculation
5. Sub-pixel contour extraction
6. CD and EPE vs dose computation

Script:
- `scripts/day7_epe_continuous.py`

---

## 5. Results

Saved in:
- `results/day7_results/`

Files:
- `cd_vs_dose.png`
- `epe_vs_dose.png`
- `cd_vs_dose_interactive.html`
- `epe_vs_dose_interactive.html`
- `process_window_data.txt`

---

## 6. Observations

- CD varies smoothly with dose.
- EPE shifts continuously, crossing zero at nominal exposure.
- Sensitivity depends on resist contrast and development threshold.

This behavior matches expected lithographic process physics.

---

## 7. Relevance to OPC Verification

OPC verification relies on:

- continuous contour prediction
- accurate EPE sensitivity to dose and focus
- worst-case error detection across process windows

Binary resist approximations cannot support these analyses.

Continuous resist modeling is therefore mandatory for physically meaningful
OPC evaluation.

---

## 8. Next Step

Extend model to include focus variation by modifying PSF width and generating
2D dose–focus process window maps.

