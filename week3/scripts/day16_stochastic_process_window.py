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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day16_results")
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

# Process sweep
doses = np.linspace(0.8, 1.3, 8)
focus_vals = np.linspace(0.0, 2.5, 8)

# Photon statistics
photons_per_pixel_base = 1200

# Monte Carlo per point
N_trials = 25

# Dill
C = 1.3

# Mack
Rmax = 1.0
M0 = 0.5
n = 3.0
develop_time = 1.0
resist_thickness = 0.55

# ============================================================
# PSF nominal
# ============================================================
pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf_nominal = np.abs(field)**2
psf_nominal /= psf_nominal.max()

# ============================================================
# Mask
# ============================================================
mask = contact_hole(nx)

# ============================================================
# Stochastic process window sweep
# ============================================================
open_prob_map = np.zeros((len(focus_vals), len(doses)))

for i, f in enumerate(focus_vals):

    psf = gaussian_filter(psf_nominal, sigma=f)
    psf /= psf.max()

    for j, dose in enumerate(doses):

        aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
        aerial_nominal /= aerial_nominal.max()

        photons_per_pixel = photons_per_pixel_base * dose

        opens = 0

        for _ in range(N_trials):

            photons = np.random.poisson(aerial_nominal * photons_per_pixel)
            aerial_noisy = photons / photons_per_pixel

            M = np.exp(-C * aerial_noisy)
            R = Rmax / (1 + (M / M0)**n)
            clear = R * develop_time
            printed = clear > resist_thickness

            c = nx // 2
            if printed[c, c]:
                opens += 1

        open_prob_map[i, j] = opens / N_trials

# ============================================================
# Heatmap (matplotlib)
# ============================================================
plt.figure(figsize=(6,5))
plt.imshow(
    open_prob_map,
    origin="lower",
    extent=[doses[0], doses[-1], focus_vals[0], focus_vals[-1]],
    aspect="auto",
    cmap="viridis"
)
plt.colorbar(label="Hole Open Probability")
plt.xlabel("Dose")
plt.ylabel("Focus (blur sigma)")
plt.title("Stochastic Process Window — Contact Hole")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "stochastic_process_window.png"))
plt.close()

# ============================================================
# Plotly interactive
# ============================================================
fig = go.Figure(data=go.Heatmap(
    z=open_prob_map,
    x=doses,
    y=focus_vals,
    colorscale="Viridis",
    colorbar=dict(title="Open Probability")
))
fig.update_layout(
    title="Stochastic Process Window — Contact Hole",
    xaxis_title="Dose",
    yaxis_title="Focus (blur sigma)"
)
fig.write_html(os.path.join(RESULTS_DIR, "stochastic_process_window_interactive.html"))

# ============================================================
# Save numeric data
# ============================================================
np.savetxt(
    os.path.join(RESULTS_DIR, "open_probability_map.txt"),
    open_prob_map,
    header="Rows=Focus, Cols=Dose"
)

print("Day 16 stochastic process window simulation completed.")
print("Results saved to:", RESULTS_DIR)
