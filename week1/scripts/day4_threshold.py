import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import plotly.graph_objects as go
import os

# ============================================================
# Path-safe results directory (always week1/results)
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
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
threshold = 0.35

# ============================================================
# Generate mask and PSF
# ============================================================
mask = two_lines_mask(nx, line_width=6, spacing=30)

pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field) ** 2
psf = psf / psf.max()

# ============================================================
# Aerial image (optical convolution)
# ============================================================
aerial = fftconvolve(mask, psf, mode="same")
aerial = aerial / aerial.max()

# ============================================================
# Threshold resist model
# ============================================================
resist = aerial >= threshold

# ============================================================
# Save Matplotlib images
# ============================================================
plt.figure(figsize=(4,4))
plt.title("Aerial Image")
plt.imshow(aerial, cmap="hot")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "day4_aerial.png"))
plt.close()

plt.figure(figsize=(4,4))
plt.title("Printed Resist (Threshold Model)")
plt.imshow(resist, cmap="gray")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "day4_resist.png"))
plt.close()

center = nx // 2
profile = aerial[center, :]

plt.figure()
plt.title("Aerial Image Profile with Threshold")
plt.plot(profile, label="Intensity")
plt.axhline(threshold, color="r", linestyle="--", label="Threshold")
plt.xlabel("Position (pixels)")
plt.ylabel("Normalized Intensity")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "day4_profile.png"))
plt.close()

# ============================================================
# Plotly interactive profile
# ============================================================
x = np.arange(len(profile))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=profile, mode="lines", name="Intensity"))
fig.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text="Threshold")

fig.update_layout(
    title="Aerial Image Profile with Resist Threshold",
    xaxis_title="Position (pixels)",
    yaxis_title="Normalized Intensity"
)

fig.write_html(os.path.join(RESULTS_DIR, "day4_profile_interactive.html"))

print("Day 4 resist threshold simulation completed successfully.")
print("Results saved to:", RESULTS_DIR)
