# Day 11 — 2D Hotspot Mapping Near Corner Structures in Lithography

## 1. Why Geometry Matters in Lithography

In early lithography learning, patterns are often treated as simple straight
lines. However, real integrated circuit layouts are full of:

- corners
- jogs
- T-junctions
- line-ends

These geometries introduce strong two-dimensional optical and resist effects.
Even if straight edges print correctly, corners often fail first.

Such local failures are called **lithography hotspots**.

A hotspot is not a global CD error. It is a **localized region where EPE or CD
violates tolerance**, even though nearby regions may be acceptable.

---

## 2. Optical Origin of Corner Hotspots

At straight edges:

- diffraction occurs mainly perpendicular to the edge
- image slope is relatively constant along the edge

At corners:

- diffraction spreads in both x and y directions
- energy redistributes around the corner
- aerial image contrast is reduced locally

This produces:

- lower intensity gradients
- blurred corner profiles
- weaker resist driving force

Even before considering resist chemistry, corners are already disadvantaged in
optical imaging.

---

## 3. Chemical and Development Effects at Corners

After optical exposure, chemical effects amplify geometric sensitivity:

### 3.1 Dill Exposure

PAC concentration depends exponentially on local intensity:

M(x, y) = exp(−C · I(x, y))

Small reductions in intensity near corners lead to:

- higher remaining PAC
- reduced dissolution during development

### 3.2 Mack Development

Development rate is highly nonlinear:

R(M) = Rmax / (1 + (M / M0)^n)

So a small increase in PAC near corners leads to:

- large reduction in dissolution rate
- incomplete clearing near corner edges

This is why corners often show:

- rounding
- pull-back
- line-end shortening

Thus, corner hotspots are not only optical, but **optics + chemistry + kinetics**
combined.

---

## 4. What Does “2D EPE Map” Mean?

Instead of measuring EPE at one or two locations, we want to know:

How much does the printed contour deviate from the design contour **at every
location near the corner**?

Mathematically:

EPE(x, y) = distance from printed contour − distance from target contour

This produces a spatial field showing:

- where errors concentrate
- how far errors extend
- whether errors are localized or spread

In OPC verification, such spatial maps are used to:

- detect hotspots
- rank severity
- guide localized corrections

---

## 5. Modeling Strategy Used in This Simulation

This simulation follows the full lithography pipeline:

### Step 1 — Mask Geometry

An L-shaped pattern is generated to represent a corner.

This is representative of routing layers and metal interconnect geometries.

### Step 2 — Optical Imaging

- A circular pupil is converted to PSF using Fourier optics.
- Defocus is approximated by Gaussian broadening of the PSF.
- Mask is convolved with PSF to produce aerial image.

This captures:
- diffraction blur
- focus degradation of image slope

### Step 3 — Dill Exposure Model

PAC concentration is computed as:

M = exp(−C · I)

This converts optical intensity into chemical state.

### Step 4 — Mack Development Model

Dissolution rate:

R(M) = Rmax / (1 + (M / M0)^n)

Clear depth:

D(x, y) = R · T_dev

This produces a **continuous resist depth surface**.

### Step 5 — Printed Geometry

Binary printed resist is approximated by:

Printed = D > resist_thickness

Although industrial tools extract precise contours, binary maps are sufficient
for distance-based hotspot estimation.

### Step 6 — Distance Transform for EPE

Distance transforms compute:

- distance to nearest target edge
- distance to nearest printed edge

Local error is approximated as:

EPE(x, y) = dist_printed − dist_target

Positive values indicate shrink, negative values indicate expansion.

---

## 6. Region of Interest (ROI) Near Corner

Instead of analyzing the entire image, only a small window near the corner is
examined.

This reflects real verification workflows where:

- local hotspots are isolated
- global areas are ignored

The ROI allows:

- high-resolution visualization
- focused severity analysis

---

## 7. Results and Interpretation

### 7.1 Printed Resist Image

The printed resist image shows:

- rounding near the corner
- reduced feature width close to junction

This confirms optical and chemical weakening at the corner.

### 7.2 EPE Heatmap

The EPE heatmap reveals:

- highest magnitude errors concentrated near inner corner
- errors decay along straight arms
- asymmetry depending on imaging conditions

This confirms that the corner is a **localized lithographic failure site**.

### 7.3 Worst-Case EPE

Worst-case EPE value provides:

- quantitative hotspot severity
- metric for OPC correction strength

In industrial verification, worst-case EPE thresholds determine whether a design
passes or fails lithography checks.

---

## 8. Why Corners Need Special OPC Treatment

Global bias correction cannot fix corner rounding because:

- straight edges and corners require different corrections
- increasing dose helps straight edges but worsens line-end pullback

Therefore OPC must:

- add serif structures
- locally widen corners
- apply geometry-specific corrections

This simulation explains *why* such corrections are necessary from physical
first principles.

---

## 9. Limitations of the Present Model

This educational model does not include:

- vector electromagnetic effects
- polarization
- acid diffusion during post-exposure bake
- stochastic photon effects

Industrial simulators include all of these.

However, dominant physical trends are correctly captured:

- reduced image slope at corners
- chemical amplification of optical non-uniformity
- localized hotspot behavior

Thus, the **mechanistic understanding is valid**, even if absolute values are not
calibrated to a real process.

---

## 10. Connection to OPC Verification Workflows

In real OPC verification:

- full-chip layouts are scanned
- geometric fragments are matched to hotspot libraries
- EPE fields are computed for suspect regions
- worst-case locations are reported

The analysis performed here mirrors:

- localized contour deviation evaluation
- hotspot localization
- severity ranking

This forms the basis for:

- rule-based OPC
- model-based OPC
- hotspot repair flows

---

## 11. Learning Outcome of Day 11

After this exercise, the following concepts are clear:

- Why corners are intrinsically weak lithographic features
- How optics and resist chemistry combine to create hotspots
- Why EPE must be treated as a spatial field, not a scalar
- Why OPC must be geometry-aware

This is a fundamental insight required for computational lithography engineers.

---

## 12. Next Step

Next step is to analyze **more complex routing geometries** such as:

- jogs
- T-junctions
- multi-corner interactions

These patterns create interacting hotspot fields and are common in real IC
layouts.
