# Day 7 — Process Window Analysis and Edge Placement Error (EPE)

## 1. Motivation

Lithography processes must tolerate variations in exposure dose and focus while
still producing acceptable printed geometries. OPC verification evaluates
whether printed edges remain within allowable tolerances across this
manufacturing window.

Key metrics include:
- Critical Dimension (CD)
- Edge Placement Error (EPE)

---

## 2. Dose Sensitivity

Dose variations modify aerial image intensity, which propagates through
photo-chemistry and development kinetics to affect final printed dimensions.

Therefore:
CD = f(Dose)

Low sensitivity implies robust manufacturing margins.

---

## 3. Edge Placement Error (EPE)

EPE is defined as the difference between printed edge location and target design
edge location:

EPE = x_printed − x_target

OPC signoff requires EPE to remain within tight bounds over the process window.

---

## 4. Simulation Flow

1. Fixed optical system and mask
2. Sweep exposure dose
3. For each dose:
   - Apply Dill exposure model
   - Apply Mack development model
   - Extract printed resist edges
   - Measure CD and EPE
4. Plot CD vs Dose and EPE vs Dose

Script used:
- `scripts/day7_process_window.py`

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

- CD varies monotonically with dose, reflecting exposure latitude.
- EPE crosses zero near nominal dose, indicating calibration point.
- Slopes quantify process sensitivity and OPC correction requirements.

---

## 7. Relevance to OPC Verification

OPC verification evaluates:
- worst-case EPE across process window
- sensitivity to dose and focus
- hotspot identification

These metrics guide:
- OPC recipe tuning
- design rule restrictions
- yield optimization strategies

---

## 8. Next Step

Next, focus variation and defocus blur will be introduced to extend analysis into
full 2D process windows (dose–focus matrices).
