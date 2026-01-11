import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os

# ============================================================
# Paths
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAY19_DIR = os.path.join(BASE_DIR, "results", "day19_results")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "day20_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# Load edge data from Day 19
# ============================================================
# We reuse printed trial images to reconstruct roughness
# But better: regenerate using saved statistics (simplified here)

# Instead: we reload roughness summary approximations
# For educational purposes, we recompute PSD from saved printed images

edge_profiles = []

for fname in os.listdir(DAY19_DIR):
    if fname.startswith("printed_trial_"):
        img = plt.imread(os.path.join(DAY19_DIR, fname))
        if img.ndim == 3:
            img = img[:,:,0]

        nx = img.shape[0]
        left_edge = []

        for y in range(nx):
            row = img[y] > 0.5
            idx = np.where(row)[0]
            if len(idx) > 0:
                left_edge.append(idx[0])

        if len(left_edge) == nx:
            edge_profiles.append(np.array(left_edge))

edge_profiles = np.array(edge_profiles)

# ============================================================
# Edge deviation
# ============================================================
mean_edge = np.mean(edge_profiles, axis=0)
edge_dev = edge_profiles - mean_edge

# ============================================================
# PSD computation
# ============================================================
def compute_psd(signal):
    fft = np.fft.fft(signal)
    psd = np.abs(fft)**2
    return psd[:len(psd)//2]

psd_list = []
for i in range(edge_dev.shape[0]):
    psd_list.append(compute_psd(edge_dev[i]))

psd_mean = np.mean(psd_list, axis=0)
freq = np.fft.fftfreq(len(mean_edge))[:len(psd_mean)]

# ============================================================
# Autocorrelation
# ============================================================
def autocorr(x):
    x = x - np.mean(x)
    result = np.correlate(x, x, mode='full')
    return result[result.size//2:]

auto = np.mean([autocorr(edge_dev[i]) for i in range(edge_dev.shape[0])], axis=0)
auto /= auto[0]

# Correlation length = where autocorr drops to 1/e
corr_len = np.where(auto < 1/np.e)[0]
corr_len = corr_len[0] if len(corr_len) > 0 else len(auto)

# ============================================================
# Plots
# ============================================================
plt.figure()
plt.plot(psd_mean)
plt.yscale("log")
plt.title("Mean Roughness PSD")
plt.xlabel("Spatial Frequency Index")
plt.ylabel("Power")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "PSD.png"))
plt.close()

plt.figure()
plt.plot(auto)
plt.axhline(1/np.e, linestyle="--")
plt.axvline(corr_len, linestyle="--")
plt.title("Autocorrelation of Edge Roughness")
plt.xlabel("Lag")
plt.ylabel("Normalized Correlation")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "autocorrelation.png"))
plt.close()

# Interactive PSD
fig = go.Figure()
fig.add_trace(go.Scatter(y=psd_mean, mode="lines"))
fig.update_layout(title="Roughness PSD (log scale)",
                  yaxis_type="log",
                  xaxis_title="Spatial Frequency Index",
                  yaxis_title="Power")
fig.write_html(os.path.join(RESULTS_DIR, "PSD_interactive.html"))

# ============================================================
# Save stats
# ============================================================
with open(os.path.join(RESULTS_DIR, "correlation_length.txt"), "w") as f:
    f.write(f"Estimated correlation length (pixels): {corr_len}\n")

print("Day 20 PSD and correlation length analysis completed.")
print("Estimated correlation length:", corr_len)
print("Results saved to:", RESULTS_DIR)
