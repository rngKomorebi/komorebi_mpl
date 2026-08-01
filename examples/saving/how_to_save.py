"""Examples of different plots and how to save them at identical sizes.

Every figure here is saved through the same helper, so the exported files
line up pixel for pixel regardless of what is drawn inside them.
"""

import os

import numpy as np
from matplotlib import pyplot as plt

plt.style.use("classic_mpl")

path = r"where_to_save"

#############################    Line plot    ##########################

fig = plt.figure()
fig.subplots_adjust(top=0.94, right=0.93)

plt.plot(np.random.rand(10), np.random.rand(10), "o")

plt.xlabel("Test")
plt.ylabel("Test")
plt.title("Test")

plt.savefig(os.path.join(path, "lineplot.png"))


######################    Histogram with colorbar    ###################

fig = plt.figure()
fig.subplots_adjust(top=0.94, right=0.93)

hist = plt.hist2d(np.random.rand(100), np.random.rand(100))
fig.colorbar(hist[3], fraction=0.05, pad=0.035, label="Count")

plt.xlabel("Test")
plt.ylabel("Test")
plt.title("Test")

plt.savefig(os.path.join(path, "hist2d_colorbar.png"))


######################    Line plot with inserts    ####################

fig, ax = plt.subplots()
fig.subplots_adjust(top=0.94, right=0.93)


ax.plot(np.random.rand(10), np.random.rand(10), "o")

ax_in1 = ax.inset_axes([0.3, 0.7, 0.15, 0.25])
ax_in1.plot(
    np.random.rand(5),
    np.random.rand(5),
    "--",
    color="red",
)

ax_in2 = ax.inset_axes([0.5, 0.7, 0.15, 0.25])
ax_in2.plot(
    np.random.rand(5),
    np.random.rand(5),
    "--",
    color="blue",
)

ax_in2 = ax.inset_axes([0.7, 0.7, 0.15, 0.25])
ax_in2.plot(
    np.random.rand(5),
    np.random.rand(5),
    "--",
    color="red",
)

ax.set_xlabel("Test")
ax.set_ylabel("Test")
ax.set_title("Test")

plt.savefig(os.path.join(path, "line_inserts.png"))
