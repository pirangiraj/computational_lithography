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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day13_results")
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

# Process sweep
doses = np.linspace(0.8, 1.2, 9)
focus_vals = np.linspace(0.0, 2.5, 9)

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
develop_time = 1.0
resist_thickness = 0.55

# ============================================================
# PSF (nominal)
# ============================================================
pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf_nominal = np.abs(field)**2
psf_nominal /= psf_nominal.max()

# ============================================================
# Pattern
# ============================================================
mask = t_junction(nx)

# ============================================================
# Conditional hotspot sweep
# ============================================================
worst_EPE = np.zeros((len(focus_vals), len(doses)))

for i, f in enumerate(focus_vals):

    psf = gaussian_filter(psf_nominal, sigma=f)
    psf /= psf.max()

    for j, dose in enumerate(doses):

        aerial = fftconvolve(mask, psf, mode="same") * dose
        M = np.exp(-C * aerial)
        R = Rmax / (1 + (M / M0)**n)
        clear = R * develop_time
        printed = clear > resist_thickness

        dist_target = distance_transform_edt(~mask.astype(bool))
        dist_printed = distance_transform_edt(~printed)
        EPE_map = dist_printed - dist_target

        # ROI near junction
        c = nx // 2
        roi = 80
        roi_map = EPE_map[c-roi:c+roi, c-roi:c+roi]

        worst_EPE[i, j] = np.nanmax(np.abs(roi_map))

# ============================================================
# Heatmap
# ============================================================
plt.figure(figsize=(6,5))
plt.imshow(
    worst_EPE,
    origin="lower",
    extent=[doses[0], doses[-1], focus_vals[0], focus_vals[-1]],
    aspect="auto",
    cmap="inferno"
)
plt.colorbar(label="Worst |EPE| (pixels)")
plt.xlabel("Dose")
plt.ylabel("Focus (blur sigma)")
plt.title("Conditional Hotspot Severity (T-junction)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "conditional_hotspot_heatmap.png"))
plt.close()

# ============================================================
# Plotly interactive
# ============================================================
fig = go.Figure(data=go.Heatmap(
    z=worst_EPE,
    x=doses,
    y=focus_vals,
    colorscale="Inferno",
    colorbar=dict(title="Worst |EPE|")
))
fig.update_layout(
    title="Conditional Hotspot Severity (T-junction)",
    xaxis_title="Dose",
    yaxis_title="Focus (blur sigma)"
)
fig.write_html(os.path.join(RESULTS_DIR, "conditional_hotspot_heatmap_interactive.html"))

# ============================================================
# Save data
# ============================================================
np.savetxt(
    os.path.join(RESULTS_DIR, "conditional_hotspot_data.txt"),
    worst_EPE,
    header="Rows=Focus, Cols=Dose"
)

print("Day 13 conditional hotspot analysis completed.")
print("Results saved to:", RESULTS_DIR)
