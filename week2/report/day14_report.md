# Day 14 — Stochastic Hotspots and Variability in Lithography

## 1. Why Deterministic Models Are Not Enough

Deterministic lithography models assume:

- continuous intensity
- continuous chemistry
- continuous development

But in reality, lithography is governed by discrete events:

- individual photons
- discrete acid molecules
- polymer chain reactions

Thus identical process conditions can produce different printed results.

This randomness creates stochastic defects that cannot be predicted by
deterministic models alone.

---

## 2. Photon Shot Noise

Photon arrival follows Poisson statistics:

Variance = Mean

So relative noise is:

σ / N = 1 / sqrt(N)

At EUV wavelengths:

- photon energy is high
- photon count per pixel is low

Therefore shot noise is significant and directly perturbs local exposure.

---

## 3. Chemical Amplification of Noise

Exposure noise is converted to PAC variation:

M = exp(−C · I)

Because of exponential response, small intensity noise becomes large chemical
noise.

Then development rate:

R = Rmax / (1 + (M / M0)^n)

further amplifies PAC fluctuations into geometric variability.

Thus stochasticity compounds through the resist process.

---

## 4. Monte Carlo Simulation Approach

Stochastic behavior must be simulated statistically.

Each Monte Carlo trial represents one hypothetical wafer exposure with:

- random photon noise
- independent chemical outcome

By repeating many trials, we estimate:

- probability of large EPE
- distribution of failure severity

Yield risk corresponds to the tail of this distribution.

---

## 5. Simulation Pipeline Used

For each trial:

1. Nominal aerial image computed
2. Poisson noise added to represent photon statistics
3. Dill exposure applied to noisy intensity
4. Mack development applied to chemical state
5. Printed geometry extracted
6. Worst EPE near junction measured

Repeating this yields statistical EPE samples.

---

## 6. Interpretation of Results

Printed patterns differ slightly across trials even under identical conditions.

Histogram of worst EPE shows:

- broad distribution
- rare but severe events

These rare events dominate manufacturing yield loss.

Thus lithography must be evaluated probabilistically, not deterministically.

---

## 7. Industrial Significance

Modern EUV verification flows evaluate:

- probability of missing features
- probability of bridges
- defect density metrics

This is called **stochastic defect modeling** and is a major research topic in
advanced nodes.

Foundries impose stricter design rules to reduce stochastic sensitivity.

---

## 8. Why OPC Alone Cannot Fix Stochastic Defects

OPC can correct systematic errors:

- bias
- corner rounding
- proximity effects

But OPC cannot fix random events:

- photon fluctuations
- molecular randomness

Thus process improvements and resist chemistry are equally important.

---

## 9. Limitations of This Educational Model

This model includes:

- photon shot noise

But does not include:

- acid diffusion noise
- quencher statistics
- polymer chain variability

However, photon noise alone is sufficient to demonstrate:

- random geometry fluctuations
- distribution-based failure analysis

Which is the key conceptual point.

---

## 10. Learning Outcome of Day 14

After this exercise, it should be clear that:

- lithography yield is statistical
- rare events dominate defectivity
- deterministic models are insufficient for EUV

This is why modern lithography modeling increasingly relies on stochastic
simulation and machine learning.

---

## 11. Next Step

Next step is to study **contact holes and via stochastic failure**, which is one
of the most severe yield limiters in EUV lithography.
