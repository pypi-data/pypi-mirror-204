# -*-Python-*-
# Created by meneghini at 2013/05/31 08:10

from OMFITlib_dprobe import select_mag_probe_template

i = list(root["INPUTS"]["kEQDSK"].keys())[0]
df = defaultVars(kEQDSK=root["INPUTS"]["kEQDSK"][i])
sel_time = kEQDSK["IN1"]["ITIME"]

fwtmp2 = kEQDSK["IN1"]["FWTMP2"]
if isinstance(fwtmp2, sparray):
    fwtmp2 = fwtmp2.dense()


subplot(1, 2, 1)
try:
    root["INPUTS"]["gEQDSK"][sel_time].plot(only2D=True)
except KeyError:
    if "XLIM" in kEQDSK["IN1"] and "YLIM" in kEQDSK["IN1"]:
        plot(
            hstack((kEQDSK["IN1"]["XLIM"], kEQDSK["IN1"]["XLIM"][0])),
            hstack((kEQDSK["IN1"]["YLIM"], kEQDSK["IN1"]["YLIM"][0])),
            "k",
        )
if len(gca().lines):
    xlim(array(xlim()) + array([-0.3, 0.3]))
    ylim(array(ylim()) + array([-0.3, 0.3]))

fontsize = 10
scaleSizes = 50.0
a1 = max(kEQDSK["IN1"]["FWTSI"])
a2 = max(fwtmp2)
vmax = max([1, a1, a2])

dprobe = select_mag_probe_template(
    tokamak(root["SETTINGS"]["EXPERIMENT"]["device"]), kEQDSK["IN1"]["ISHOT"]
)

# get colormap
cm = get_cmap("RdYlGn")

#
# FLUX LOOPS
#
x0 = squeeze(dprobe["IN3"]["RSI"])
y0 = squeeze(dprobe["IN3"]["ZSI"])
s0 = squeeze((kEQDSK["IN1"]["COILS"] != 0) * scaleSizes)[: len(x0)]
c0 = squeeze(kEQDSK["IN1"]["FWTSI"])[: len(x0)]
x0 = x0[: len(s0)]
y0 = y0[: len(s0)]
CS = scatter(x0, y0, s=s0, c=c0, vmin=0, vmax=vmax, marker="o", cmap=cm, alpha=0.75)

for k in range(len(x0)):
    if not numpy.iterable(s0) or s0[k] > 0:
        text(
            x0[k],
            y0[k],
            "\n " + str(k + 1),
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=fontsize,
            color="w",
            zorder=1000,
            weight="bold",
        )
        text(
            x0[k],
            y0[k],
            "\n " + str(k + 1),
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=fontsize,
            color="k",
            zorder=1001,
        )

#
# MAGNETIC PROBES
#
# the magnetic probes are characterized by:
#  - XMP2 and
#  - YMP2, cartesian coordinates of the center of the probe,
#  - SMP2, size/length of the probe in meters (read below!),
#  - AMP2, angle/orientation of the probe in degrees.
#
# the usual magnetic probe in EFIT is a partial rogowski coil,
# yet beware! the EFIT D3D probe file also models saddle loops,
# which extend in the toroidal direction and provide integrated
# signals. such loops are characterized by a negative length.
#
# in order to plot non-rogowski coils correctly, a forced 90 deg
# counter-clockwise rotation has to be applied on the probe's angle.
#
# the probes are plotted with different linestyles: rogowski coils
# are plotted with segments centered around squares, whereas
# saddle loops are plotted with segments with square endpoints.
#
# FURTHER REFERENCE as explained by T. Strait on 19-jul-2016
#
# - The angle AMP2 always indicates the direction of the magnetic field
#   component that is being measured.
#
# - The length SMP2 indicates the length (in the R-Z plane) over which
#   the magnetic field is averaged by the sensor.
#
# - SMP2 > 0 indicates that the averaging length is in the direction of AMP2.
#   SMP2 < 0 indicates that the averaging length is perpendicular to AMP2.
#
# - In predicting the measurement of the sensor for purposes of fitting,
#   only the length SMP2 is considered.  The width of the sensor in the
#   direction perpendicular to SMP2 (in the R-Z plane) is small and is
#   therefore neglected.
#   Since the EFIT equilibrium is assumed to be axisymmetric, the width
#   of the sensor in the toroidal direction is not relevant.

# first, get the arrays and make sure that their dimensions match
x0 = squeeze(dprobe["IN3"]["XMP2"])
y0 = squeeze(dprobe["IN3"]["YMP2"])
l0 = squeeze(dprobe["IN3"]["SMP2"])
a0 = squeeze(dprobe["IN3"]["AMP2"])
s0 = squeeze((kEQDSK["IN1"]["EXPMP2"] != 0) * scaleSizes)[: len(x0)]
c0 = squeeze(fwtmp2)[: len(x0)]
x0 = x0[: len(s0)]
y0 = y0[: len(s0)]
l0 = l0[: len(s0)]
a0 = a0[: len(s0)]

# second, detect the negative-length probes and compute the
# 90 deg = pi/2 [rad] angle to be exploited as a correction
sgn = abs(l0) / l0
boo = (1 - sgn) / 2.0
cor = boo * pi / 2.0

# then, compute the two-point arrays to build the partial rogowskis
# as segments rather than single points, applying the correction
px = x0 - l0 / 2.0 * cos(a0 * pi / 180.0 + cor)
py = y0 - l0 / 2.0 * sin(a0 * pi / 180.0 + cor)
qx = x0 + l0 / 2.0 * cos(a0 * pi / 180.0 + cor)
qy = y0 + l0 / 2.0 * sin(a0 * pi / 180.0 + cor)

# finally, plot
for k in range(len(x0)):
    segx = [px[k], qx[k]]
    segy = [py[k], qy[k]]
    col = cm(c0[k])
    if l0[k] > 0:
        plot(segx, segy, "-", lw=2, color=col, alpha=0.75)
        plot(x0[k], y0[k], "s", color=col, alpha=0.75)
    else:
        plot(segx, segy, "s-", lw=2, color=col, alpha=0.75)

for k in range(len(x0)):
    if not numpy.iterable(s0) or s0[k] > 0:
        text(
            x0[k],
            y0[k],
            "\n " + str(k + 1),
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=fontsize,
            color="w",
            zorder=1000,
            weight="bold",
        )
        text(
            x0[k],
            y0[k],
            "\n " + str(k + 1),
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=fontsize,
            color="k",
            zorder=1001,
        )

gca().set_frame_on(False)
gca().set_aspect("equal")

subplot(1, 4, 3)
colorbar(CS).set_label("weight of the constraint")
plot(nan, nan, linestyle="", marker="o", c="gray", label="PSI loops")
plot(nan, nan, linestyle="", marker="s", c="gray", label="Mag. probes")
legend(loc=0).draggable(True)
gca().set_frame_on(False)
pyplot.setp(gca().get_xticklabels(), visible=False)
pyplot.setp(gca().get_yticklabels(), visible=False)
gca().xaxis.set_tick_params(size=0)
gca().yaxis.set_tick_params(size=0)

suptitle(
    f"Active probes location for #{kEQDSK['IN1']['ISHOT']} "
    + f"{kEQDSK['IN1']['ITIME']} ms"
)
subplots_adjust(wspace=0.0, right=1.0)
