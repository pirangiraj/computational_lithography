import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter
import plotly.graph_objects as go
import os

# ============================================================
# Paths
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day19_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Mask: Single long line
# ============================================================
def single_line(nx, width=8):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[:, c - width//2 : c + width//2] = 1.0
    return img

# ============================================================
# Optical pupil
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

photons_per_pixel = 1200
N_trials = 40

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
mask = single_line(nx)
aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
aerial_nominal /= aerial_nominal.max()

# ============================================================
# Storage (fixed-size with NaN)
# ============================================================
all_left_edges = np.full((N_trials, nx), np.nan)
all_right_edges = np.full((N_trials, nx), np.nan)

# ============================================================
# Monte Carlo simulation
# ============================================================
for trial in range(N_trials):

    photons = np.random.poisson(aerial_nominal * photons_per_pixel)
    aerial_noisy = photons / photons_per_pixel

    M = np.exp(-C * aerial_noisy)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time
    printed = clear > resist_thickness

    for y in range(nx):
        row = printed[y]
        idx = np.where(row)[0]
        if len(idx) > 0:
            all_left_edges[trial, y] = idx[0]
            all_right_edges[trial, y] = idx[-1]

    if trial < 5:
        plt.figure(figsize=(4,4))
        plt.title(f"Printed Line — Trial {trial}")
        plt.imshow(printed, cmap="gray")
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"printed_trial_{trial}.png"))
        plt.close()

# ============================================================
# Roughness statistics (ignore NaNs)
# ============================================================
mean_left = np.nanmean(all_left_edges, axis=0)
mean_right = np.nanmean(all_right_edges, axis=0)

LER_left = np.nanstd(all_left_edges - mean_left, axis=0)
LER_right = np.nanstd(all_right_edges - mean_right, axis=0)

widths = all_right_edges - all_left_edges
mean_width = np.nanmean(widths, axis=0)
LWR = np.nanstd(widths - mean_width, axis=0)

# ============================================================
# Plots
# ============================================================
plt.figure()
plt.plot(mean_left, label="Mean Left Edge")
plt.plot(mean_right, label="Mean Right Edge")
plt.title("Mean Edge Positions")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "mean_edges.png"))
plt.close()

plt.figure()
plt.plot(LER_left, label="Left Edge LER")
plt.plot(LER_right, label="Right Edge LER")
plt.title("Line Edge Roughness (LER)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "LER_profile.png"))
plt.close()

plt.figure()
plt.plot(LWR)
plt.title("Line Width Roughness (LWR)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "LWR_profile.png"))
plt.close()

# ============================================================
# Plotly interactive
# ============================================================
fig = go.Figure()
fig.add_trace(go.Scatter(y=LWR, mode="lines", name="LWR"))
fig.update_layout(
    title="Line Width Roughness vs Position",
    xaxis_title="Position along line",
    yaxis_title="LWR (pixels)"
)
fig.write_html(os.path.join(RESULTS_DIR, "LWR_profile_interactive.html"))

# ============================================================
# Save summary
# ============================================================
with open(os.path.join(RESULTS_DIR, "roughness_summary.txt"), "w") as f:
    f.write(f"Mean LER left: {np.nanmean(LER_left)}\n")
    f.write(f"Mean LER right: {np.nanmean(LER_right)}\n")
    f.write(f"Mean LWR: {np.nanmean(LWR)}\n")

print("Day 19 LER/LWR simulation completed.")
print("Results saved to:", RESULTS_DIR)
