import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter
import plotly.graph_objects as go
import os

# ============================================================
# Results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day15_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Contact hole mask
# ============================================================
def contact_hole(nx, radius=6):
    y, x = np.ogrid[:nx, :nx]
    c = nx // 2
    return ((x - c)**2 + (y - c)**2 <= radius**2).astype(float)

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
focus_sigma = 1.5
dose = 1.0

# Photon statistics
photons_per_pixel = 1200

# Monte Carlo
N_trials = 80

# Dill
C = 1.3

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
# Mask and nominal aerial image
# ============================================================
mask = contact_hole(nx)
aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
aerial_nominal /= aerial_nominal.max()

# ============================================================
# Monte Carlo
# ============================================================
hole_open = []
hole_radius = []

for trial in range(N_trials):

    photons = np.random.poisson(aerial_nominal * photons_per_pixel)
    aerial_noisy = photons / photons_per_pixel

    M = np.exp(-C * aerial_noisy)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time

    printed = clear > resist_thickness

    # check hole opening at center
    c = nx // 2
    open_center = printed[c, c]

    hole_open.append(open_center)

    # estimate hole radius if open
    if open_center:
        profile = printed[c, :]
        idx = np.where(profile)[0]
        if len(idx) > 0:
            r = (idx[-1] - idx[0]) / 2
        else:
            r = 0
    else:
        r = 0

    hole_radius.append(r)

    if trial < 6:
        plt.figure(figsize=(4,4))
        plt.title(f"Printed Hole — Trial {trial}")
        plt.imshow(printed, cmap="gray")
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"printed_trial_{trial}.png"))
        plt.close()

# ============================================================
# Statistics
# ============================================================
hole_open = np.array(hole_open)
hole_radius = np.array(hole_radius)

open_prob = hole_open.mean()

# ============================================================
# Plots
# ============================================================
plt.figure()
plt.hist(hole_radius[hole_radius > 0], bins=10)
plt.xlabel("Printed Hole Radius (pixels)")
plt.ylabel("Count")
plt.title("Distribution of Open Hole Radius")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "hole_radius_distribution.png"))
plt.close()

plt.figure()
plt.bar(["Open", "Closed"], [hole_open.sum(), N_trials - hole_open.sum()])
plt.ylabel("Count")
plt.title("Hole Open vs Missing Events")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "hole_open_probability.png"))
plt.close()

# Plotly interactive
fig = go.Figure()
fig.add_trace(go.Histogram(x=hole_radius[hole_radius > 0], nbinsx=10))
fig.update_layout(title="Distribution of Open Hole Radius",
                  xaxis_title="Radius", yaxis_title="Count")
fig.write_html(os.path.join(RESULTS_DIR, "hole_radius_distribution_interactive.html"))

# ============================================================
# Save numeric results
# ============================================================
with open(os.path.join(RESULTS_DIR, "hole_statistics.txt"), "w") as f:
    f.write(f"Trials: {N_trials}\n")
    f.write(f"Open probability: {open_prob}\n")
    f.write(f"Missing probability: {1 - open_prob}\n")

print("Day 15 contact hole stochastic simulation completed.")
print("Open probability:", open_prob)
print("Results saved to:", RESULTS_DIR)
