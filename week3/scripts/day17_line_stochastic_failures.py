
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter, label
import plotly.graph_objects as go
import os

# ============================================================
# Results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day17_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Two-line mask
# ============================================================
def two_lines(nx, width=6, spacing=20):
    img = np.zeros((nx, nx))
    c = nx // 2
    l = c - spacing//2
    r = c + spacing//2
    img[:, l-width//2:l+width//2] = 1.0
    img[:, r-width//2:r+width//2] = 1.0
    return img

# ============================================================
# Optical system
# ============================================================
def circular_pupil(nx, radius):
    y, x = np.ogrid[-nx//2:nx//2, -nx//2:nx//2]
    return (x*x + y*y <= radius*radius).astype(float)

# ============================================================
# Parameters
# ============================================================
nx = 256
pupil_radius = 45
focus_sigma = 1.2
dose = 1.0

# Photon statistics
photons_per_pixel = 1200

# Monte Carlo
N_trials = 60

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 3.0
develop_time = 1.0
resist_thickness = 0.55

# ============================================================
# PSF
# ============================================================
pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field)**2
psf /= psf.max()
psf = gaussian_filter(psf, sigma=focus_sigma)
psf /= psf.max()

# ============================================================
# Mask and nominal aerial
# ============================================================
mask = two_lines(nx)
aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
aerial_nominal /= aerial_nominal.max()

# ============================================================
# Monte Carlo simulation
# ============================================================
opens = 0
shorts = 0

for trial in range(N_trials):

    photons = np.random.poisson(aerial_nominal * photons_per_pixel)
    aerial_noisy = photons / photons_per_pixel

    M = np.exp(-C * aerial_noisy)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time
    printed = clear > resist_thickness

    # Label connected components
    structure = np.ones((3,3))
    labeled, num = label(printed, structure)

    # Expected: 2 separate lines
    if num < 2:
        shorts += 1
    else:
        # Check if any row is fully broken
        broken = False
        for y in range(nx):
            if printed[y].sum() == 0:
                broken = True
                break
        if broken:
            opens += 1

    if trial < 5:
        plt.figure(figsize=(4,4))
        plt.title(f"Printed Lines — Trial {trial}")
        plt.imshow(printed, cmap="gray")
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"printed_trial_{trial}.png"))
        plt.close()

# ============================================================
# Statistics
# ============================================================
open_prob = opens / N_trials
short_prob = shorts / N_trials

# ============================================================
# Plot
# ============================================================
plt.figure()
plt.bar(["Open", "Short", "Pass"], [opens, shorts, N_trials-opens-shorts])
plt.ylabel("Count")
plt.title("Stochastic Line Failure Outcomes")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "line_failure_statistics.png"))
plt.close()

fig = go.Figure()
fig.add_trace(go.Bar(x=["Open", "Short", "Pass"], y=[opens, shorts, N_trials-opens-shorts]))
fig.update_layout(title="Stochastic Line Failure Outcomes")
fig.write_html(os.path.join(RESULTS_DIR, "line_failure_statistics_interactive.html"))

# ============================================================
# Save stats
# ============================================================
with open(os.path.join(RESULTS_DIR, "line_failure_probabilities.txt"), "w") as f:
    f.write(f"Trials: {N_trials}\n")
    f.write(f"Open probability: {open_prob}\n")
    f.write(f"Short probability: {short_prob}\n")
    f.write(f"Pass probability: {1 - open_prob - short_prob}\n")

print("Day 17 stochastic line failure simulation completed.")
print("Open probability:", open_prob)
print("Short probability:", short_prob)
print("Results saved to:", RESULTS_DIR)
