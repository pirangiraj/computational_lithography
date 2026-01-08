# Day 1 — Mask Rasterization and Sampling Effects

## Objective
To understand how continuous layout geometries are converted into discrete pixel grids
for numerical simulation, and how sampling resolution affects edge representation in
computational lithography.

## Theory Summary
In lithography simulation, mask layouts described by polygons must be rasterized into
uniform grids before optical modeling. This discretization introduces sampling effects
that can distort edges and feature dimensions if the grid resolution is insufficient.

Higher grid resolution reduces stair-stepping artifacts and improves edge fidelity,
but increases computational cost. Therefore, choosing appropriate pixel size is a key
trade-off between accuracy and runtime in OPC and verification flows.

## Implementation Details
- Binary mask generation using NumPy
- Vertical line feature centered in the simulation grid
- Grid resolutions tested: 64×64, 128×128, 256×256, 512×512

Script used:
- `scripts/day1_sampling.py`

## Observations
- At low resolution (64×64), edges show strong stair-step artifacts.
- Increasing resolution produces smoother edges and more accurate feature width.
- Feature shape becomes more faithful to the intended geometry as sampling improves.

## Results
Saved mask images:
- `results/mask_64.png`
- `results/mask_128.png`
- `results/mask_256.png`
- `results/mask_512.png`

These demonstrate how grid discretization directly affects layout fidelity in simulation.

## Relevance to OPC Engineering
OPC corrections rely on accurate simulation of edge placement and feature dimensions.
If rasterization is too coarse, the model may predict incorrect proximity effects and
lead to poor correction strategies. Therefore, grid selection is fundamental to reliable
OPC recipe development and verification.

## Next Step
Introduce diffraction effects through Fourier optics by computing the Point Spread
Function (PSF) of the optical system and studying resolution limits.
