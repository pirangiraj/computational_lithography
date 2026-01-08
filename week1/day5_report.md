# Day 5 — Dill Exposure Model and Photoactive Compound (PAC) Dynamics

## 1. Motivation

Threshold resist models convert aerial image directly into printed geometry, but
real photoresist undergoes chemical transformations before development.

The Dill model describes how optical exposure converts photoactive compound (PAC)
into inactive species, which later determines dissolution behavior during
development.

Thus, Dill exposure modeling provides the physical bridge between optics and
resist chemistry.

---

## 2. Dill Exposure Equation

Let M(x, y, t) represent normalized PAC concentration.

The exposure kinetics are described by:

dM/dt = -C · I(x, y) · M

Where:
- C is the resist exposure rate constant
- I(x, y) is aerial image intensity

Solution:

M(x, y) = exp(-C · I(x, y) · Dose)

Where Dose = I · t.

Thus, PAC decays exponentially in high-intensity regions, a phenomenon known as
photo-bleaching.

---

## 3. Physical Interpretation

High intensity:
- rapid PAC depletion
- high acid generation
- faster dissolution during development

Low intensity:
- PAC remains high
- slower dissolution

Therefore, PAC distribution controls spatial variation of development rate.

---

## 4. Simulation Flow

1. Generate mask and PSF
2. Compute aerial image by optical convolution
3. Apply Dill exposure model to compute PAC map
4. Extract profiles and dose-response curves

Script used:
- `scripts/day5_dill_model.py`

---

## 5. Results

Saved images:
- `results/day5_aerial.png`
- `results/day5_pac.png`
- `results/day5_profiles.png`
- `results/day5_pac_vs_dose.png`

Interactive plots:
- `results/day5_profiles_interactive.html`
- `results/day5_pac_vs_dose_interactive.html`

### Observations

- PAC depletion follows optical intensity distribution.
- Exponential response compresses dynamic range compared to aerial image.
- Dose-response curve is nonlinear, defining resist contrast behavior.

---

## 6. Relevance to OPC and Process Modeling

OPC models must predict printed contours across variations in:
- dose
- focus
- pattern density

Since development rate depends on PAC concentration, exposure modeling is
necessary for accurate edge placement prediction.

Dill parameters are often calibrated using experimental contrast curves and
integrated into full resist models used in OPC engines.

---

## 7. Limitations of Dill Model

Dill model includes only:
- exposure chemistry

It does not include:
- acid diffusion
- post-exposure bake effects
- dissolution kinetics

Therefore, exposure modeling must be combined with development models such as
the Mack model to predict final resist contours.

---

## 8. Next Step

Next, resist development will be modeled using Mack kinetics to convert PAC maps
into dissolution rates and printed resist profiles.
