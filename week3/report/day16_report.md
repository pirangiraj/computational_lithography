# Day 16 — Stochastic Process Window for Contact Holes

## 1. Why Deterministic Process Windows Are Insufficient

Traditional lithography process windows are defined using:

- critical dimension (CD)
- edge placement error (EPE)

These metrics assume deterministic behavior.

However, in EUV lithography, stochastic effects dominate for small features,
especially contact holes.

Thus even if average CD is correct, some features fail randomly.

Yield depends on probability of failure, not average geometry.

---

## 2. Definition of Stochastic Process Window

A stochastic process window is defined as the region in dose–focus space where:

P(defect) < acceptable defect probability

or equivalently:

P(feature prints correctly) > required yield threshold

This shifts lithography optimization from geometry control to probability control.

---

## 3. Role of Dose in Stochastic Yield

Photon arrival is governed by Poisson statistics.

Relative noise magnitude is:

σ / N = 1 / sqrt(N)

Thus:

Higher dose → more photons → lower relative noise → better yield

However, increasing dose also affects:

- resist blur
- CD bias
- line-edge roughness

Thus dose must be optimized, not maximized.

---

## 4. Role of Focus in Stochastic Yield

Defocus reduces aerial image contrast by:

- broadening PSF
- reducing intensity gradients

This reduces chemical driving force and increases sensitivity to noise.

Thus stochastic failure probability increases sharply with defocus.

Focus control is therefore critical in EUV manufacturing.

---

## 5. Simulation Strategy Used

For each (dose, focus) pair:

1. Modify PSF to represent defocus
2. Compute aerial image of contact hole
3. Add Poisson photon noise
4. Apply Dill exposure model
5. Apply Mack development model
6. Determine whether hole opens
7. Repeat many trials to estimate probability

This yields open probability as a function of dose and focus.

---

## 6. Interpretation of Stochastic Process Window

Heatmap shows:

- region of reliable printing
- boundaries where yield collapses

This region is much smaller than deterministic CD-based window.

Thus fabs must operate well inside stochastic window, not just CD window.

---

## 7. Yield Implications

If a chip contains millions of vias, total yield becomes:

Yield_chip ≈ (P_open)^(number of vias)

Thus even small reductions in open probability lead to catastrophic yield loss.

Therefore extremely high per-via reliability is required.

---

## 8. Why OPC Cannot Solve Stochastic Windows

OPC corrects systematic errors.

Stochastic defects arise from:

- photon randomness
- chemical randomness

OPC cannot eliminate randomness.

Thus improvements must come from:

- resist materials
- exposure dose
- process control

OPC can only reduce sensitivity, not eliminate stochasticity.

---

## 9. Industrial Process Optimization

Foundries optimize:

- exposure dose
- focus budgets
- resist formulations

to maximize stochastic process window.

Design rules are often adjusted to enlarge stochastic window, not deterministic
window.

---

## 10. Learning Outcome of Day 16

After this exercise, it should be clear that:

- yield is probability-driven, not geometry-driven
- process windows must include stochastic margins
- contact holes are primary yield limiters

This understanding is critical for EUV lithography engineers.

---

## 11. Next Step

Next step is to introduce **stochastic necking and bridging in line patterns**
and analyze probability of line breaks and shorts.
