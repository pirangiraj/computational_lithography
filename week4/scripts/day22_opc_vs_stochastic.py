import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter
import os

# ============================================================
# Paths
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day22_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Masks
# ============================================================
def plain_line(nx, width=8):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[:, c-width//2:c+width//2] = 1.0
    return img

def opc_line(nx, width=8, serif=3):
    img = plain_line(nx, width)
    c = nx // 2
    for y in range(0, nx, 12):
        img[y:y+serif, c-width//2-serif:c-width//2] = 1.0
        img[y:y+serif, c+width//2:c+width//2+serif] = 1.0
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
focus_sigma = 1.1
dose = 1.0

photons_per_pixel = 900
N_trials = 30

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 3.0
develop_time = 1.0
resist_thickness = 0.55

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
# Run both cases
# ============================================================
def simulate(mask):

    aerial_nominal = fftconvolve(mask, psf, mode="same") * dose
    aerial_nominal /= aerial_nominal.max()

    slopes = []
    widths = []

    for _ in range(N_trials):

        photons = np.random.poisson(aerial_nominal * photons_per_pixel)
        aerial_noisy = photons / photons_per_pixel

        M = np.exp(-C * aerial_noisy)
        R = Rmax / (1 + (M / M0)**n)
        clear = R * develop_time
        printed = clear > resist_thickness

        mid = nx // 2
        slope = np.gradient(aerial_nominal[mid])
        slopes.append(np.max(np.abs(slope)))

        row = printed[mid]
        idx = np.where(row)[0]
        if len(idx) > 0:
            widths.append(idx[-1] - idx[0])

    return np.array(slopes), np.array(widths)

mask_plain = plain_line(nx)
mask_opc = opc_line(nx)

slope_plain, width_plain = simulate(mask_plain)
slope_opc, width_opc = simulate(mask_opc)

# ============================================================
# Plots
# ============================================================
plt.figure()
plt.hist(width_plain, alpha=0.6, label="No OPC")
plt.hist(width_opc, alpha=0.6, label="With OPC")
plt.legend()
plt.title("Printed Line Width Distribution")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "width_distribution.png"))
plt.close()

plt.figure()
plt.boxplot([slope_plain, slope_opc], labels=["No OPC", "With OPC"])
plt.title("Aerial Image Slope Comparison")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "slope_comparison.png"))
plt.close()

with open(os.path.join(RESULTS_DIR, "summary.txt"), "w") as f:
    f.write(f"Mean slope no OPC: {np.mean(slope_plain)}\n")
    f.write(f"Mean slope OPC: {np.mean(slope_opc)}\n")
    f.write(f"Width sigma no OPC: {np.std(width_plain)}\n")
    f.write(f"Width sigma OPC: {np.std(width_opc)}\n")

print("Day 22 OPC vs stochastic variability simulation completed.")
print("Results saved to:", RESULTS_DIR)
