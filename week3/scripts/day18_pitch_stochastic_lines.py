import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter, label
import plotly.graph_objects as go
import os

# ============================================================
# Results directory
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day18_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Two-line mask with variable pitch
# ============================================================
def two_lines(nx, width=6, pitch=30):
    img = np.zeros((nx, nx))
    c = nx // 2
    l = c - pitch//2
    r = c + pitch//2
    img[:, l-width//2:l+width//2] = 1.0
    img[:, r-width//2:r+width//2] = 1.0
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
nx = 256
pupil_radius = 45
focus_sigma = 1.2
dose = 1.0

# Photon statistics
photons_per_pixel = 1200

# Monte Carlo
N_trials = 50

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 3.0
develop_time = 1.0
resist_thickness = 0.55

# Pitch sweep (smaller = denser)
pitches = [18, 22, 26, 30, 36, 44]

# ============================================================
# PSF
# ============================================================
pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field)**2
psf /= psf.max()
psf = gaussian_filter(psf, sigma=focus_sigma)
psf /= psf.max()

# ============================================================
# Pitch sweep
# ============================================================
open_prob = []
short_prob = []

for pitch in pitches:

    mask = two_lines(nx, pitch=pitch)
    aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
    aerial_nominal /= aerial_nominal.max()

    opens = 0
    shorts = 0

    for _ in range(N_trials):

        photons = np.random.poisson(aerial_nominal * photons_per_pixel)
        aerial_noisy = photons / photons_per_pixel

        M = np.exp(-C * aerial_noisy)
        R = Rmax / (1 + (M / M0)**n)
        clear = R * develop_time
        printed = clear > resist_thickness

        labeled, num = label(printed)

        if num < 2:
            shorts += 1
        else:
            broken = False
            for y in range(nx):
                if printed[y].sum() == 0:
                    broken = True
                    break
            if broken:
                opens += 1

    open_prob.append(opens / N_trials)
    short_prob.append(shorts / N_trials)

# ============================================================
# Plots
# ============================================================
plt.figure()
plt.plot(pitches, open_prob, marker="o", label="Open Probability")
plt.plot(pitches, short_prob, marker="o", label="Short Probability")
plt.xlabel("Pitch (pixels)")
plt.ylabel("Probability")
plt.title("Stochastic Line Failure vs Pitch")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "failure_vs_pitch.png"))
plt.close()

# Plotly interactive
fig = go.Figure()
fig.add_trace(go.Scatter(x=pitches, y=open_prob, mode="lines+markers", name="Open"))
fig.add_trace(go.Scatter(x=pitches, y=short_prob, mode="lines+markers", name="Short"))
fig.update_layout(title="Stochastic Line Failure vs Pitch",
                  xaxis_title="Pitch (pixels)", yaxis_title="Probability")
fig.write_html(os.path.join(RESULTS_DIR, "failure_vs_pitch_interactive.html"))

# ============================================================
# Save numeric data
# ============================================================
np.savetxt(
    os.path.join(RESULTS_DIR, "failure_vs_pitch.txt"),
    np.column_stack((pitches, open_prob, short_prob)),
    header="Pitch   OpenProb   ShortProb"
)

print("Day 18 pitch dependence stochastic simulation completed.")
print("Results saved to:", RESULTS_DIR)
