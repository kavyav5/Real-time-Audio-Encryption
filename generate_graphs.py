import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

# mpl.rcParams['figure.dpi'] = 150
mpl.rcParams.update({
    "figure.dpi": 150,
    "font.family": "Helvetica",
    "font.size": 14,
    "axes.labelsize": 12
})

# ----- Customize -----
max_frames = round(20 * 4.5)
ticks_per_second = 20
# Docs: https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html
# Usually "none" or "antialiased"
interpolation = "none"
# Less => vertically shrink
# More => vertically stretch
size = 1200

# ----- Graphing Code -----
fig, axs = plt.subplots(3, figsize=(6, 9))

data = np.load("./output/spectrogram_before.npy", allow_pickle=False)
datapoints = min(data.shape[0], max_frames)
data = data[:datapoints]
shape = data.shape
data = np.ndarray.tobytes(data)
data = np.frombuffer(data, dtype=np.int32).reshape(shape).T
data_original = data
aspect = size / datapoints
x_extent = max_frames / ticks_per_second
y_extent = x_extent / shape[1] * shape[0]

pos = axs[0].imshow(
    data,
    extent=[0, x_extent, 0, y_extent],
    cmap="viridis",
    aspect=aspect,
    interpolation=interpolation
)

axs[0].set_title("Wavelet Spectrogram Before Encryption")

axs[0].set_xlabel("Seconds (20 frames/sec)")

axs[0].set_ylabel("DWT Approximate\nCoefficients (pywavelets)")
axs[1].yaxis.set_tick_params(labelleft=False)
axs[0].set_yticks([])
axs[0].set_yticklabels([])

fig.colorbar(pos, ax=axs[0], anchor=(0.1, 0.5), shrink=0.7)

data = np.load("./output/spectrogram_mid.npy", allow_pickle=False)
datapoints = min(data.shape[0], max_frames)
data = data[:datapoints]
shape = data.shape
data = np.ndarray.tobytes(data)
data = np.frombuffer(data, dtype=np.int32).reshape(shape).T
data_mid = data
aspect = size / datapoints
y_extent = x_extent / shape[1] * shape[0]

pos = axs[1].imshow(
    data,
    extent=[0, x_extent, 0, y_extent],
    cmap="viridis",
    aspect=aspect,
    interpolation=interpolation
)

axs[1].set_title("Wavelet Spectrogram After Encryption")

axs[1].set_xlabel("Seconds (20 frames/sec)")

axs[1].set_ylabel("Encrypted Coefficients")
axs[1].yaxis.set_tick_params(labelleft=False)
axs[1].set_yticks([])
axs[1].set_yticklabels([])

fig.colorbar(pos, ax=axs[1], anchor=(0.1, 0.5), shrink=0.7)

data = np.load("./output/spectrogram_after.npy", allow_pickle=False)
datapoints = min(data.shape[0], max_frames)
data = data[:datapoints]
shape = data.shape
data = np.ndarray.tobytes(data)
data = np.frombuffer(data, dtype=np.int32).reshape(shape).T
data_after = data
aspect = size / datapoints
y_extent = x_extent / shape[1] * shape[0]

pos = axs[2].imshow(
    data,
    extent=[0, x_extent, 0, y_extent],
    cmap="viridis",
    aspect=aspect,
    interpolation=interpolation
)

axs[2].set_title("Wavelet Spectrogram After Decryption")

axs[2].set_xlabel("Seconds (20 frames/sec)")

axs[2].set_ylabel("DWT Approximate\nCoefficients (pywavelets)")
axs[2].yaxis.set_tick_params(labelleft=False)
axs[2].set_yticks([])
axs[2].set_yticklabels([])

fig.colorbar(pos, ax=axs[2], anchor=(0.1, 0.5), shrink=0.7)

plt.tight_layout()
plt.savefig("./output/spectrogram.png")
# plt.show()

print("Average:", np.average(data))
print("STD:", np.std(data))

data_original = np.array(data_original, dtype=np.int64)
data_mid = np.array(data_mid, dtype=np.int64)
data_after = np.array(data_after, dtype=np.int64)

# MSE values used in paper
print("MSE Before:", np.average((data_original - data_mid)**2))
print("MSE After:", np.average((data_original - data_after)**2))

# New graph
plt.close()

data = np.load("./output/time_data.npy", allow_pickle=False) / 10**6
datapoints = min(data.shape[0], max_frames)
data = data[:datapoints]
total_time = data.size // 20 if data.size % 20 == 0 else data.size / 20

plt.scatter(np.linspace(0, total_time, data.size), data)
plt.title("Signal Latency")
plt.xlabel("Seconds (20 frames/sec)")
plt.ylabel("Transmission Time (ms)")

plt.tight_layout()
plt.savefig("./output/latency.png")
# plt.show()
