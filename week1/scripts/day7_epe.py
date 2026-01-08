import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import plotly.graph_objects as go
import os

# ============================================================
# Path-safe results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day7_results2")
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
# Sub-pixel contour extraction
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

# Dose sweep
doses = np.linspace(0.6, 1.4, 15)

# ============================================================
# Optical base image
# ============================================================
mask = two_lines_mask(nx, 6, 30)

pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field)**2
psf /= psf.max()

aerial_nominal = fftconvolve(mask, psf, mode="same")

# Target edge from design
center = nx // 2
target_edge = center + 15

# ============================================================
# Sweep dose
# ============================================================
CDs = []
EPEs = []

for dose in doses:
    aerial = aerial_nominal * dose

    # Dill
    M = np.exp(-C * aerial)

    # Mack
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time

    profile = clear[center, :]

    edges = find_edges_subpixel(profile, resist_thickness)

    if len(edges) >= 2:
        cd = edges[1] - edges[0]
        epe = edges[1] - target_edge
    else:
        cd = np.nan
        epe = np.nan

    CDs.append(cd)
    EPEs.append(epe)

# ============================================================
# Save plots (matplotlib)
# ============================================================
plt.figure()
plt.title("CD vs Dose (Continuous Resist)")
plt.plot(doses, CDs, marker="o")
plt.xlabel("Dose")
plt.ylabel("CD (pixels)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "cd_vs_dose.png"))
plt.close()

plt.figure()
plt.title("EPE vs Dose (Continuous Resist)")
plt.plot(doses, EPEs, marker="o")
plt.axhline(0, linestyle="--")
plt.xlabel("Dose")
plt.ylabel("EPE (pixels)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "epe_vs_dose.png"))
plt.close()

# ============================================================
# Plotly interactive
# ============================================================
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=doses, y=CDs, mode="lines+markers"))
fig1.update_layout(title="CD vs Dose (Continuous Resist)", xaxis_title="Dose", yaxis_title="CD")
fig1.write_html(os.path.join(RESULTS_DIR, "cd_vs_dose_interactive.html"))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=doses, y=EPEs, mode="lines+markers"))
fig2.add_hline(y=0, line_dash="dash")
fig2.update_layout(title="EPE vs Dose (Continuous Resist)", xaxis_title="Dose", yaxis_title="EPE")
fig2.write_html(os.path.join(RESULTS_DIR, "epe_vs_dose_interactive.html"))

# ============================================================
# Save numeric data
# ============================================================
np.savetxt(
    os.path.join(RESULTS_DIR, "process_window_data.txt"),
    np.column_stack((doses, CDs, EPEs)),
    header="Dose   CD_pixels   EPE_pixels"
)

print("Day 7 continuous resist EPE simulation completed.")
print("Results saved to:", RESULTS_DIR)
