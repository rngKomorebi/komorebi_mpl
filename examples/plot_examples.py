"""A bunch of examples showing each style and functions available.

The functions can be used with any of the styles, but honestly it works
only with the 'night_wave' style.
"""

import numpy as np
from matplotlib import pyplot as plt

from komorebi_mpl.functions import night_wave_func

# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                           Faded scientific
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

plt.style.use("sci_faded")
plt.figure()

for i in range(7):
    plt.plot(
        np.arange(i * 10, (i + 1) * 10 + 1),
        np.sin([j for j in range(i * 10, (i + 1) * 10 + 1)]),
        label=f"{i}",
    )
plt.legend(loc="upper right")
plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("'sci_faded' style")

# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                           Pure scientific
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

plt.style.use("sci_pure")
plt.figure()

for i in range(7):
    plt.plot(
        np.arange(i * 10, (i + 1) * 10 + 1),
        np.sin([j for j in range(i * 10, (i + 1) * 10 + 1)]),
        label=f"{i}",
    )
plt.legend(loc="upper right")
plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("'sci_pure' style")

# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                          Night wave: lines
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

plt.style.use("night_wave")
plt.figure()

for i in range(7):
    plt.plot(
        np.arange(i * 10, (i + 1) * 10 + 1),
        np.sin([j for j in range(i * 10, (i + 1) * 10 + 1)]),
        label=f"{i}",
    )
plt.legend(loc="upper right")
plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("'night_wave' style")

# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                     Night wave: lines + neon glow
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

plt.style.use("night_wave")
plt.figure()

for i in range(7):
    plt.plot(
        np.arange(i * 10, (i + 1) * 10 + 1),
        np.sin([j for j in range(i * 10, (i + 1) * 10 + 1)]),
        label=f"{i}",
    )
plt.legend(loc="upper right")
plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("'night_wave' style + neon glow")

night_wave_func.make_lines_glow()

# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                Night wave: lines + neon glow + gradient
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

plt.style.use("night_wave")
plt.figure()

for i in range(7):
    plt.plot(
        np.arange(i * 10, (i + 1) * 10 + 1),
        np.sin([j for j in range(i * 10, (i + 1) * 10 + 1)]),
        label=f"{i}",
    )
plt.legend(loc="upper right")
plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("'night_wave' style + neon glow + gradient")

night_wave_func.add_glow_and_grad_fill()

# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                     Night wave: bar + gradient
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

plt.style.use("night_wave")

fig, ax = plt.subplots()
for i in range(7):
    bars = ax.bar([j + i for j in range(1)], i, width=1)
plt.xlim(0, 7)
plt.ylim(0, 7)
plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("Bars")

fig, ax = plt.subplots()
for i in range(7):
    bars = ax.bar([j + i for j in range(1)], i, width=1)
    night_wave_func.add_bar_gradient(bars, ax)
plt.xlim(0, 7)
plt.ylim(0, 7)

plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("Bars + neon gradient")

# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                     Night wave: hist + gradient
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

np.random.seed(10)
plt.style.use("night_wave")

plt.figure()
for i in range(7):
    hist = plt.hist(np.random.normal(i, 0.5, 500), bins=30)
plt.xlim(-2, 8)

plt.xlabel("Bins (-)")
plt.ylabel("Counts (-)")
plt.title("Histogram")

plt.figure()
for i in range(7):
    hist = plt.hist(np.random.normal(i, 0.5, 500), bins=30)
    night_wave_func.add_hist_gradient(hist[-1])
plt.xlim(-2, 8)

plt.xlabel("Bins (-)")
plt.ylabel("Counts (-)")
plt.title("Histogram + neon gradient")


# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<
#                     Night wave: scatter + neon
# >==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<==>==<

plt.style.use("night_wave")
np.random.seed(10)

plt.subplots()
for _ in range(5):
    plt.scatter(np.random.rand(20), np.random.rand(20), marker="s", s=50)
    night_wave_func.make_scatter_glow()

plt.xlabel("X-axis (-)")
plt.ylabel("Y-axis (-)")
plt.title("Scatter + neon glow")
