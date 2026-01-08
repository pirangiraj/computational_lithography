# Day 4 — Threshold Photoresist Model and Printed Contours

## 1. Role of Photoresist in Lithography

While the aerial image defines the optical intensity distribution at the wafer
plane, the photoresist converts this optical energy into chemical changes that
determine which regions are removed during development.

Thus, the photoresist acts as a nonlinear transfer function between optical
exposure and final printed geometry.

---

## 2. Threshold Resist Model

As a first-order approximation, resist behavior can be modeled using a simple
threshold rule:

Printed(x, y) = 1 if I(x, y) ≥ Ith  
Printed(x, y) = 0 if I(x, y) < Ith

Where:
- I(x, y) is the normalized aerial image intensity
- Ith is the resist threshold dose

This model assumes:
- infinite resist contrast
- no diffusion
- no post-exposure effects

Although unrealistic chemically, it provides insight into how aerial image
contrast maps into printed geometry.

---

## 3. Edge Formation Mechanism

Printed edges occur at spatial locations where aerial image intensity crosses
the resist threshold.

Therefore:
- edge position depends on local slope of aerial image
- shallow slopes lead to high CD sensitivity to dose
- steep slopes improve dimensional control

Thus, aerial image contrast directly impacts process robustness.

---

## 4. Simulation Flow

1. Generate two-line mask pattern
2. Compute PSF using Fourier optics
3. Convolve mask with PSF to obtain aerial image
4. Apply intensity threshold to obtain printed resist
5. Extract line profiles to visualize edge locations

Script used:
- `scripts/day4_resist_threshold.py`

---

## 5. Numerical Results

Saved files:
- `results/day4_aerial.png` — optical intensity distribution
- `results/day4_resist.png` — printed binary resist pattern
- `results/day4_profile.png` — intensity profile with threshold crossing

### Observations

- Printed features are wider than mask due to optical blur.
- Valley between features may disappear if threshold is low, causing bridging.
- Edge positions shift significantly with small threshold changes.

This demonstrates how resist nonlinearity amplifies optical proximity effects.

---

## 6. Relevance to OPC and Process Control

OPC must ensure that printed contours match design intent across variations in:
- dose
- focus
- resist sensitivity

Since edges are defined by threshold crossings, OPC corrections must improve:
- aerial image slope at edges
- separation between neighboring intensity peaks

Therefore, resist modeling is essential for predicting CD and EPE, not just
optical intensity.

---

## 7. Limitations of Threshold Model

The threshold model ignores:
- chemical amplification
- post-exposure diffusion
- dissolution kinetics

Thus, it cannot predict:
- resist profile shape
- line edge roughness
- exposure latitude accurately

More realistic models such as Dill exposure and Mack development are required
for quantitative lithography simulation.

---

## 8. Next Step

Next, chemical exposure models will be introduced to simulate photoactive
compound (PAC) concentration and development rates, moving toward physically
based resist modeling.
