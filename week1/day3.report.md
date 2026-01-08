# Day 3 — Aerial Image Simulation and Optical Proximity Effects

## Objective
To generate aerial images by convolving mask layouts with the optical Point Spread
Function (PSF) and to observe proximity effects caused by diffraction.

## Theory Summary
In projection lithography, the aerial image represents the optical intensity
distribution formed on the wafer plane before photoresist exposure.

The aerial image is computed as a convolution of the mask transmission function with
the system PSF:

I(x,y) = M(x,y) ⊗ PSF(x,y)

Due to diffraction, each mask point spreads into a blur spot, and neighboring features
interact through overlapping PSFs, producing proximity effects.

## Implementation Details
- Mask pattern: two vertical lines with controlled spacing
- PSF generated from circular pupil using Fourier optics
- Aerial image computed using FFT-based convolution
- All images normalized to maximum intensity

Script used:
- `scripts/day3_aerial.py`

## Observations
- Printed features are wider than mask dimensions due to optical blur.
- Intensity between adjacent lines is non-zero, indicating proximity interaction.
- Line profiles show smooth peaks instead of square profiles, reducing edge sharpness.

## Results
Saved images:
- `results/day3_mask.png`
- `results/day3_psf.png`
- `results/day3_aerial.png`
- `results/day3_profile.png`

These clearly demonstrate optical proximity effects prior to resist modeling.

## Relevance to OPC Engineering
OPC modifies mask shapes so that after convolution with the optical system, the aerial
image edges align with intended design targets. Accurate aerial image modeling is the
foundation of model-based OPC and lithography verification flows.

## Next Step
Introduce photoresist models to convert aerial images into final printed contours and
study how resist chemistry further modifies feature shapes.
