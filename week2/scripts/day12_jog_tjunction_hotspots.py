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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day12_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Pattern generators
# ============================================================
def straight_line(nx, width=8, length=300):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c-length//2:c+length//2, c-width//2:c+width//2] = 1.0
    return img

def jog_pattern(nx, width=8, arm=200, shift=30):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c-arm//2:c, c-width//2:c+width//2] = 1.0
    img[c:c+arm//2, c+shift-width//2:c+shift+width//2] = 1.0
    return img

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
focus_sigma = 1.5
dose = 1.0

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
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
# Patterns to test
# ============================================================
patterns = {
    "Straight": straight_line(nx),
    "Jog": jog_pattern(nx),
    "T_Junction": t_junction(nx)
}

results = {}

# ============================================================
# Simulation loop
# ============================================================
for name, mask in patterns.items():

    aerial = fftconvolve(mask, psf, mode="same") * dose
    M = np.exp(-C * aerial)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time
    printed = clear > resist_thickness

    # Distance-based EPE approx
    dist_target = distance_transform_edt(~mask.astype(bool))
    dist_printed = distance_transform_edt(~printed)
    EPE_map = dist_printed - dist_target

    results[name] = {
        "mask": mask,
        "aerial": aerial,
        "PAC": M,
        "clear": clear,
        "printed": printed,
        "EPE": EPE_map
    }

    # Save stage plots
    for key, cmap in [
        ("aerial", "hot"),
        ("PAC", "viridis"),
        ("clear", "plasma"),
        ("printed", "gray"),
        ("EPE", "RdBu")
    ]:
        plt.figure(figsize=(4,4))
        plt.title(f"{name} — {key}")
        plt.imshow(results[name][key], cmap=cmap)
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"{name}_{key}.png"))
        plt.close()

# ============================================================
# ROI hotspot comparison
# ============================================================
c = nx // 2
roi = 100

worst = {}

for name in results:
    roi_map = results[name]["EPE"][c-roi:c+roi, c-roi:c+roi]
    worst[name] = np.nanmax(np.abs(roi_map))

# ============================================================
# Bar plot hotspot severity
# ============================================================
plt.figure()
plt.bar(worst.keys(), worst.values())
plt.ylabel("Worst |EPE| (pixels)")
plt.title("Hotspot Severity by Geometry")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "hotspot_severity_comparison.png"))
plt.close()

fig = go.Figure()
fig.add_trace(go.Bar(x=list(worst.keys()), y=list(worst.values())))
fig.update_layout(title="Hotspot Severity by Geometry", yaxis_title="Worst |EPE| (pixels)")
fig.write_html(os.path.join(RESULTS_DIR, "hotspot_severity_comparison_interactive.html"))

# ============================================================
# Save summary
# ============================================================
with open(os.path.join(RESULTS_DIR, "hotspot_summary.txt"), "w") as f:
    for k, v in worst.items():
        f.write(f"{k}: Worst |EPE| = {v}\n")

print("Day 12 jog and T-junction hotspot analysis completed.")
print("Results saved to:", RESULTS_DIR)
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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day12_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Pattern generators
# ============================================================
def straight_line(nx, width=8, length=300):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c-length//2:c+length//2, c-width//2:c+width//2] = 1.0
    return img

def jog_pattern(nx, width=8, arm=200, shift=30):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c-arm//2:c, c-width//2:c+width//2] = 1.0
    img[c:c+arm//2, c+shift-width//2:c+shift+width//2] = 1.0
    return img

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
focus_sigma = 1.5
dose = 1.0

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
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
# Patterns to test
# ============================================================
patterns = {
    "Straight": straight_line(nx),
    "Jog": jog_pattern(nx),
    "T_Junction": t_junction(nx)
}

results = {}

# ============================================================
# Simulation loop
# ============================================================
for name, mask in patterns.items():

    aerial = fftconvolve(mask, psf, mode="same") * dose
    M = np.exp(-C * aerial)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time
    printed = clear > resist_thickness

    # Distance-based EPE approx
    dist_target = distance_transform_edt(~mask.astype(bool))
    dist_printed = distance_transform_edt(~printed)
    EPE_map = dist_printed - dist_target

    results[name] = {
        "mask": mask,
        "aerial": aerial,
        "PAC": M,
        "clear": clear,
        "printed": printed,
        "EPE": EPE_map
    }

    # Save stage plots
    for key, cmap in [
        ("aerial", "hot"),
        ("PAC", "viridis"),
        ("clear", "plasma"),
        ("printed", "gray"),
        ("EPE", "RdBu")
    ]:
        plt.figure(figsize=(4,4))
        plt.title(f"{name} — {key}")
        plt.imshow(results[name][key], cmap=cmap)
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"{name}_{key}.png"))
        plt.close()

# ============================================================
# ROI hotspot comparison
# ============================================================
c = nx // 2
roi = 100

worst = {}

for name in results:
    roi_map = results[name]["EPE"][c-roi:c+roi, c-roi:c+roi]
    worst[name] = np.nanmax(np.abs(roi_map))

# ============================================================
# Bar plot hotspot severity
# ============================================================
plt.figure()
plt.bar(worst.keys(), worst.values())
plt.ylabel("Worst |EPE| (pixels)")
plt.title("Hotspot Severity by Geometry")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "hotspot_severity_comparison.png"))
plt.close()

fig = go.Figure()
fig.add_trace(go.Bar(x=list(worst.keys()), y=list(worst.values())))
fig.update_layout(title="Hotspot Severity by Geometry", yaxis_title="Worst |EPE| (pixels)")
fig.write_html(os.path.join(RESULTS_DIR, "hotspot_severity_comparison_interactive.html"))

# ============================================================
# Save summary
# ============================================================
with open(os.path.join(RESULTS_DIR, "hotspot_summary.txt"), "w") as f:
    for k, v in worst.items():
        f.write(f"{k}: Worst |EPE| = {v}\n")

print("Day 12 jog and T-junction hotspot analysis completed.")
print("Results saved to:", RESULTS_DIR)
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
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day12_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Pattern generators
# ============================================================
def straight_line(nx, width=8, length=300):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c-length//2:c+length//2, c-width//2:c+width//2] = 1.0
    return img

def jog_pattern(nx, width=8, arm=200, shift=30):
    img = np.zeros((nx, nx))
    c = nx // 2
    img[c-arm//2:c, c-width//2:c+width//2] = 1.0
    img[c:c+arm//2, c+shift-width//2:c+shift+width//2] = 1.0
    return img

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
focus_sigma = 1.5
dose = 1.0

# Dill
C = 1.2

# Mack
Rmax = 1.0
M0 = 0.5
n = 2.5
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
# Patterns to test
# ============================================================
patterns = {
    "Straight": straight_line(nx),
    "Jog": jog_pattern(nx),
    "T_Junction": t_junction(nx)
}

results = {}

# ============================================================
# Simulation loop
# ============================================================
for name, mask in patterns.items():

    aerial = fftconvolve(mask, psf, mode="same") * dose
    M = np.exp(-C * aerial)
    R = Rmax / (1 + (M / M0)**n)
    clear = R * develop_time
    printed = clear > resist_thickness

    # Distance-based EPE approx
    dist_target = distance_transform_edt(~mask.astype(bool))
    dist_printed = distance_transform_edt(~printed)
    EPE_map = dist_printed - dist_target

    results[name] = {
        "mask": mask,
        "aerial": aerial,
        "PAC": M,
        "clear": clear,
        "printed": printed,
        "EPE": EPE_map
    }

    # Save stage plots
    for key, cmap in [
        ("aerial", "hot"),
        ("PAC", "viridis"),
        ("clear", "plasma"),
        ("printed", "gray"),
        ("EPE", "RdBu")
    ]:
        plt.figure(figsize=(4,4))
        plt.title(f"{name} — {key}")
        plt.imshow(results[name][key], cmap=cmap)
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(os.path.join(RESULTS_DIR, f"{name}_{key}.png"))
        plt.close()

# ============================================================
# ROI hotspot comparison
# ============================================================
c = nx // 2
roi = 100

worst = {}

for name in results:
    roi_map = results[name]["EPE"][c-roi:c+roi, c-roi:c+roi]
    worst[name] = np.nanmax(np.abs(roi_map))

# ============================================================
# Bar plot hotspot severity
# ============================================================
plt.figure()
plt.bar(worst.keys(), worst.values())
plt.ylabel("Worst |EPE| (pixels)")
plt.title("Hotspot Severity by Geometry")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "hotspot_severity_comparison.png"))
plt.close()

fig = go.Figure()
fig.add_trace(go.Bar(x=list(worst.keys()), y=list(worst.values())))
fig.update_layout(title="Hotspot Severity by Geometry", yaxis_title="Worst |EPE| (pixels)")
fig.write_html(os.path.join(RESULTS_DIR, "hotspot_severity_comparison_interactive.html"))

# ============================================================
# Save summary
# ============================================================
with open(os.path.join(RESULTS_DIR, "hotspot_summary.txt"), "w") as f:
    for k, v in worst.items():
        f.write(f"{k}: Worst |EPE| = {v}\n")

print("Day 12 jog and T-junction hotspot analysis completed.")
print("Results saved to:", RESULTS_DIR)
