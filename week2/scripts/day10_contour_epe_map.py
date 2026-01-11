import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter
import plotly.graph_objects as go
import os

# ============================================================
# Path-safe results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day10_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Mask: isolated vertical line
# ============================================================
def isolated_line(nx, width=6, length=300):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c - length//2 : c + length//2, c - width//2 : c + width//2] = 1.0
    return img

# ============================================================
# Pupil -> PSF
# ============================================================
def circular_pupil(nx, radius):
    y, x = np.ogrid[-nx//2:nx//2, -nx//2:nx//2]
    return (x*x + y*y <= radius*radius).astype(float)

# ============================================================
# Sub-pixel edge extraction
# ============================================================
def find_edges_subpixel(profile, threshold):
    edges = []
    for i in range(len(profile) - 1):
        if (profile[i] - threshold) * (profile[i+1] - threshold) < 0:
            x = i + (threshold - profile[i]) / (profile[i+1] - profile[i])
            edges.append(x)
    return edges

# ============================================================
# Parameters
# ============================================================
nx = 512
pupil_radius = 60
focus_sigma = 1.5
dose = 1.0

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
develop_time = 1.0
resist_thickness = 0.55

# ============================================================
# Optical system
# ============================================================
mask = isolated_line(nx)

pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field)**2
psf /= psf.max()
psf = gaussian_filter(psf, sigma=focus_sigma)
psf /= psf.max()

aerial = fftconvolve(mask, psf, mode="same") * dose

# ============================================================
# Resist modeling
# ============================================================
M = np.exp(-C * aerial)
R = Rmax / (1 + (M / M0)**n)
clear = R * develop_time

# ============================================================
# Spatial EPE extraction along y
# ============================================================
center = nx // 2
target_left = center - 3
target_right = center + 3

ys = []
EPE_left = []
EPE_right = []

for y in range(100, nx - 100):
    profile = clear[y, :]
    edges = find_edges_subpixel(profile, resist_thickness)

    if len(edges) >= 2:
        epe_l = edges[0] - target_left
        epe_r = edges[1] - target_right
        ys.append(y)
        EPE_left.append(epe_l)
        EPE_right.append(epe_r)

# ============================================================
# Save clear depth map
# ============================================================
plt.figure(figsize=(5,5))
plt.title("Resist Clear Depth Map")
plt.imshow(clear, cmap="viridis")
plt.colorbar(label="Clear depth")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "clear_depth_map.png"))
plt.close()

# ============================================================
# EPE vs Y plots (matplotlib)
# ============================================================
plt.figure()
plt.plot(ys, EPE_left, label="Left Edge")
plt.plot(ys, EPE_right, label="Right Edge")
plt.axhline(0, linestyle="--")
plt.xlabel("Y position (pixels)")
plt.ylabel("EPE (pixels)")
plt.title("Spatial EPE Along Line")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "spatial_epe.png"))
plt.close()

# ============================================================
# Plotly interactive
# ============================================================
fig = go.Figure()
fig.add_trace(go.Scatter(x=ys, y=EPE_left, mode="lines", name="Left Edge"))
fig.add_trace(go.Scatter(x=ys, y=EPE_right, mode="lines", name="Right Edge"))
fig.add_hline(y=0, line_dash="dash")
fig.update_layout(
    title="Spatial EPE Along Printed Line",
    xaxis_title="Y position (pixels)",
    yaxis_title="EPE (pixels)"
)
fig.write_html(os.path.join(RESULTS_DIR, "spatial_epe_interactive.html"))

# ============================================================
# Save numeric data
# ============================================================
np.savetxt(
    os.path.join(RESULTS_DIR, "spatial_epe_values.txt"),
    np.column_stack((ys, EPE_left, EPE_right)),
    header="Y   EPE_left   EPE_right"
)

print("Day 10 contour EPE mapping completed.")
print("Results saved to:", RESULTS_DIR)
