#!/usr/bin/env python
"""
File to validate h5 files to see if the conform to various EFIT-AI standards
"""
import os
import optparse
import h5py
import f90nml
import numpy as np


dprobe_files = {}
dprobe_files["DIII-D"] = [
    "D3D_dprobe.dat",
    "D3D_dprobe_112000.dat",
    "D3D_dprobe_156000.dat",
]
dprobe_files["HL2A"] = ["HL2A_dprobe.dat"]
dprobe_files["KSTAR"] = ["KSTAR_dprobe.dat"]
dprobe_files["NSTX"] = ["NSTX_dprobe.dat"]

dprobe_minmax = {}
dprobe_minmax["DIII-D"] = {}
# Min is inclusive, Max is non-inclusive
dprobe_minmax["DIII-D"]["D3D_dprobe.dat"] = (0, 112000)
dprobe_minmax["DIII-D"]["D3D_dprobe_112000.dat"] = (112000, 156000)
dprobe_minmax["DIII-D"]["D3D_dprobe_156000.dat"] = (156000, 999999)


def get_diiid_phi():

    mpphi_dct = {}
    with open("phi_calc.txt", "r") as fh:
        for line in fh.read().split("\n"):
            if not line:
                break
            mp_name, mp_phi = line.split("#")[0].split()
            mpphi_dct[mp_name] = np.double(mp_phi)

    return mpphi_dct


def dprobe_to_machine():
    """
    Read in the dprobe files and write it out machine file
    """
    verbose = True

    for machine in dprobe_files:
        file = machine + "_machine.h5"
        if machine == "DIII-D":
            mp_phi = get_diiid_phi()

        if os.path.exists(file):
            h5io = h5py.File(file, mode="r+")
        else:
            h5io = h5py.File(file, mode="w")

        if verbose:
            print("Processing ", file)

        # This set is a python list
        i = 0
        for dfile in dprobe_files[machine]:
            in3 = f90nml.read(dfile)["IN3"]

            # See README
            fluxloop = {}
            fluxloop["R"] = in3["RSI"]
            fluxloop["Z"] = in3["ZSI"]
            lpname = in3["LPNAME"]
            ascname = [n.strip().encode("ascii", "ignore") for n in lpname]
            fluxloop["name"] = ascname

            if "RSISVS" in in3:
                vessel = {}
                vessel["resistivity_component"] = in3["RSISVS"]  # NVESSEL
                vessel["turns_per_coil"] = in3["TURNFC"]
                vsname = in3["VSNAME"]
                ascname = [n.strip().encode("ascii", "ignore") for n in vsname]
                vessel["name_component"] = ascname

            magprobe = {}
            magprobe["r_center"] = in3["XMP2"]
            magprobe["z_center"] = in3["YMP2"]
            magprobe["length"] = in3["SMP2"]
            print(len(in3["SMP2"]))
            magprobe["angle"] = in3["AMP2"]
            mpname = in3["MPNAM2"]
            ascname = [n.strip().encode("ascii", "ignore") for n in mpname]
            magprobe["name"] = ascname
            if machine == "DIII-D":
                mpphi_lst = []
                for mp in magprobe["name"]:
                    if mp in mp_phi:
                        mpphi_lst.append(mp_phi[mp])
                    else:
                        print("Probe not found: ", mp)
                        mpphi_lst.append(np.double(-0.01))
                magprobe["phi"] = mpphi_lst
            # Lang: These are the path lengths for a particular set of
            # magnetic probes that form a close loop in a poloidal plane for
            # calculations of plasma currents using Ampere’s law.
            if "PATMP2" in in3:
                magprobe["path_length"] = in3["PATMP2"]

            # Now write out the HDF5 file
            setname = "efit_set" + str(i)  # Label the sets
            h5set = h5io.create_group(setname)
            if len(dprobe_files[machine]) > 1:
                smin, smax = dprobe_minmax[machine][dfile]
            h5set.create_dataset("min_pulse_num", data=smin)
            h5set.create_dataset("max_pulse_num", data=smax)

            h5fl = h5set.create_group("flux_loop")
            for field in fluxloop:
                # print(field, fluxloop[field])
                h5fl.create_dataset(field, data=fluxloop[field])

            h5mp = h5set.create_group("magnetic_probes")
            for field in magprobe:
                # print(field, magprobe[field])
                h5mp.create_dataset(field, data=magprobe[field])

            h5vs = h5set.create_group("vessel")
            for field in vessel:
                # print(field, vessel[field])
                h5vs.create_dataset(field, data=vessel[field])

            i += 1

        h5io.close()

    return


def parse_fixargs():
    """
    Routine for parsing arguments
    """
    parser = optparse.OptionParser(usage="%prog [options])")

    parser.add_option(
        "-v", "--verbose", help="Verbose output", dest="verbose", action="store_true"
    )
    return parser


def main():
    """
    Parse arguments and options and act accordingly
    """
    parser = parse_fixargs()
    options, args = parser.parse_args()

    dprobe_to_machine()


if __name__ == "__main__":
    main()
