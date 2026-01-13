# Day 22 — Impact of OPC on Stochastic Variability

## 1. Purpose of OPC

Optical Proximity Correction (OPC) modifies mask geometry so that after optical distortion, wafer patterns match design intent.

OPC compensates for:

- diffraction blur
- corner rounding
- line shortening

It is a deterministic image correction technique.

---

## 2. How OPC Improves Image Fidelity

OPC introduces:

- serifs
- assist features
- edge biasing

These increase high spatial frequency content of the mask, improving:

- aerial image slope
- edge placement accuracy

Higher slope reduces deterministic EPE.

---

## 3. Photon Statistics and Energy Concentration

Photon noise scales as:

σ ∝ √N

Relative noise:

σ/N ∝ 1/√N

When OPC concentrates intensity into smaller regions:

- fewer photons contribute locally
- relative noise increases

Thus stochastic variability can increase.

---

## 4. Competing Objectives

OPC improves:

- mean CD accuracy
- contour fidelity

But may worsen:

- LER
- stochastic defect probability

Therefore OPC optimization must balance:

deterministic accuracy vs stochastic robustness.

---

## 5. Simulation Strategy

Two mask cases are compared:

1. Plain line mask
2. OPC-enhanced mask with serifs

For each case:

- aerial image computed
- photon noise added
- resist development simulated
- slope and width variability measured

---

## 6. Observed Trends

OPC increases average image slope, confirming improved optical fidelity.

However width variability may not reduce and can increase depending on photon statistics.

This demonstrates fundamental tradeoff between sharpening and noise amplification.

---

## 7. Industrial Implications

Modern OPC tools include stochastic cost functions such as:

- local photon density
- LER prediction
- defect probability metrics

This field is called stochastic-aware OPC.

---

## 8. Design-Technology Co-Optimization (DTCO)

Layouts are modified to:

- reduce extreme OPC features
- favor regular patterns

Thus layout and OPC are co-optimized to reduce variability.

---

## 9. Why This Limits Scaling

As feature size shrinks:

- OPC complexity increases
- stochastic effects worsen

Thus scaling becomes limited by stochastic noise, not optical resolution.

---

## 10. Key Learning Outcomes

After Day 22:

- OPC is not purely beneficial
- variability must be co-optimized
- manufacturing yield and design are tightly coupled

---

## 11. References

1. C. A. Mack, *Fundamental Principles of Optical Lithography*
2. Erdmann et al., SPIE stochastic OPC studies
3. Gallatin et al., stochastic effects in EUV lithography
4. IRDS Roadmap — Patterning and Variability chapters
