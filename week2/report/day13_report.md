# Day 13 — Conditional Hotspots Across Dose–Focus Process Window

## 1. What Is a Conditional Hotspot?

A conditional hotspot is a layout location that:

- prints correctly at nominal conditions
- fails only at certain combinations of dose and focus

This makes detection difficult because:

- single-condition simulations cannot catch it
- failures appear only under process variation

Such hotspots are major contributors to yield loss in production.

---

## 2. Why Geometry Alone Is Not Enough

From earlier days, we learned:

- some geometries are intrinsically weak (corners, junctions)

However, even weak geometries may print acceptably at:

- optimal focus
- correct dose

But when:

- focus drifts
- dose shifts

optical slope reduces and resist kinetics amplify errors.

Thus hotspot severity depends on:

Geometry × Process

Not on either alone.

---

## 3. Process Window Concept

Process window describes allowable variations in:

- exposure dose
- focus

such that printed geometry remains within tolerance.

OPC verification must ensure:

For all (dose, focus) in allowed window:
    |EPE| < tolerance

Thus verification is a multi-dimensional problem.

---

## 4. Why Junctions Are Sensitive to Process Variations

At T-junctions:

- optical interference is already complex
- aerial image slope is locally low

Defocus further:

- spreads energy
- reduces gradient

Dose changes further:

- shift PAC conversion
- shift dissolution threshold

Thus junctions experience:

Nonlinear error amplification across window corners.

---

## 5. Simulation Method Used

For each (dose, focus) pair:

1. Modify PSF according to defocus
2. Compute aerial image
3. Apply Dill exposure model
4. Apply Mack development model
5. Extract binary printed geometry
6. Compute distance-based EPE field
7. Extract worst-case EPE near junction

This produces:

Worst_EPE(dose, focus)

which directly maps hotspot severity across process window.

---

## 6. Interpretation of Conditional Hotspot Heatmap

Heatmap axes:
- X → Dose
- Y → Focus

Color:
- magnitude of worst EPE near junction

Typical observations:

- low error near nominal
- sharp increase at defocus
- asymmetric sensitivity to dose

This means:

A pattern that looks safe in nominal simulations can be unsafe in real
manufacturing.

---

## 7. Industrial Significance

In production OPC flows:

- verification checks hundreds of process corners
- worst-case metrics determine signoff
- conditional hotspots trigger layout redesign or correction

Foundries often restrict:

- allowed routing geometries
- minimum spacing rules

based on conditional hotspot statistics.

---

## 8. Why Simple Design Rules Are Not Enough

Design rules assume worst-case everywhere.

But conditional hotspots show:

- some locations are worse than others
- context matters

Thus modern flows use:

- model-based verification
- hotspot libraries
- context-aware correction

This is a core task of computational lithography engineers.

---

## 9. Limitations of This Model

The present model omits:

- polarization
- mask 3D effects
- resist diffusion
- stochastic variability

However, the following behaviors are physically correct:

- combined geometry + process sensitivity
- non-linear error amplification
- conditional failure regions

Thus conceptual understanding is valid.

---

## 10. Learning Outcome of Day 13

After this exercise, it should be clear that:

- hotspot severity is process dependent
- verification must scan across windows
- nominal checks are insufficient

This concept is central to:

- OPC signoff
- DFM validation
- yield ramp analysis

---

## 11. Next Step

Next step is to introduce stochastic effects such as:

- photon shot noise
- random resist variation

and observe how variability creates random hotspots even for identical layouts.
