# Day 20 — Roughness Power Spectral Density (PSD) and Correlation Length

## 1. Why RMS Roughness Is Not Sufficient

Traditional roughness metrics such as RMS LER provide only a single number.

However, two edges can have:
- identical RMS roughness
- completely different spatial structures

Device sensitivity depends on spatial scale of variation, not just magnitude.

Thus frequency-domain analysis is required.

---

## 2. Spatial Frequency Interpretation

Edge position varies along line length.

This variation can be decomposed into:
- slow variations (low frequency)
- fast variations (high frequency)

Low-frequency roughness affects:
- effective channel length
- electrostatic control

High-frequency roughness tends to average out electrically.

---

## 3. Power Spectral Density (PSD)

PSD describes how roughness energy is distributed over spatial frequencies.

Computed by:
1. subtract mean edge
2. Fourier transform
3. square magnitude

PSD allows comparison of resist processes independent of RMS value.

---

## 4. Physical Meaning of PSD Shape

PSD slope and cutoff frequency reflect:

- optical smoothing (PSF)
- acid diffusion length
- polymer chain mobility

Thus PSD shape contains information about resist chemistry and process conditions.

---

## 5. Correlation Length

Correlation length represents:

typical size of roughness features

Estimated from:
- autocorrelation decay
- or inverse PSD bandwidth

Large correlation length:
- long smooth waves
- greater impact on transistor variability

Small correlation length:
- fine random noise

---

## 6. Autocorrelation Analysis

Autocorrelation measures:

how similar edge position is to itself after shifting

When correlation drops to 1/e:
- structure is no longer related

This defines correlation length scale.

---

## 7. Industrial Relevance

Foundries characterize resists by:

- PSD curves
- correlation length
- low-frequency roughness suppression

Design-technology co-optimization depends on:

matching layout pitch to roughness spectrum.

---

## 8. Connection to Device Variability

LER causes:
- Vt variation
- drive current mismatch
- SRAM stability issues

Low-frequency roughness is most damaging.

Thus roughness engineering is critical for advanced nodes.

---

## 9. Limitations of Educational Model

This model includes:

- photon shot noise

But excludes:

- acid diffusion stochasticity
- quencher effects
- polymer chain statistics

However, optical smoothing and chemical amplification already produce realistic PSD shapes.

---

## 10. Key Learning Outcomes

After Day 20:

- roughness must be studied in frequency domain
- correlation length matters more than RMS alone
- lithography, chemistry, and device physics are linked

---

## 11. References

1. C. A. Mack, *Fundamental Principles of Optical Lithography*
2. Levinson, *Principles of Lithography*
3. Gallatin et al., "Impact of line-edge roughness on transistor performance"
4. Erdmann et al., "Stochastic effects and PSD analysis in EUV resists"
5. IRDS Roadmap — Variability and Metrology chapters
