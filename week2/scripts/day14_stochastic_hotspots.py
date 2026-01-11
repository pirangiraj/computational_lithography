import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter, distance_transform_edt
import plotly.graph_objects as go
import os

# ============================================================
# Results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day14_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# T-junction pattern
# ============================================================
def t_junction(nx, width=8, arm=200):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c-arm//2:c+arm//2, c-width//2:c+width//2] = 1.0
    img[c-width//2:c+width//2, c:c+arm//2] = 1.0
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
nx = 512
pupil_radius = 60
focus_sigma = 1.5
dose = 1.0

# Photon statistics
photons_per_pixel = 2000  # controls noise strength

# Monte Carlo
N_trials = 40

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
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
# Pattern and nominal aerial image
# ============================================================
mask = t_junction(nx)
aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
aerial_nominal /= aerial_nominal.max()

# ============================================================
# Monte Carlo simulation
# ============================================================
worst_EPE_list = []

for trial in range(N_trials):

    # Photon shot noise (Poisson)
    photons = np.random.poisson(aerial_nominal * photons_per_pixel)
    aerial_noisy = photons / photons_per_pixel

    # Resist
    M = np.exp(-C * aerial_noisy)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time
    printed = clear > resist_thickness

    # EPE approx by distance fields
    dist_target = distance_transform_edt(~mask.astype(bool))
    dist_printed = distance_transform_edt(~printed)
    EPE_map = dist_printed - dist_target

    # ROI near junction
    c = nx // 2
    roi = 80
    roi_map = EPE_map[c-roi:c+roi, c-roi:c+roi]

    worst_EPE_list.append(np.nanmax(np.abs(roi_map)))

    # Save first few realizations
    if trial < 5:
        plt.figure(figsize=(4,4))
        plt.title(f"Printed Resist — Trial {trial}")
        plt.imshow(printed, cmap="gray")
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"printed_trial_{trial}.png"))
        plt.close()

# ============================================================
# Histogram of worst EPE
# ============================================================
plt.figure()
plt.hist(worst_EPE_list, bins=10)
plt.xlabel("Worst |EPE| (pixels)")
plt.ylabel("Count")
plt.title("Distribution of Worst EPE (Stochastic)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "worst_epe_histogram.png"))
plt.close()

# Plotly interactive
fig = go.Figure()
fig.add_trace(go.Histogram(x=worst_EPE_list, nbinsx=10))
fig.update_layout(title="Distribution of Worst EPE (Stochastic)",
                  xaxis_title="Worst |EPE|", yaxis_title="Count")
fig.write_html(os.path.join(RESULTS_DIR, "worst_epe_histogram_interactive.html"))

# ============================================================
# Save numeric data
# ============================================================
np.savetxt(
    os.path.join(RESULTS_DIR, "worst_epe_samples.txt"),
    np.array(worst_EPE_list),
    header="Worst EPE per Monte Carlo trial"
)

print("Day 14 stochastic hotspot simulation completed.")
print("Results saved to:", RESULTS_DIR)
