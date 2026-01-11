# Day 10 — Spatial Edge Placement Error (EPE) Along Printed Contours

## 1. Why We Must Look Beyond Single-Point Measurements

In earlier days, edge placement error (EPE) was measured at only one or two
locations along a printed line. While this gives some information about global
CD shift, it does not capture local distortions such as:

- line-end pullback
- corner rounding
- necking in narrow regions

In real semiconductor layouts, failures usually occur at **localized regions**
rather than uniformly along the entire edge. Therefore, OPC verification tools
analyze EPE along the full contour of printed features.

This day introduces spatial EPE analysis, where edge error is measured as a
function of position along the feature.

---

## 2. From Aerial Image to Resist Surface

Lithography simulation proceeds through several physical stages:

### 2.1 Optical Imaging

The mask pattern is convolved with the optical point-spread function (PSF) to
produce the aerial image:

I(x, y) = Mask ⊗ PSF

Defocus is modeled as additional blur applied to the PSF, which reduces image
contrast and edge slope.

---

### 2.2 Exposure Chemistry (Dill Model)

Exposure converts photoactive compound (PAC) according to:

M(x, y) = exp(-C · I(x, y))

Where:
- M is normalized PAC concentration
- C is resist sensitivity parameter

Regions receiving more light experience greater PAC depletion (bleaching).

---

### 2.3 Development Kinetics (Mack Model)

Development rate depends on PAC concentration:

R(M) = Rmax / (1 + (M / M0)^n)

Low PAC → fast dissolution  
High PAC → slow dissolution

After development time T:

Clear depth:
D(x, y) = R(M(x, y)) · T

This clear depth is a **continuous surface**, not a binary pattern.

---

## 3. What Defines the Printed Contour

The printed resist boundary is defined by:

D(x, y) = resist_thickness

This is a contour (level set) of the clear-depth surface.

Therefore, edge locations should be extracted from the continuous depth map,
not from thresholded binary images.

Binary thresholding would quantize edges to pixel boundaries and destroy
process sensitivity.

---

## 4. Sub-Pixel Edge Extraction

To locate edges accurately:

1. Take a horizontal slice of D(x, y) at fixed y
2. Find where the profile crosses resist_thickness
3. Interpolate between pixels to obtain sub-pixel edge location

This allows continuous edge movement when dose, focus, or geometry changes.

Mathematically, for neighboring pixels i and i+1:

x_edge = i + (d - D[i]) / (D[i+1] - D[i])

Where d is resist thickness.

---

## 5. Spatial EPE Along the Feature

For many y-locations along the printed line:

- left and right edges are extracted
- EPE is computed relative to target mask edges

This produces:

EPE_left(y) and EPE_right(y)

Which reveal where along the line the lithographic process is most sensitive.

---

## 6. Results

Saved in:
- `results/day10_results/`

Files:

- `clear_depth_map.png`  
  Continuous resist dissolution surface after development.

- `spatial_epe.png`  
  EPE plotted as a function of position along the line.

- `spatial_epe_interactive.html`  
  Interactive Plotly version of spatial EPE distribution.

- `spatial_epe_values.txt`  
  Numeric EPE data for further analysis.

---

## 7. How to Interpret the Plots

### Clear Depth Map

- Central region of line shows uniform clearing
- Ends of the line show rounded contours and weaker development

This reflects optical diffraction and reduced image slope near line ends.

---

### Spatial EPE Plot

- In the middle of the line, EPE is nearly constant
- Near line ends, EPE deviates strongly
- These deviations correspond to hotspot regions

Thus, even if average CD is acceptable, localized failures may occur.

---

## 8. Why This Matters for OPC Verification

OPC verification does not simply check average CD.
It evaluates:

- worst-case local EPE
- sensitivity to process variation
- geometry-dependent failure risk

Spatial EPE analysis enables:

- hotspot detection
- targeted OPC correction
- design rule optimization

This is why contour-based verification is mandatory for advanced nodes.

---

## 9. Model Limitations and What Is Missing

This model uses:

- scalar optics
- Gaussian defocus approximation
- no acid diffusion or post-exposure bake

Industrial tools also include:

- vector electromagnetic imaging
- resist diffusion and PEB chemistry
- calibrated material parameters

However, the **structure of the physics and verification logic is correct**, and
the mechanisms responsible for hotspot formation are accurately represented.

---

## 10. Skills Developed on Day 10

By completing this day, the following competencies are practiced:

- continuous resist modeling
- sub-pixel contour extraction
- spatial EPE metrics
- hotspot interpretation

These are core skills for computational lithography and OPC verification roles.

---

## 11. Next Step

Next, spatial EPE mapping will be extended to 2D geometries such as corners and
jogs to visualize hotspot clusters around layout features.

