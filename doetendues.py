import sys
import numpy as np
from pylab import *
import matplotlib.image as mpimg
import pandas as pd

# read data from google slides

#df = pd.read_csv("etendues.csv", comment = "#")
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrmdDf0mJD-oCCzCiXVcUyVghZlayKtH3D9Ha2wm7-od8usnnaIL9v9T3C41fP2WWoOtAnqbzD2Wvu/pub?gid=0&single=true&output=csv"
df = pd.read_csv(url, comment = "#")
df.to_csv("etendues_latest.csv")

# bubble plot
fig, ax = plt.subplots(figsize = (12, 8))#8, 7))
im = ax.scatter(df.area, df.FOV, marker = '.', s = 200 * df.etendue, c = np.log10(df.npix), edgecolor = 'none', alpha = 0.8)

# add text, small position corrections
for i in range(len(df.names)):
    alpha = 1.
    if df.names[i] == "LSST" or df.names[i] == "ZTF":
        ax.text(df.area[i], df.FOV[i], " %s" % (df.names[i]), alpha = alpha, fontsize = 14, va = 'center', ha = "center")
    elif df.names[i] in ["VST-OmegaCam", "PanSTARRS"]:
        ax.text(df.area[i], df.FOV[i] * 0.9, " %s" % (df.names[i]), alpha = alpha, fontsize = 8, va = 'center', ha = "center")        
    elif df.names[i] in ["KMTNet-CL"]:
        ax.text(df.area[i], df.FOV[i] * 0.85, " %s" % (df.names[i]), alpha = alpha, fontsize = 8, va = 'center', ha = "center")        
    elif df.names[i] in ["KMTNet-AU"]:
        ax.text(df.area[i], df.FOV[i] * 0.85**2, " %s" % (df.names[i]), alpha = alpha, fontsize = 8, va = 'center', ha = "center")        
    else:
        ax.text(df.area[i], df.FOV[i], "%s" % (df.names[i]), alpha = alpha, fontsize = 8, va = 'center', ha = "center")

# constant etendue lines
for etendue in [1, 3, 10, 30, 100, 300, 1000]:
    xs = np.array([1e-3, 3e3])
    ax.plot(xs, etendue / xs, ls = ':', c = 'gray', alpha = 0.5)
    xl = 1e-1
    ax.text(xl, etendue / xl, "%i" % etendue, rotation = -30, fontsize = 6, color = 'gray')#, ha = 'right')

# Add ALeRCE logo
img = mpimg.imread('alercelogo_small.png')
fig.figimage(img, 100, 100, zorder = 100)

# number of pixels colorbar
cb = plt.colorbar(im)
cb.set_label(r'$\log_{10}$ Number of pixels')
cb.set_alpha(1.)
cb.draw_all()

# labels
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_title("Etendue of survey telescopes (circle size)", fontsize=16)
ax.set_xlabel("light collecting area [m$^2$]", fontsize=16)
ax.set_ylabel("FOV [deg$^2$]", fontsize=16)
ax.set_xlim(0.002, 200)
ax.set_ylim(1e-1, 3e4)
plt.tight_layout()
plt.savefig("etendue.png")
plt.savefig("etendue.pdf")


# Other statistics
if len(sys.argv) > 1:
    doother = bool(sys.argv[1])
else:
    doother = False

if not doother:
    sys.exit()

# etendue fraction
fig, ax = plt.subplots()
df.sort_values(by = 'year', inplace = True)
totaletendue = df.etendue.sum()
mask = (df.location == 'CL')
total = df.etendue.cumsum()
CL = (df.etendue * mask).cumsum()

# aggregate data per year
years = df.year.unique()
etenduesCL = np.array([], dtype = float)
etenduesWorld = np.array([], dtype = float)
for yr in years:
    etenduesCL = np.append(etenduesCL, df[(df.year == yr) & (df.location == "CL")].etendue.sum())
    etenduesWorld = np.append(etenduesWorld, df[df.year == yr].etendue.sum())
fraction = np.cumsum(etenduesCL) / np.cumsum(etenduesWorld)
print(np.shape(fraction), np.shape(years))
ax.plot(years, fraction, c = 'r', label = "Chile / total", marker = '^')
ax.set_title(r"Fracción de etendue en Chile vs total", fontsize = 12)
ax.set_xlabel("Año")
ax.set_ylabel("Etendue Chile / etendue total")
ax.legend()
ax.set_xlim(2009.1, 2027.1)
LSSTyr = float(df[df.names == "LSST"].year)
ax.text(LSSTyr, fraction[years == LSSTyr], "LSST", ha = 'right', va = 'top', fontsize = 16)
plt.grid()
plt.savefig("etenduefrac.png")

# etendue and number of pixels
fig, ax = plt.subplots(figsize = (8, 6))
ax.scatter(df.etendue, df.npix)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("etendue")
ax.set_ylabel("npix [Mpix]")
ax.plot(np.linspace(1e-1, 1e3, 100), np.linspace(1e0, 1e4, 100))
plt.savefig("etenduenpix.png")
