import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import plotly.graph_objects as go
import os

# ============================================================
# Path-safe results directory (week1/results/day6_results)
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_BASE = os.path.join(BASE_DIR, "results")
RESULTS_DIR = os.path.join(RESULTS_BASE, "day6_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Mask: two vertical lines
# ============================================================
def two_lines_mask(nx, line_width=6, spacing=30):
    img = np.zeros((nx, nx))
    center = nx // 2

    left = center - spacing // 2
    right = center + spacing // 2

    img[:, left - line_width // 2 : left + line_width // 2] = 1.0
    img[:, right - line_width // 2 : right + line_width // 2] = 1.0
    return img

# ============================================================
# Circular pupil -> PSF
# ============================================================
def circular_pupil(nx, radius):
    y, x = np.ogrid[-nx//2:nx//2, -nx//2:nx//2]
    mask = x*x + y*y <= radius*radius
    return mask.astype(float)

# ============================================================
# Simulation parameters
# ============================================================
nx = 512
pupil_radius = 60

# Dill parameters
C = 0.8
dose = 1.0

# Mack parameters
Rmax = 1.0
M0 = 0.5
n = 4
develop_time = 1.0
resist_thickness = 0.5

# ============================================================
# Optical imaging
# ============================================================
mask = two_lines_mask(nx, line_width=6, spacing=30)

pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field)**2
psf = psf / psf.max()

aerial = fftconvolve(mask, psf, mode="same")
aerial = aerial / aerial.max()

# ============================================================
# Dill exposure -> PAC concentration
# ============================================================
M = np.exp(-C * aerial * dose)

# ============================================================
# Mack development rate
# ============================================================
R = Rmax / (1 + (M / M0)**n)

# ============================================================
# Development to final resist pattern
# ============================================================
clear_depth = R * develop_time
printed = clear_depth > resist_thickness

# ============================================================
# Save Matplotlib images
# ============================================================
plt.figure(figsize=(4,4))
plt.title("Aerial Image")
plt.imshow(aerial, cmap="hot")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "aerial.png"))
plt.close()

plt.figure(figsize=(4,4))
plt.title("PAC Concentration (Dill Model)")
plt.imshow(M, cmap="viridis")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "pac.png"))
plt.close()

plt.figure(figsize=(4,4))
plt.title("Dissolution Rate (Mack Model)")
plt.imshow(R, cmap="plasma")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "rate.png"))
plt.close()

plt.figure(figsize=(4,4))
plt.title("Final Printed Resist")
plt.imshow(printed, cmap="gray")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "printed.png"))
plt.close()

# ============================================================
# Line profiles
# ============================================================
center = nx // 2
profile_I = aerial[center, :]
profile_M = M[center, :]
profile_R = R[center, :]

plt.figure()
plt.title("Optics → Chemistry → Development Profiles")
plt.plot(profile_I, label="Intensity")
plt.plot(profile_M, label="PAC")
plt.plot(profile_R, label="Rate")
plt.xlabel("Position (pixels)")
plt.ylabel("Normalized")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "profiles.png"))
plt.close()

# ============================================================
# Plotly interactive profile
# ============================================================
x = np.arange(len(profile_I))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=profile_I, mode="lines", name="Intensity"))
fig.add_trace(go.Scatter(x=x, y=profile_M, mode="lines", name="PAC"))
fig.add_trace(go.Scatter(x=x, y=profile_R, mode="lines", name="Rate"))

fig.update_layout(
    title="Optics → Chemistry → Development Profiles (Day 6)",
    xaxis_title="Position (pixels)",
    yaxis_title="Normalized Value"
)

fig.write_html(os.path.join(RESULTS_DIR, "profiles_interactive.html"))

# ============================================================
# CD Measurement (rough)
# ============================================================
row = printed[center, :].astype(int)
edges = np.where(np.diff(row) != 0)[0]

if len(edges) >= 2:
    cd_pixels = edges[1] - edges[0]
else:
    cd_pixels = None

with open(os.path.join(RESULTS_DIR, "cd_measurement.txt"), "w") as f:
    f.write(f"Estimated CD (pixels): {cd_pixels}\n")

print("Day 6 Mack development simulation completed.")
print("Results saved to:", RESULTS_DIR)
print("Estimated CD (pixels):", cd_pixels)
