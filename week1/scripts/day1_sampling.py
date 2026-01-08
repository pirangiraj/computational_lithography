import numpy as np
import matplotlib.pyplot as plt

def vertical_line(nx, width_px=6):
    img = np.zeros((nx, nx))
    center = nx//2
    img[:, center - width_px//2 : center + width_px//2] = 1.0
    return img

resolutions = [64, 128, 256, 512]

for nx in resolutions:
    mask = vertical_line(nx)

    plt.figure(figsize=(4,4))
    plt.title(f"Resolution: {nx} x {nx}")
    plt.imshow(mask, cmap="gray")
    plt.colorbar(label="Transmission")
    plt.savefig(f"../results/mask_{nx}.png")
    plt.close()
