# Day 3 — Aerial Image Formation and Optical Proximity Effects

## 1. Motivation: Why Aerial Image Matters

In photolithography, the wafer does not directly see the mask geometry.
Instead, light propagates through a projection optical system and forms an
optical intensity distribution at the wafer plane known as the **aerial image**.

All downstream steps (photoresist exposure, development, and etch) depend on
the shape and contrast of this aerial image. Therefore, accurate modeling of
the aerial image is the foundation of computational lithography and OPC.

Before modeling chemistry or etch, we must first understand how optics alone
distorts mask patterns.

---

## 2. Optical Imaging as a Linear System

Under scalar diffraction and partially coherent approximation, the imaging
system can be modeled as a linear spatial filtering system.

Let:
- M(x, y) be the mask transmission function
- PSF(x, y) be the point spread function of the optical system

Then the aerial image intensity is:

I(x, y) = M(x, y) ⊗ PSF(x, y)

where ⊗ denotes 2D convolution.

This means every point on the mask spreads into a blur spot defined by the PSF,
and the final image is the superposition of all such blurred contributions.

---

## 3. Physical Meaning of Point Spread Function (PSF)

The PSF represents how a point source on the mask is imaged by the projection
optics.

It is determined by:
- Numerical Aperture (NA)
- Wavelength
- Pupil shape

Mathematically, in Fourier optics:

PSF(x, y) = | IFFT{ Pupil(u, v) } |²

A larger pupil (higher NA) produces a tighter PSF, improving resolution.
A smaller pupil produces stronger diffraction blur.

Thus, PSF controls:
- Edge sharpness
- Feature spreading
- Interaction between nearby features

---

## 4. Origin of Optical Proximity Effects

When features are widely separated, their PSFs do not significantly overlap,
and they print independently.

When features are close:
- PSFs overlap
- Intensity between features increases
- Features may broaden, merge, or shift

This is known as **optical proximity effect**.

Importantly, proximity effects arise purely from optics, even before resist
chemistry is considered. OPC is fundamentally a correction for convolution
physics.

---

## 5. Simulation Setup

To study proximity effects, a simple two-line mask pattern was simulated.

### Mask
- Two vertical lines
- Finite spacing between them
- Binary transmission (0 or 1)

### Optical Model
- Circular pupil function
- PSF obtained using inverse FFT of pupil
- PSF normalized to unit peak

### Aerial Image
- Computed by FFT-based convolution:
  aerial = mask ⊗ PSF
- Result normalized for visualization

Script used:
- `scripts/day3_aerial.py`

---

## 6. Numerical Results

Saved files:
- `results/day3_mask.png` — original mask layout
- `results/day3_psf.png` — optical blur kernel
- `results/day3_aerial.png` — aerial image intensity
- `results/day3_profile.png` — horizontal intensity cross-section

### Observations

From the aerial image:
- Printed features appear wider than mask features
- Intensity between the two lines is non-zero
- Edge transitions are smooth, not abrupt

From the line profile:
- Peaks are rounded rather than rectangular
- Valley between peaks is elevated, indicating risk of bridging
- Edge slope is reduced, lowering resist contrast

These effects arise purely from diffraction and optical filtering.

---

## 7. Implications for OPC

Since the printed image is a convolution of the mask with the PSF, simply
shrinking or biasing features uniformly is insufficient.

Model-based OPC modifies mask geometry such that after optical convolution and
subsequent resist processing, the final printed contour matches design intent.

Therefore:
- Accurate aerial image models are mandatory
- PSF fidelity directly affects OPC accuracy
- Proximity effects must be predicted and corrected at the mask level

This simulation demonstrates the first stage of that pipeline.

---

## 8. Limitations of Current Model

This model includes only optical effects and ignores:
- Partial coherence source integration
- Photoresist chemistry
- Post-exposure diffusion
- Development kinetics

Therefore, aerial image alone cannot predict final resist contours, but it
defines the exposure distribution that drives all resist behavior.

---

## 9. Next Step

Next, photoresist threshold and chemical models will be applied to the aerial
image to obtain printed contours and critical dimensions.

This will allow direct measurement of CD error and edge placement error (EPE),
which are the primary metrics used in OPC verification.
