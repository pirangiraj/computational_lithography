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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day9_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Patterns
# ============================================================
def isolated_line(nx, width=6):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[:, c - width//2 : c + width//2] = 1.0
    return img

def dense_lines(nx, width=6, pitch=20):
    img = np.zeros((nx, nx))
    for x in range(0, nx, pitch):
        img[:, x + pitch//2 - width//2 : x + pitch//2 + width//2] = 1.0
    return img

def line_end(nx, width=6, length=200):
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
pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf_nominal = np.abs(field)**2
psf_nominal /= psf_nominal.max()
psf = gaussian_filter(psf_nominal, sigma=focus_sigma)
psf /= psf.max()

# ============================================================
# Patterns to analyze
# ============================================================
patterns = {
    "Isolated Line": isolated_line(nx),
    "Dense Lines": dense_lines(nx),
    "Line End": line_end(nx)
}

EPE_results = {}

# ============================================================
# Simulate each pattern
# ============================================================
for name, mask in patterns.items():

    aerial = fftconvolve(mask, psf, mode="same") * dose

    M = np.exp(-C * aerial)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time

    center = nx // 2

    if name == "Line End":
        profile = clear[:, center]
        target_edge = center + 100
    else:
        profile = clear[center, :]
        target_edge = center

    edges = find_edges_subpixel(profile, resist_thickness)

    if len(edges) >= 1:
        epe = edges[0] - target_edge
    else:
        epe = np.nan

    EPE_results[name] = epe

    plt.figure(figsize=(4,4))
    plt.title(f"{name} – Printed Resist (Depth Map)")
    plt.imshow(clear, cmap="viridis")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, f"{name.replace(' ','_')}_clear_depth.png"))
    plt.close()

# ============================================================
# Bar chart comparison
# ============================================================
names = list(EPE_results.keys())
values = [EPE_results[n] for n in names]

plt.figure()
plt.bar(names, values)
plt.axhline(0, linestyle="--")
plt.ylabel("EPE (pixels)")
plt.title("Pattern-Dependent EPE (Hotspot Analysis)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "pattern_epe_comparison.png"))
plt.close()

# Plotly interactive
fig = go.Figure()
fig.add_trace(go.Bar(x=names, y=values))
fig.add_hline(y=0, line_dash="dash")
fig.update_layout(title="Pattern-Dependent EPE (Hotspot Analysis)", yaxis_title="EPE (pixels)")
fig.write_html(os.path.join(RESULTS_DIR, "pattern_epe_comparison_interactive.html"))

# ============================================================
# Save numeric data
# ============================================================
with open(os.path.join(RESULTS_DIR, "hotspot_epe_values.txt"), "w") as f:
    for k, v in EPE_results.items():
        f.write(f"{k}: {v}\n")

print("Day 9 hotspot pattern analysis completed.")
print("Results saved to:", RESULTS_DIR)
