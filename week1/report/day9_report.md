# Day 9 — Pattern-Dependent Hotspot and Local EPE Analysis

## 1. Motivation

Lithographic printing behavior depends strongly on local layout geometry.
Even under identical process conditions, different pattern types exhibit
different edge placement errors (EPE).

Thus, OPC verification must identify layout-specific hotspots.

---

## 2. Pattern Dependence Mechanisms

Pattern geometry affects:

- optical proximity
- aerial image slope
- resist chemical gradients

Line-ends, corners, and dense patterns are particularly sensitive to
diffraction and resist kinetics, leading to elevated EPE.

---

## 3. Patterns Simulated

Three canonical geometries were analyzed:

1. Isolated vertical line
2. Dense line array
3. Line-end structure

These represent common hotspot categories in design verification.

---

## 4. Simulation Flow

For each pattern:

1. Optical convolution with defocused PSF
2. Dill exposure to compute PAC concentration
3. Mack development to compute dissolution depth
4. Sub-pixel contour extraction
5. Local EPE measurement

Script:
- `scripts/day9_hotspot_patterns.py`

---

## 5. Results

Saved in:
- `results/day9_results/`

Files include:
- Individual clear depth maps for each pattern
- Pattern EPE comparison plots
- Interactive bar chart
- Numeric EPE values

---

## 6. Observations

- Line-end structures exhibit larger EPE than straight lines.
- Dense patterns show different behavior compared to isolated lines.
- Pattern-dependent sensitivity explains why global OPC biases are insufficient.

---

## 7. Relevance to OPC Verification

Modern OPC verification involves:

- scanning layouts for known hotspot geometries
- evaluating local EPE under process windows
- inserting localized corrections

Pattern-based hotspot detection is therefore a core step in signoff flows.

---

## 8. Next Step

Next, edge placement error will be evaluated along entire contours to produce
spatial EPE maps rather than single-point measurements.
