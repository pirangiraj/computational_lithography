# Day 18 — Pitch Dependence of Stochastic Line Failures

## 1. Why Pitch Determines Manufacturability

Pitch controls the spacing between neighboring features.

As pitch decreases:
- optical interference increases
- aerial image contrast decreases
- separation margin shrinks

Thus pitch directly controls sensitivity to stochastic noise.

This is why design rules are usually pitch-limited, not CD-limited.

---

## 2. Optical Contrast and Image Slope

Line separation depends on:

- peak-to-valley contrast
- slope of aerial image between lines

At small pitch:
- diffraction orders overlap
- valleys fill in
- slope becomes shallow

Shallow slope means:
small noise → large edge movement → topology change.

---

## 3. Chemical Amplification at Small Pitch

PAC concentration:

M = exp(−C · I)

So small valley intensity changes at small pitch become:

- large PAC fluctuations
- strong variation in dissolution rate

Thus stochastic chemistry is stronger for dense patterns.

---

## 4. Competing Failure Modes

Two failure modes exist simultaneously:

Open:
- peak intensity drops
- line thins and breaks

Short:
- valley intensity rises
- gap clears and bridges

At very small pitch, bridging dominates.
At intermediate pitch, both can occur.

---

## 5. Monte Carlo Modeling Strategy

For each pitch:

1. Two-line mask generated
2. Optical image computed
3. Photon noise added
4. Resist exposure and development modeled
5. Printed topology analyzed
6. Open and short events counted

Repeating this estimates failure probabilities.

---

## 6. Interpretation of Results

Failure probability increases sharply below certain pitch.

This pitch corresponds to:

stochastic resolution limit

which is stricter than optical resolution limit.

Thus scaling is limited by yield, not imaging physics.

---

## 7. Connection to Design Rules

Foundries choose minimum pitch such that:

P(open) and P(short) < allowable defect rate

Design rules are therefore yield-driven constraints.

This explains why:

improved optics alone does not guarantee tighter design rules.

---

## 8. Industrial Relevance

Routing layers are usually pitch-limited by stochastic yield.

Advanced nodes use:

- larger pitch
- multiple patterning
- alternative patterning strategies

to reduce stochastic failure probability.

---

## 9. Limitations of the Educational Model

This model includes:

- photon shot noise

but excludes:

- acid diffusion stochasticity
- quencher noise
- polymer statistics

Nevertheless, dominant pitch-dependent trends are captured.

---

## 10. Key Learning Outcomes

After this exercise, it should be clear that:

- yield limits scaling before optics does
- pitch controls stochastic sensitivity
- design rules are statistical constraints

This is fundamental to understanding advanced-node layout rules.

---

## 11. References for Further Study

1. C. A. Mack, *Fundamental Principles of Optical Lithography*
2. H. J. Levinson, *Principles of Lithography*
3. Erdmann et al., "Stochastic effects in EUV lithography", SPIE
4. Gallatin et al., "Photon shot noise and pattern collapse"
5. IRDS Roadmap — Lithography and Patterning Chapters

These discuss both theoretical and experimental limits of stochastic scaling.
