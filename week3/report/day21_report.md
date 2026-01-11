# Day 21 — Transistor Variability Induced by Lithographic Roughness

## 1. Why Lithography Controls Device Variability

In modern CMOS, channel dimensions are comparable to:

- diffusion length
- depletion width
- electrostatic screening length

Thus small geometric variations strongly influence electrical behavior.

LER and LWR directly modulate effective channel length.

---

## 2. Channel Length Sensitivity

Drain current approximately follows:

Id ∝ (W/L) · (VGS − VT)^2

Thus:

ΔId / Id ≈ −ΔL / L

Even 2–3% variation in L produces large Id mismatch.

---

## 3. Vt Modulation by Geometry

Shorter channel increases:

- drain-induced barrier lowering (DIBL)
- effective gate control

Thus Vt decreases with decreasing L.

Therefore LER produces:

- correlated Id and Vt variations

---

## 4. Variability Propagation into Circuits

Variability impacts:

- SRAM cell stability
- logic delay variation
- analog mismatch

Hence lithography roughness is no longer a manufacturing-only issue but a circuit reliability problem.

---

## 5. Modeling Strategy Used

For each simulated transistor:

1. Stochastic resist profile is generated
2. Gate edges extracted row-wise
3. Mean effective channel length computed
4. Compact sensitivity model maps geometry to electrical parameters
5. Statistical distributions constructed

This approximates transistor population variability.

---

## 6. Observed Trends

Simulated devices show:

- L distribution from rough edges
- Id strongly correlated with L
- Vt distribution width

These trends agree qualitatively with experimental studies.

---

## 7. Design Implications

To manage variability:

- designers use larger channel lengths
- variability-aware design margins are required
- layout regularity reduces roughness impact

Thus DTCO must consider stochastic lithography effects.

---

## 8. Process Mitigation Strategies

Foundries reduce roughness by:

- increasing dose
- optimizing resist chemistry
- smoothing bake processes
- multiple patterning techniques

However tradeoffs exist between resolution, throughput, and variability.

---

## 9. Limitations of Educational Model

This model uses:

- simplified sensitivity relations

Real devices depend on:

- 3D electrostatics
- mobility degradation
- variability of dopants

Nevertheless the dominant link between LER and electrical mismatch is captured.

---

## 10. Key Learning Outcomes

After Day 21:

- lithography roughness directly maps to device variability
- circuit yield depends on pattern fidelity
- scaling is increasingly variability-limited

---

## 11. References

1. Taur & Ning, *Fundamentals of Modern VLSI Devices*
2. Mack, *Fundamental Principles of Optical Lithography*
3. Gallatin et al., SPIE stochastic roughness studies
4. IRDS Roadmap — Device Variability sections
