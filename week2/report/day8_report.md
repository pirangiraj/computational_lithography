# Day 8 — Dose–Focus Process Window and Worst-Case EPE

## 1. Motivation

Manufacturing variability includes both exposure dose fluctuations and focus
errors. OPC verification evaluates whether printed edges remain within tolerance
across combined variations.

Thus, process windows must be analyzed in two dimensions: dose and focus.

---

## 2. Focus Modeling

Defocus broadens the optical point-spread function (PSF), reducing image slope
and increasing sensitivity to dose and resist kinetics.

In this simulation, defocus is approximated by Gaussian broadening of the PSF.
While not a full vector defocus model, it captures the dominant physical effect:
reduced contrast and edge slope.

---

## 3. Process Window Simulation Flow

For each (dose, focus) pair:

1. Modify PSF to represent defocus
2. Compute aerial image by convolution
3. Apply Dill exposure model
4. Apply Mack development model
5. Compute continuous resist clear depth
6. Extract sub-pixel contour where clear depth equals resist thickness
7. Measure edge placement error (EPE)

---

## 4. Results

Saved in:
- `results/day8_results/`

Files:
- `epe_heatmap.png`
- `epe_heatmap_interactive.html`
- `worst_epe_vs_focus.png`
- `worst_epe_vs_focus_interactive.html`

---

## 5. Observations

- EPE increases rapidly with defocus due to reduced aerial image slope.
- Process margin shrinks as focus worsens.
- Optimal operating region appears near nominal dose and minimal defocus.

These trends are consistent with experimental lithography process behavior.

---

## 6. Relevance to OPC Verification

OPC signoff evaluates worst-case EPE across:
- dose variations
- focus variations
- pattern dependencies

Dose–focus windows determine:
- manufacturability limits
- hotspot detection
- design rule restrictions

Thus, 2D process window analysis is fundamental to OPC verification.

---

## 7. Model Limitations

This model uses:
- scalar PSF
- Gaussian defocus approximation
- no acid diffusion or PEB modeling

Industrial simulators use:
- vector imaging
- calibrated resist kinetics
- diffusion and bake models

However, the dependency structure and verification methodology remain physically
correct.

---

## 8. Next Step

Next step is pattern-dependent hotspot analysis by simulating different
geometries and evaluating local EPE sensitivity across layouts.

