import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter, distance_transform_edt
import plotly.graph_objects as go
import os

# ============================================================
# Path-safe results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day11_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Corner mask (L-shape)
# ============================================================
def corner_pattern(nx, width=8, arm=200):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c - width//2 : c + width//2, c : c + arm] = 1.0
    img[c : c + arm, c - width//2 : c + width//2] = 1.0
    return img

# ============================================================
# Pupil -> PSF
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

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
develop_time = 1.0
resist_thickness = 0.55

# ============================================================
# Optical imaging
# ============================================================
mask = corner_pattern(nx)

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

printed = clear > resist_thickness

# ============================================================
# Target geometry distance field
# ============================================================
target = mask.astype(bool)

dist_target = distance_transform_edt(~target)
dist_printed = distance_transform_edt(~printed)

# Signed distance approx (positive = shrink)
EPE_map = dist_printed - dist_target

# ============================================================
# Crop region near corner
# ============================================================
c = nx // 2
roi = 80
EPE_roi = EPE_map[c-10:c+roi, c-10:c+roi]

# ============================================================
# Save maps
# ============================================================
plt.figure(figsize=(5,5))
plt.title("Printed Resist (Binary)")
plt.imshow(printed, cmap="gray")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "printed_resist.png"))
plt.close()

plt.figure(figsize=(5,5))
plt.title("Corner EPE Map (ROI)")
plt.imshow(EPE_roi, cmap="RdBu")
plt.colorbar(label="EPE (pixels)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "corner_epe_map.png"))
plt.close()

# ============================================================
# Plotly interactive heatmap
# ============================================================
fig = go.Figure(data=go.Heatmap(
    z=EPE_roi,
    colorscale="RdBu",
    colorbar=dict(title="EPE (pixels)")
))
fig.update_layout(title="Corner Hotspot EPE Map (ROI)")
fig.write_html(os.path.join(RESULTS_DIR, "corner_epe_map_interactive.html"))

# ============================================================
# Worst EPE in ROI
# ============================================================
worst_epe = np.nanmax(np.abs(EPE_roi))

with open(os.path.join(RESULTS_DIR, "worst_corner_epe.txt"), "w") as f:
    f.write(f"Worst |EPE| near corner (pixels): {worst_epe}\n")

print("Day 11 corner hotspot analysis completed.")
print("Worst EPE near corner:", worst_epe)
print("Results saved to:", RESULTS_DIR)
