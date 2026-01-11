import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import plotly.graph_objects as go
import os

# ============================================================
# Path-safe results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day7_results")
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
    return (x*x + y*y <= radius*radius).astype(float)

# ============================================================
# Parameters
# ============================================================
nx = 512
pupil_radius = 60

# Dill parameters
C = 1.2

# Mack parameters (softened)
Rmax = 1.0
M0 = 0.5
n = 2.0
develop_time = 1.0
resist_thickness = 0.55

# Dose sweep
doses = np.linspace(0.6, 1.4, 15)

# ============================================================
# Optical imaging (fixed, no renormalization later)
# ============================================================
mask = two_lines_mask(nx, line_width=6, spacing=30)

pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field) ** 2
psf /= psf.max()

aerial_nominal = fftconvolve(mask, psf, mode="same")

# Target edge
center = nx // 2
target_edge = center + 15

# ============================================================
# Sweep dose
# ============================================================
CDs = []
EPEs = []

for dose in doses:
    aerial = aerial_nominal * dose   # NO RENORMALIZATION

    M = np.exp(-C * aerial)
    R = Rmax / (1 + (M / M0) ** n)
    clear = R * develop_time

    printed = clear > resist_thickness

    row = printed[center, :].astype(int)
    edges = np.where(np.diff(row) != 0)[0]

    if len(edges) >= 2:
        cd = edges[1] - edges[0]
        edge_pos = edges[1]
        epe = edge_pos - target_edge
    else:
        cd = np.nan
        epe = np.nan

    CDs.append(cd)
    EPEs.append(epe)

# ============================================================
# Save Matplotlib plots
# ============================================================
plt.figure()
plt.title("CD vs Dose")
plt.plot(doses, CDs, marker="o")
plt.xlabel("Dose")
plt.ylabel("CD (pixels)")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "cd_vs_dose.png"))
plt.close()

plt.figure()
plt.title("EPE vs Dose")
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
fig1.update_layout(title="CD vs Dose", xaxis_title="Dose", yaxis_title="CD (pixels)")
fig1.write_html(os.path.join(RESULTS_DIR, "cd_vs_dose_interactive.html"))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=doses, y=EPEs, mode="lines+markers"))
fig2.add_hline(y=0, line_dash="dash")
fig2.update_layout(title="EPE vs Dose", xaxis_title="Dose", yaxis_title="EPE (pixels)")
fig2.write_html(os.path.join(RESULTS_DIR, "epe_vs_dose_interactive.html"))

# ============================================================
# Save numeric data
# ============================================================
np.savetxt(
    os.path.join(RESULTS_DIR, "process_window_data.txt"),
    np.column_stack((doses, CDs, EPEs)),
    header="Dose   CD_pixels   EPE_pixels"
)

print("Day 7 corrected process window simulation completed.")
print("Results saved to:", RESULTS_DIR)
