import matplotlib.pyplot as plt
import matplotlib as mpl

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

fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))

plt.tight_layout()

plt.savefig("Test.png")
