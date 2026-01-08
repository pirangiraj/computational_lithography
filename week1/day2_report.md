# Day 2 — Diffraction and Point Spread Function (PSF)

## Objective
To understand how optical diffraction limits resolution by simulating the
Point Spread Function (PSF) using Fourier optics.

## Theory Summary
In projection lithography, the imaging system acts as a low-pass filter.
The pupil function represents the aperture of the optical system, and the
PSF is obtained by taking the inverse Fourier transform of the pupil and
squaring the magnitude of the field.

Larger pupil radius (higher NA) leads to tighter PSF and better resolution.

## Implementation Details
- Simulation grid: 512 × 512
- Pupil: circular aperture with different radii
- PSF = |IFFT(pupil)|², normalized

Scripts used:
- `scripts/day2_psf.py`

## Observations
- Small pupil radius produced a wide blur spot.
- Larger pupil radius produced a sharper central peak.
- PSF line profiles clearly showed reduced spread with increasing radius.

## Results
Saved files:
- `results/psf_profile_r100.png`
- `results/psf_profile_r60.png`
- `results/psf_profile_r30.png`

## Relevance to OPC Engineering
PSF defines how mask features spread on the wafer and directly causes
proximity effects such as line broadening and corner rounding.
Understanding PSF behavior is fundamental for model-based OPC correction.

## Next Step
Convolve PSF with layout patterns to generate aerial images and observe
optical proximity effects.
