import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Create circular pupil
# -------------------------
def circular_pupil(nx, radius):
    y, x = np.ogrid[-nx//2:nx//2, -nx//2:nx//2]
    mask = x*x + y*y <= radius*radius
    return mask.astype(float)

# -------------------------
# Simulation grid
# -------------------------
nx = 512

# try different NA-like radii
radii = [30, 60, 100]

for r in radii:

    pupil = circular_pupil(nx, r)

    # Fourier optics: pupil -> PSF
    field = np.fft.ifft2(np.fft.ifftshift(pupil))
    psf = np.abs(field)**2
    psf = psf / psf.max()

    # -------------------------
    # Save pupil image
    # -------------------------
    plt.figure(figsize=(4,4))
    plt.title(f"Pupil (radius={r})")
    plt.imshow(pupil, cmap="gray")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"../results/pupil_r{r}.png")
    plt.close()

    # -------------------------
    # Save PSF image
    # -------------------------
    plt.figure(figsize=(4,4))
    plt.title(f"PSF (radius={r})")
    plt.imshow(psf, cmap="hot")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f"../results/psf_r{r}.png")
    plt.close()

    # -------------------------
    # Save center line profile
    # -------------------------
    center = nx // 2
    profile = psf[center, :]

    plt.figure()
    plt.title(f"PSF Profile (radius={r})")
    plt.plot(profile)
    plt.xlabel("Position (pixels)")
    plt.ylabel("Intensity")
    plt.tight_layout()
    plt.savefig(f"../results/psf_profile_r{r}.png")
    plt.close()
