import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

"""Generalized plot attributes"""
mpl.rcParams["xtick.direction"] = "in"
mpl.rcParams["xtick.labelsize"] = "large"
mpl.rcParams["xtick.major.width"] = 1.5
mpl.rcParams["xtick.minor.width"] = 1.5
mpl.rcParams["xtick.minor.visible"] = "True"
mpl.rcParams["xtick.top"] = "True"

mpl.rcParams["ytick.direction"] = "in"
mpl.rcParams["ytick.labelsize"] = "large"
mpl.rcParams["ytick.major.width"] = 1.5
mpl.rcParams["ytick.minor.width"] = 1.5
mpl.rcParams["ytick.minor.visible"] = "True"
mpl.rcParams["ytick.right"] = "True"

mpl.rcParams["axes.grid"] = "True"
mpl.rcParams["axes.linewidth"] = 1.5
mpl.rcParams["axes.labelsize"] = "large"

x = np.arange(1, 10, 0.01)
y1 = np.sin(x)
y2 = np.sin(x+0.5)

fig, ax = plt.subplots(1, 1, figsize=(15, 4.5))
ax.plot(x, y1, lw=2.5, c="darkviolet")
ax.plot(x, y2, lw=2.5, ls="--", c="fuchsia")

plt.tight_layout()
plt.show()
