import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

# -------------------------
# Mask: two vertical lines
# -------------------------
def two_lines_mask(nx, line_width=6, spacing=20):
    img = np.zeros((nx, nx))
    center = nx // 2

    left = center - spacing//2
    right = center + spacing//2

    img[:, left - line_width//2 : left + line_width//2] = 1.0
    img[:, right - line_width//2 : right + line_width//2] = 1.0
    return img

# -------------------------
# Circular pupil -> PSF
# -------------------------
def circular_pupil(nx, radius):
    y, x = np.ogrid[-nx//2:nx//2, -nx//2:nx//2]
    mask = x*x + y*y <= radius*radius
    return mask.astype(float)

# -------------------------
# Simulation parameters
# -------------------------
nx = 512
pupil_radius = 60

mask = two_lines_mask(nx, line_width=6, spacing=30)

pupil = circular_pupil(nx, pupil_radius)
field = np.fft.ifft2(np.fft.ifftshift(pupil))
psf = np.abs(field)**2
psf = psf / psf.max()

# -------------------------
# Aerial image = mask ⊗ PSF
# -------------------------
aerial = fftconvolve(mask, psf, mode="same")
aerial = aerial / aerial.max()

# -------------------------
# Save images
# -------------------------
plt.figure(figsize=(4,4))
plt.title("Mask Pattern")
plt.imshow(mask, cmap="gray")
plt.colorbar()
plt.tight_layout()
plt.savefig("../results/day3_mask.png")
plt.close()

plt.figure(figsize=(4,4))
plt.title("Point Spread Function")
plt.imshow(psf, cmap="hot")
plt.colorbar()
plt.tight_layout()
plt.savefig("../results/day3_psf.png")
plt.close()

plt.figure(figsize=(4,4))
plt.title("Aerial Image (Intensity)")
plt.imshow(aerial, cmap="hot")
plt.colorbar()
plt.tight_layout()
plt.savefig("../results/day3_aerial.png")
plt.close()

# -------------------------
# Line profile
# -------------------------
center = nx // 2
profile = aerial[center, :]

plt.figure()
plt.title("Aerial Image Line Profile")
plt.plot(profile)
plt.xlabel("Position (pixels)")
plt.ylabel("Normalized Intensity")
plt.tight_layout()
plt.savefig("../results/day3_profile.png")
plt.close()

print("Day 3 simulation completed. Results saved.")
