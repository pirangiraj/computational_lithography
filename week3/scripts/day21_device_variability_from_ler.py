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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day21_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Mask: gate pattern (two edges define channel length)
# ============================================================
def gate_mask(nx, width=12):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[:, c - width//2 : c + width//2] = 1.0
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
focus_sigma = 1.1
dose = 1.0

photons_per_pixel = 1000
N_devices = 80

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 3.0
develop_time = 1.0
resist_thickness = 0.55

# Device sensitivity model
L0 = 30.0        # nominal channel length (nm, conceptual)
Id0 = 1.0        # normalized drain current
alpha_L = 1.5    # Id sensitivity to L variation
beta_L = 0.8     # Vt sensitivity to L variation

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
# Nominal aerial image
# ============================================================
mask = gate_mask(nx)
aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
aerial_nominal /= aerial_nominal.max()

# ============================================================
# Monte Carlo device population
# ============================================================
channel_lengths = []
Id_values = []
Vt_values = []

for dev in range(N_devices):

    photons = np.random.poisson(aerial_nominal * photons_per_pixel)
    aerial_noisy = photons / photons_per_pixel

    M = np.exp(-C * aerial_noisy)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time
    printed = clear > resist_thickness

    # Extract gate edges row-wise
    left_edges = []
    right_edges = []

    for y in range(nx):
        row = printed[y]
        idx = np.where(row)[0]
        if len(idx) > 0:
            left_edges.append(idx[0])
            right_edges.append(idx[-1])

    if len(left_edges) < nx * 0.8:
        continue  # skip broken devices

    L_eff_pixels = np.mean(np.array(right_edges) - np.array(left_edges))

    # Convert pixel length to physical variation
    delta_L = (L_eff_pixels - np.mean(L_eff_pixels)) * 0.5

    L_device = L0 + delta_L

    # Simple sensitivity models
    Id = Id0 * (L0 / L_device) ** alpha_L
    Vt = 0.4 + beta_L * (L0 - L_device) / L0

    channel_lengths.append(L_device)
    Id_values.append(Id)
    Vt_values.append(Vt)

# ============================================================
# Convert to arrays
# ============================================================
channel_lengths = np.array(channel_lengths)
Id_values = np.array(Id_values)
Vt_values = np.array(Vt_values)

# ============================================================
# Statistics
# ============================================================
Id_sigma = np.std(Id_values)
Vt_sigma = np.std(Vt_values)

# ============================================================
# Plots
# ============================================================
plt.figure()
plt.hist(Id_values, bins=20)
plt.title("Drain Current Distribution")
plt.xlabel("Normalized Id")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "Id_distribution.png"))
plt.close()

plt.figure()
plt.hist(Vt_values, bins=20)
plt.title("Threshold Voltage Distribution")
plt.xlabel("Vt (a.u.)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "Vt_distribution.png"))
plt.close()

# Interactive scatter
fig = go.Figure()
fig.add_trace(go.Scatter(x=channel_lengths, y=Id_values, mode="markers",
                         name="Id vs L"))
fig.update_layout(title="Drain Current vs Channel Length",
                  xaxis_title="Channel Length",
                  yaxis_title="Drain Current")
fig.write_html(os.path.join(RESULTS_DIR, "Id_vs_L_interactive.html"))

# ============================================================
# Save summary
# ============================================================
with open(os.path.join(RESULTS_DIR, "device_variability.txt"), "w") as f:
    f.write(f"Number of devices: {len(Id_values)}\n")
    f.write(f"Id sigma: {Id_sigma}\n")
    f.write(f"Vt sigma: {Vt_sigma}\n")

print("Day 21 device variability simulation completed.")
print("Id sigma:", Id_sigma)
print("Vt sigma:", Vt_sigma)
print("Results saved to:", RESULTS_DIR)
