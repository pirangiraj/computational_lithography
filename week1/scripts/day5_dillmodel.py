import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
import plotly.graph_objects as go
import os

# ============================================================
# Path-safe results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results","day5_results")
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
C = 0.8            # Dill exposure rate constant
dose = 1.0        # exposure time * intensity scaling

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
# Dill exposure model: PAC concentration
# ============================================================
M = np.exp(-C * aerial * dose)

# ============================================================
# Save images (Matplotlib)
# ============================================================
plt.figure(figsize=(4,4))
plt.title("Aerial Image")
plt.imshow(aerial, cmap="hot")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "day5_aerial.png"))
plt.close()

plt.figure(figsize=(4,4))
plt.title("PAC Concentration (Dill Model)")
plt.imshow(M, cmap="viridis")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "day5_pac.png"))
plt.close()

# ============================================================
# Line profile
# ============================================================
center = nx // 2
profile_I = aerial[center, :]
profile_M = M[center, :]

plt.figure()
plt.title("Aerial Intensity and PAC Profile")
plt.plot(profile_I, label="Intensity")
plt.plot(profile_M, label="PAC (M)")
plt.xlabel("Position (pixels)")
plt.ylabel("Normalized Value")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "day5_profiles.png"))
plt.close()

# ============================================================
# Plotly interactive profile
# ============================================================
x = np.arange(len(profile_I))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=profile_I, mode="lines", name="Intensity"))
fig.add_trace(go.Scatter(x=x, y=profile_M, mode="lines", name="PAC (M)"))

fig.update_layout(
    title="Aerial Intensity vs PAC Concentration (Dill Model)",
    xaxis_title="Position (pixels)",
    yaxis_title="Normalized Value"
)

fig.write_html(os.path.join(RESULTS_DIR, "day5_profiles_interactive.html"))

# ============================================================
# Dose sweep for contrast curve
# ============================================================
doses = np.linspace(0.1, 2.0, 50)
M_center = []

I0 = aerial[nx//2, nx//2]

for d in doses:
    M_center.append(np.exp(-C * I0 * d))

plt.figure()
plt.title("PAC vs Dose (Contrast Behavior)")
plt.plot(doses, M_center)
plt.xlabel("Dose")
plt.ylabel("PAC Concentration")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "day5_pac_vs_dose.png"))
plt.close()

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=doses, y=M_center, mode="lines"))
fig2.update_layout(
    title="PAC vs Dose (Dill Exposure Curve)",
    xaxis_title="Dose",
    yaxis_title="PAC Concentration"
)
fig2.write_html(os.path.join(RESULTS_DIR, "day5_pac_vs_dose_interactive.html"))

print("Day 5 Dill exposure simulation completed successfully.")
print("Results saved to:", RESULTS_DIR)
