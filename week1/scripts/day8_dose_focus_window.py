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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day8_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Mask
# ============================================================
def two_lines_mask(nx, line_width=6, spacing=30):
    img = np.zeros((nx, nx))
    c = nx // 2
    l = c - spacing // 2
    r = c + spacing // 2
    img[:, l - line_width//2 : l + line_width//2] = 1.0
    img[:, r - line_width//2 : r + line_width//2] = 1.0
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

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
develop_time = 1.0
resist_thickness = 0.55

# Dose and focus sweep
doses = np.linspace(0.7, 1.3, 11)
focus_vals = np.linspace(0.0, 2.5, 11)  # blur sigma

# ============================================================
# Optical base image
# ============================================================
mask = two_lines_mask(nx, 6, 30)

pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf_nominal = np.abs(field)**2
psf_nominal /= psf_nominal.max()

aerial_base = fftconvolve(mask, psf_nominal, mode="same")

center = nx // 2
target_edge = center + 15

# ============================================================
# Dose–focus sweep
# ============================================================
EPE_map = np.zeros((len(focus_vals), len(doses)))

for i, f in enumerate(focus_vals):

    psf_defocus = gaussian_filter(psf_nominal, sigma=f)
    psf_defocus /= psf_defocus.max()

    aerial_f = fftconvolve(mask, psf_defocus, mode="same")

    for j, dose in enumerate(doses):

        aerial = aerial_f * dose

        M = np.exp(-C * aerial)
        R = Rmax / (1 + (M / M0)**n)
        clear = R * develop_time

        profile = clear[center, :]

        edges = find_edges_subpixel(profile, resist_thickness)

        if len(edges) >= 2:
            epe = edges[1] - target_edge
        else:
            epe = np.nan

        EPE_map[i, j] = epe

# ============================================================
# Save heatmap (matplotlib)
# ============================================================
plt.figure(figsize=(6,5))
plt.imshow(EPE_map, origin="lower",
           extent=[doses[0], doses[-1], focus_vals[0], focus_vals[-1]],
           aspect="auto", cmap="coolwarm")
plt.colorbar(label="EPE (pixels)")
plt.xlabel("Dose")
plt.ylabel("Focus (blur sigma)")
plt.title("Dose–Focus EPE Process Window")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "epe_heatmap.png"))
plt.close()

# ============================================================
# Plotly interactive heatmap
# ============================================================
fig = go.Figure(data=go.Heatmap(
    z=EPE_map,
    x=doses,
    y=focus_vals,
    colorscale="RdBu",
    colorbar=dict(title="EPE (pixels)")
))

fig.update_layout(
    title="Dose–Focus EPE Process Window",
    xaxis_title="Dose",
    yaxis_title="Focus (blur sigma)"
)

fig.write_html(os.path.join(RESULTS_DIR, "epe_heatmap_interactive.html"))

# ============================================================
# Worst-case EPE vs focus
# ============================================================
worst_EPE = np.nanmax(np.abs(EPE_map), axis=1)

plt.figure()
plt.plot(focus_vals, worst_EPE, marker="o")
plt.xlabel("Focus (blur sigma)")
plt.ylabel("Worst |EPE| (pixels)")
plt.title("Worst-case EPE vs Focus")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "worst_epe_vs_focus.png"))
plt.close()

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=focus_vals, y=worst_EPE, mode="lines+markers"))
fig2.update_layout(
    title="Worst-case EPE vs Focus",
    xaxis_title="Focus (blur sigma)",
    yaxis_title="Worst |EPE| (pixels)"
)
fig2.write_html(os.path.join(RESULTS_DIR, "worst_epe_vs_focus_interactive.html"))

print("Day 8 dose–focus process window simulation completed.")
print("Results saved to:", RESULTS_DIR)
