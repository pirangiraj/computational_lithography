# Day 12 — Jog and T-Junction Hotspot Clusters in Lithography

## 1. Why Routing Geometries Are Hard to Print

In real IC layouts, most wires are not straight. Routing introduces:

- jogs (direction changes)
- T-junctions (branch points)
- intersections

These geometries create strong local optical and chemical interactions.
Even if straight lines and simple corners print well, routing structures often
fail first.

Therefore, OPC verification places strong emphasis on routing hotspot detection.

---

## 2. Optical Superposition at Junctions

Each edge of a pattern acts as a diffraction source.

At straight lines:
- diffraction is approximately one-dimensional

At junctions:
- multiple edges diffract simultaneously
- interference redistributes energy unpredictably

This produces:
- local intensity minima
- reduced aerial image slope
- spatially varying contrast

Thus, junctions inherently weaken image fidelity.

---

## 3. Chemical Amplification of Optical Errors

The Dill model converts intensity to chemical state:

M(x, y) = exp(−C · I(x, y))

So small intensity variations become large PAC differences.

At junctions:
- local intensity minima create chemically resistant regions
- development slows locally
- edges retract asymmetrically

This amplifies optical proximity effects into geometric distortions.

---

## 4. Development Front Interactions

Development is not static thresholding.

Development fronts propagate from all sides of features.

At junctions:
- multiple fronts approach each other
- dissolution becomes competition between fronts
- shape evolution becomes asymmetric

This causes:
- necking
- corner erosion
- line-end pullback

These effects cannot be corrected by global bias.

---

## 5. Simulation Pipeline Used

Each geometry is processed through:

1. Mask generation
2. Optical convolution with defocused PSF
3. Dill exposure chemistry
4. Mack dissolution kinetics
5. Clear depth calculation
6. Binary resist extraction
7. Distance-based EPE estimation

Thus, optical, chemical, and kinetic effects are all included.

---

## 6. Visualization Strategy

For each geometry, the following maps are visualized:

- Aerial image → optical distortions
- PAC map → chemical gradients
- Clear depth → kinetic effects
- Printed resist → final geometry
- EPE map → deviation from target

This layered visualization helps trace:
cause → effect → failure location

---

## 7. Hotspot Severity Comparison

Worst-case EPE near the center region is extracted for each geometry.

Results typically show:

Straight line < Jog < T-junction

Meaning junctions produce the strongest local lithographic failures.

This matches industrial hotspot libraries used in OPC verification.

---

## 8. Why OPC Must Be Geometry-Aware

Since different geometries fail differently:

- one correction does not fit all
- model-based OPC must adapt locally

Modern OPC flows use:

- pattern matching
- fragment-based correction
- model-based contour optimization

Routing junctions receive special correction shapes.

---

## 9. Limitations of This Educational Model

This model does not include:

- vector polarization
- flare
- acid diffusion and post-exposure bake
- stochastic photon noise

However, dominant interactions between:

- diffraction
- chemical amplification
- development kinetics

are captured correctly, making geometric sensitivity realistic.

---

## 10. Learning Outcome of Day 12

After this exercise, it should be clear that:

- lithographic failure is highly geometry-dependent
- routing structures dominate hotspot statistics
- OPC is fundamentally a geometric correction problem, not just biasing

Understanding this is essential for computational lithography roles.

---

## 11. Next Step

Next step is to combine:

- geometry dependence
- process window dependence

to identify patterns that fail only under specific dose–focus conditions.

This leads to **conditional hotspots**, which are the hardest to detect.
