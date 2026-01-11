# Day 19 — Line Edge Roughness (LER) and Line Width Roughness (LWR)

## 1. Why Roughness Matters Even When Patterns Do Not Fail

Lithography is often evaluated by:

- critical dimension (CD)
- defectivity (opens/shorts)

However, even when no topological defects exist, rough edges create:

- transistor variability
- timing uncertainty
- leakage variation

Thus LER and LWR directly impact circuit performance and yield.

---

## 2. Definitions

Line Edge Roughness (LER):
Standard deviation of edge position along line length.

Line Width Roughness (LWR):
Standard deviation of line width along line length.

Since width = right edge − left edge:

LWR depends on correlation between edges.

---

## 3. Physical Origins of Roughness

### Photon Shot Noise

Local exposure fluctuates due to discrete photons.

### Chemical Amplification

PAC generation is exponential in intensity.

Small intensity noise becomes large chemical variation.

### Development Front Instability

Dissolution proceeds unevenly due to:

- PAC gradients
- polymer chain randomness

Front position becomes noisy, creating rough edges.

---

## 4. Correlation Length of Roughness

Roughness is not independent at each location.

Spatial smoothing comes from:

- optical PSF
- diffusion during post-exposure bake
- developer transport

Thus roughness exhibits correlation length, not white noise.

This correlation length affects device variability.

---

## 5. Simulation Approach Used

For each Monte Carlo trial:

1. Aerial image computed
2. Photon shot noise added
3. Dill exposure applied
4. Mack development applied
5. Printed resist extracted
6. Left and right edges located for each row
7. Edge statistics computed across trials

This mimics experimental roughness measurement.

---

## 6. Interpretation of Results

LER profiles show spatial variation of edge stability.

LWR profiles show local width variability.

Mean LER and LWR represent global roughness severity.

---

## 7. Impact on Device Performance

Roughness causes:

- gate length variability
- threshold voltage variation
- drain current mismatch

This degrades:

- SRAM stability
- logic timing margins

Thus LER is now treated as a device variability problem, not only a lithography problem.

---

## 8. Industry Mitigation Strategies

To reduce roughness:

- increase exposure dose
- improve resist chemistry
- introduce smoothing bake steps
- use alternative patterning schemes

However, all involve tradeoffs with resolution and throughput.

---

## 9. Limitations of This Model

This model includes:

- photon shot noise

But excludes:

- acid diffusion stochasticity
- quencher variability
- polymer chain statistics

Nevertheless, it captures fundamental origin of edge variability.

---

## 10. Key Learning Outcomes

After this exercise:

- roughness is seen as statistical, not geometric
- yield loss can occur without visible defects
- lithography and device physics are tightly coupled

---

## 11. References

1. C. A. Mack, *Fundamental Principles of Optical Lithography*
2. H. J. Levinson, *Principles of Lithography*
3. Gallatin et al., "Line-edge roughness and its impact on device variability"
4. Erdmann et al., "Stochastic modeling of EUV resist processes"
5. IRDS Roadmap — Variability and Lithography chapters

These discuss both modeling and experimental measurements of roughness.
