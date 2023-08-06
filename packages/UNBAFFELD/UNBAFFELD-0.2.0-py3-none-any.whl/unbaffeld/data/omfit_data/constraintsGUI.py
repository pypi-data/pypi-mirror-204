# -*-Python-*-
# Created by meneghini at 2013/05/30 09:19
# Modified by battaglia at 2018/04/02 for NSTX

import OMFITlib_general

OMFITx.TitleGUI("EFIT CONSTRAINTS GUI")
wrap = 400

key_keys = ["INPUTS", "OUTPUTS", "SETTINGS"]
pm_valid = (profiles_module is not None) and all(
    [kk in profiles_module for kk in key_keys]
)
times = OMFITlib_general.get_times("time_selector")
device = root["SETTINGS"]["EXPERIMENT"]["device"]

#


OMFITx.Tab("Magnetic")
if "kEQDSK" in root["INPUTS"] and all(
    [
        "COILS" in root["INPUTS"]["kEQDSK"][k]["IN1"]
        and "FWTMP2" in root["INPUTS"]["kEQDSK"][k]["IN1"]
        and len(root["INPUTS"]["kEQDSK"][k]["IN1"])
        for k in root["INPUTS"]["kEQDSK"].KEYS()
    ]
):
    OMFITx.CheckBox(
        "root['SETTINGS']['PHYSICS']['update_magnetic_constraint']",
        "Update magnetic constraint",
        updateGUI=True,
        default=device in ["DIII-D", "NSTX"],
    )
    if root["SETTINGS"]["PHYSICS"]["update_magnetic_constraint"]:
        if is_device(device, "DIII-D"):
            if root["INPUTS"]["kEQDSK"].values()[0]["IN1"]["ISHOT"] < 112000:
                dprobe = root["TEMPLATES"]["D3D_dprobe"]
            elif 112000 < root["INPUTS"]["kEQDSK"].values()[0]["IN1"]["ISHOT"] < 156000:
                dprobe = root["TEMPLATES"]["D3D_dprobe_112000"]
            else:
                dprobe = root["TEMPLATES"]["D3D_dprobe_156000"]
        elif is_device(device, "NSTX"):
            dprobe = root["TEMPLATES"]["NSTX_dprobe"]
        elif is_device(device, "KSTAR"):
            dprobe = root["TEMPLATES"]["KSTAR_dprobe"]
        else:
            raise RuntimeError(f"Missing dprobe.dat for device {device}")

        FluxLoop = SortedDict()
        k = 1
        while True:
            try:
                FluxLoop[
                    f"{k} - {dprobe['IN3']['LPNAME'][k-1].strip()}"
                    + " (%3.3f)"
                    % +root["INPUTS"]["kEQDSK"].values()[0]["IN1"]["FWTSI"][k - 1]
                ] = k
                k += 1
            except Exception:
                break

        MagProbe = SortedDict()
        k = 1
        while True:
            try:
                MagProbe[
                    f"{k} - {dprobe['IN3']['MPNAM2'][k-1].strip()}"
                    + " (%3.3f)"
                    % root["INPUTS"]["kEQDSK"].values()[0]["IN1"]["FWTMP2"][k - 1]
                ] = k
                k += 1
            except Exception:
                break

        OMFITx.ComboBox(
            "scratch['FluxLoopSelector']",
            FluxLoop,
            "Edit flux loop #",
            default=1,
            updateGUI=True,
        )

        OMFITx.Entry(
            "root['INPUTS']['kEQDSK']['IN1']['FWTSI'][%d]"
            % (scratch["FluxLoopSelector"] - 1),
            "Weight of channel #" + str(scratch["FluxLoopSelector"]),
        )

        OMFITx.ComboBox(
            "scratch['MagProbeSelector']",
            MagProbe,
            "Edit mag probe #",
            default=1,
            updateGUI=True,
        )

        OMFITx.Entry(
            "root['INPUTS']['kEQDSK']['IN1']['FWTMP2'][%d]"
            % (scratch["MagProbeSelector"] - 1),
            "Weight of channel #" + str(scratch["MagProbeSelector"]),
        )
    else:
        OMFITx.Label("The magnetic constraint will be the one specified in the k-file")
    OMFITx.Button(
        "Plot magnetic",
        lambda: root["PLOTS"]["plotMultiplexer"].runNoGUI(
            plotName="magneticConstraint",
            time_plot_selector=[root["SETTINGS"]["EXPERIMENT"]["TIMES"][0]],
        ),
    )


#
# MSE
#
OMFITx.Tab("MSE")

# MSE data from original kEQDSK files
mse_data_available = False
if "kEQDSK" in root["INPUTS"] and all(
    ["INS" in k and len(k["INS"]) for k in root["INPUTS"]["kEQDSK"].values()]
):
    mse_data_available = True

    descr = [""]
    if is_device(device, "DIII-D"):
        descr.extend(["30L tangential"] * 11)  # [1:11]
        descr.extend(["30L edge"] * 15)  # [12:26]
        descr.extend(["30L radial"] * 10)  # [27:36]
        descr.extend(["30L tangential"] * 9)  # [37:45]
        descr.extend(["210R core"] * 8)  # [46:53]
        descr.extend(["210R edge"] * 16)  # [54:69]
    else:
        descr.extend([""] * 1000)

    MSEchannel = SortedDict()
    # assume that the weight is the same for all times
    t0 = root["INPUTS"]["kEQDSK"].keys()[0]
    mse_weight = root["INPUTS"]["kEQDSK"][t0]["INS"]["FWTGAM"]
    for k, d in enumerate(descr):
        chan_label = f"{k}"
        if is_device(device, ("NSTX", "NSTXU")):
            chan_label = f"{k-1}"

        if k > 0 and k <= len(mse_weight):
            MSEchannel[f"{chan_label} - {d}" + " (%3.3f)" % mse_weight[k - 1]] = k

    OMFITx.ComboBox(
        "scratch['MSEchannelSelector']",
        MSEchannel,
        "Edit channel #",
        default=1,
        updateGUI=True,
    )
    # OMFITx.Entry("root['INPUTS']['kEQDSK']['INS']['TGAMMA'][%d]"%(scratch['MSEchannelSelector'] - 1), 'tan(gamma) of channel #'+str(scratch['MSEchannelSelector'])) # noqa: E501
    # OMFITx.Entry("root['INPUTS']['kEQDSK']['INS']['SGAMMA'][%d]"%(scratch['MSEchannelSelector'] - 1), 'Uncertainty of channel #'+str(scratch['MSEchannelSelector'])) # noqa: E501
    chan_label = scratch["MSEchannelSelector"] - 1
    chan_label_print = scratch["MSEchannelSelector"]
    if is_device(device, ("NSTX", "NSTXU")):
        chan_label_print = chan_label
    OMFITx.Entry(
        f"root['INPUTS']['kEQDSK']['INS']['FWTGAM'][{chan_label}]",
        f"Weight of channel #{chan_label_print}",
        updateGUI=True,
    )

    # OMFITx.Separator()
    def MSEweightMultiplier(location):
        if scratch["MSEweightMultiplier"] > 0:
            for k in root["INPUTS"]["kEQDSK"].values():
                k["INS"]["FWTGAM"] *= scratch["MSEweightMultiplier"]

            printi(
                "All MSE weights have been multiplied by %f"
                % scratch["MSEweightMultiplier"]
            )
        else:
            printe("MSE weights multiplier must be >0")
        scratch["MSEweightMultiplier"] = 1.0

    def non_zero_weight_multiplier(val):
        if not is_numeric(val):
            return False
        if not val > 0:
            return False
        return True

    OMFITx.Entry(
        "scratch['MSEweightMultiplier']",
        "Multiply all MSE weights by",
        postcommand=MSEweightMultiplier,
        updateGUI=True,
        default=1.0,
        check=non_zero_weight_multiplier,
    )

    if is_device(device, ("NSTX", "NSTX-U")):

        if pm_valid and (
            not ismodule(profiles_module, "OMFITprofiles")
            or (
                "SLICE" in profiles_module["OUTPUTS"]
                and "MSE" in profiles_module["OUTPUTS"]["SLICE"]
                and "tan_alpha" in profiles_module["OUTPUTS"]["SLICE"]["MSE"]
            )
        ):

            OMFITx.Button(
                "Load MSE data from OMFIT profiles",
                lambda: root["SCRIPTS"]["NSTX"]["MSEconstraint"].run(
                    verbose=True, apply=False
                ),
                updateGUI=False,  # Not needed because script is run in regular way
            )
            # if root['SETTINGS']['PHYSICS']['update_MSE_constraint']:
            OMFITx.CheckBox(
                "root['SETTINGS']['PHYSICS']['use_corrected_Er_MSE_data']",
                "Correct MSE for Radial Electric Field",
                default=True,
                updateGUI=True,
                help="Use Radial Electric Field to Correct MSE Pitch Angles"
                     + "(applied on EFIT execution)",
            )
            if root["SETTINGS"]["PHYSICS"]["use_corrected_Er_MSE_data"]:
                # Omega tor fit
                omfp_keys = []
                omfp_lab = []
                if (
                    ismodule(profiles_module, "OMFITprofiles")
                    and "DERIVED" in profiles_module["OUTPUTS"]
                ):
                    omfp_keys = [
                        "profiles_module['OUTPUTS']['FIT']['{}']".format(k)
                        for k in profiles_module["OUTPUTS"]["FIT"]
                        if re.match("omega_tor_*", k)
                    ]
                    omfp_lab = [
                        "High Rotation: {}".format(omfp_keys[i])
                        for i in range(len(omfp_keys))
                    ]
                # Omega E derived
                ome_keys = []
                ome_lab = []
                if (
                    ismodule(profiles_module, "OMFITprofiles")
                    and "DERIVED" in profiles_module["OUTPUTS"]
                ):
                    ome_keys = [
                        "profiles_module['OUTPUTS']['DERIVED']['{}']".format(k)
                        for k in profiles_module["OUTPUTS"]["DERIVED"]
                        if re.match("omega_E_*", k)
                    ]
                    ome_lab = [
                        "Er: {}".format(ome_keys[i]) for i in range(len(ome_keys))
                    ]
                # Corrected MSE on MDS+ tree derived using EFIT02
                cor_keys = []
                cor_lab = []
                if "SLICE" in OMFITprofiles["OUTPUTS"]:
                    cor_keys = [
                        "OMFITprofiles['OUTPUTS']['SLICE']['MSE']['{}']".format(k)
                        for k in OMFITprofiles["OUTPUTS"]["SLICE"]["MSE"]
                        if re.match("tan_alpha_cor", k)
                    ]
                    cor_lab = [
                        "Values from MSE Tree: {}".format(cor_keys[i])
                        for i in range(len(cor_keys))
                    ]
                # Option TRANSP (to be added)
                # Option GAprofiles (to be added)
                # Option NEO (to be added)
                if len(omfp_keys) or len(ome_keys) or len(cor_keys):
                    labs = omfp_lab + ome_lab + cor_lab
                    keys = omfp_keys + ome_keys + cor_keys
                    opt = dict(list(zip(labs, keys)))
                    OMFITx.ComboBox(
                        "root['SETTINGS']['PHYSICS']['source_Er_MSE']",
                        opt,
                        "",
                        updateGUI=True,
                        default=keys[0],
                        help="Values from MSE Tree: Correction saved to MDS+ "
                             + "sing CHERS and EFIT02. Or use OMFITprofile fits "
                             + "(Vtor or Er) to compute a self-consistent "
                             + "correction with EFIT solution.",
                    )
                else:
                    OMFITx.Label("No Valid Options for Radial Electric Field")
                OMFITx.Button(
                    "Preview MSE Data and Correction",
                    lambda: root["SCRIPTS"]["MSEerCorrection"].run(
                        verbose=True, doplot=True, apply=False
                    ),
                )

    if is_device(device, "KSTAR"):
        OMFITx.Entry(
            "scratch['sgamma_adjust']",
            "Replace all SGAMMA by",
            updateGUI=False,
            default=0.02,
        )
        with OMFITx.same_row():
            OMFITx.Button(
                "Adjust sgamma in k-files",
                "root['SCRIPTS']['KSTAR']['forceSgamma'].runNoGUI",
            )
            OMFITx.Button(
                "Rewind sgamma to MDS value",
                lambda: root["SCRIPTS"]["KSTAR"]["forceSgamma"].run(reset=True),
            )

    # Er correction in DIII-D
    if is_device(device, ["DIII-D", "KSTAR"]):
        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['use_corrected_Er_MSE_data']",
            "Correct MSE for Radial Electric Field",
            default=False,
            updateGUI=True,
            help="Use Radial Electric Field to Correct MSE Pitch Angles"
                 + " (applied on EFIT execution)",
        )
        if root["SETTINGS"]["PHYSICS"]["use_corrected_Er_MSE_data"]:
            options = SortedDict()
            # collect all fit toroidal rotations (could have multiple ions)
            if pm_valid:
                omegas = [
                    k
                    for k in profiles_module["OUTPUTS"].get("FIT", {})
                    if re.match("omega_tor_*", k)
                ]
                for omega in omegas:
                    options[
                        "High Rotation: {:}".format(omega)
                    ] = "profiles_module['OUTPUTS']['FIT']['{}']".format(omega)
                # collect all derived omega_E profiles (if they exist)
                omega_Es = [
                    k
                    for k in profiles_module["OUTPUTS"].get("DERIVED", {})
                    if re.match("omega_E_*", k)
                ]
                for omega in omega_Es:
                    options[
                        "Full Er Correction: {:}".format(omega)
                    ] = "profiles_module['OUTPUTS']['DERIVED']['{}']".format(omega)
            # if we have a valid rotation profile, then enable the selection
            # Option TRANSP (to be added)
            # Option GAprofiles (to be added)
            # Option NEO (to be added)
            if len(options) > 0:
                OMFITx.ComboBox(
                    "root['SETTINGS']['PHYSICS']['source_Er_MSE']",
                    options,
                    "Source",
                    updateGUI=True,
                    default=list(options.values())[0],
                )
            else:
                OMFITx.Label("No Valid Options for Radial Electric Field")
            OMFITx.Button(
                "Preview MSE Data and Correction",
                lambda: root["SCRIPTS"]["MSEerCorrection"].run(
                    verbose=True, doplot=True, apply=False
                ),
            )

    OMFITx.Separator("Plot MSE data")
    OMFITx.Button(
        "Plot MSE data in k-Files", "root['PLOTS']['plotMSEkfiles'].plotFigure"
    )
    OMFITx.Button("Plot MSE measurements", "root['PLOTS']['plot_mse'].plotFigure")

    # this is convenient to have here when doing kineticEFITtime iterations
    if len(root["OUTPUTS"].get("gEQDSK", [])) > 0:
        OMFITx.Separator()
        OMFITx.Button(
            "Plot MSE error and current for current OUTPUTS",
            lambda: root["PLOTS"]["MSEerror"].plotFigure(plot_times=times),
        )
# For NSTX MSE data from OMFITprofiles

# Not supported devices
elif not mse_data_available:
    OMFITx.Label("MSE constraint not available", width=50)

#
# BOUNDARY
#
OMFITx.Tab("Boundary")


def update_fixed_bdry(location):
    if root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] == "OMFITprofiles":
        root["SETTINGS"]["PHYSICS"]["fix_boundary_to"] = "OMFITprofiles"
    elif root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] == "mds":
        root["SETTINGS"]["PHYSICS"]["fix_boundary_to"] = "EFIT01"
    elif root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] == "tree":
        root["SETTINGS"]["PHYSICS"]["fix_boundary_to"] = ""
    else:
        root["SETTINGS"]["PHYSICS"]["fix_boundary_to"] = ""


if root["SETTINGS"]["PHYSICS"]["fix_boundary_to"] == "OMFITprofiles":
    root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] = "OMFITprofiles"
elif (
    "OMFIT" in root["SETTINGS"]["PHYSICS"]["fix_boundary_to"]
    or "[" in root["SETTINGS"]["PHYSICS"]["fix_boundary_to"]
):
    root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] = "tree"
elif "EFIT" in root["SETTINGS"]["PHYSICS"]["fix_boundary_to"]:
    root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] = "mds"

separatrix_constraints = []
if pm_valid and "DIAGNOSTICS" in profiles_module["OUTPUTS"]:
    for k in profiles_module["OUTPUTS"]["DIAGNOSTICS"]:
        if "separatrix" in profiles_module["OUTPUTS"]["DIAGNOSTICS"][k]:
            separatrix_constraints.append(
                (
                    k,
                    profiles_module["OUTPUTS"]["DIAGNOSTICS"][k]["separatrix"][
                        "subsystem"
                    ].values,
                )
            )

options = SortedDict()
if not is_device(device, "HL-2A"):
    options["EFIT from MDSplus"] = "mds"
options["G-files in the tree"] = "tree"
options["profils_module boundary"] = "OMFITprofiles"
if len(separatrix_constraints):
    options["profils_module separatrix constraints"] = ""
else:
    options["None: do not fix boundary"] = ""

OMFITx.ComboBox(
    "root['SETTINGS']['PHYSICS']['fixed_boundary_source']",
    options,
    "Source for boundary constraint",
    default="",
    updateGUI=True,
    postcommand=update_fixed_bdry,
    help="Selecting anything other than \"None\" will impose a fixed boundary "
         + "constraint on EFIT. To use an OMFITprofiles-based boundary constraint, "
         + "you must load OMFITprofiles, set a dependency, and run appropriate scripts "
         + "to form raw EQ data. To use EFITs in the tree, you must get a G-file "
         + "collection into the tree somehow. Sourcing from MDSplus requires no "
         + "special setup; just make sure the tree you try to collect from exists.",
)

if root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] == "mds":
    OMFITx.ComboBox(
        "root['SETTINGS']['PHYSICS']['fix_boundary_to']",
        available_EFITs(
            scratch, device=device, shot=root["SETTINGS"]["EXPERIMENT"]["shot"]
        )[0],
        "Get EFIT boundary from",
        state=normal,
        default="EFIT01",
        help="Pick a valid MDSplus EFIT tree as a source for a fixed "
             + "boundary constraint.",
    )

elif root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] == "tree":
    OMFITx.TreeLocationPicker(
        "root['SETTINGS']['PHYSICS']['fix_boundary_to']",
        "Tree location of G-file collection",
        default="",
        help="Pick a set of G-files (the parent of the G-files, not any one individual "
        "G-file) to use as a source for a fixed boundary constraint.",
    )

if separatrix_constraints:

    def set_bc():
        root["SETTINGS"]["PHYSICS"]["boundary_constraints"] = []
        for k, subsystems in separatrix_constraints:
            for subsystem in subsystems:
                if (
                    "bc_%s_%s" % (k, subsystem) in scratch
                    and scratch["bc_%s_%s" % (k, subsystem)]
                ):
                    root["SETTINGS"]["PHYSICS"]["boundary_constraints"].extend(
                        (k, subsystem)
                    )

    def get_bc(k1, subsystem1):
        if "boundary_constraints" in root["SETTINGS"]["PHYSICS"]:
            if root["SETTINGS"]["PHYSICS"]["boundary_constraints"] is True:
                return True
            elif root["SETTINGS"]["PHYSICS"]["boundary_constraints"] is False:
                return False
            elif root["SETTINGS"]["PHYSICS"][
                "boundary_constraints"
            ] is not None and len(root["SETTINGS"]["PHYSICS"]["boundary_constraints"]):
                for k, subsystem in reshape(
                    root["SETTINGS"]["PHYSICS"]["boundary_constraints"], (-1, 2)
                ):
                    if k == k1 and subsystem == subsystem1:
                        return True
        return False

    for k, subsystems in separatrix_constraints:
        for subsystem in subsystems:
            OMFITx.CheckBox(
                "scratch['bc_%s_%s']" % (k, subsystem),
                k + " " + subsystem,
                default=get_bc(k, subsystem),
                postcommand=lambda location: set_bc(),
                updateGUI=True,
            )

    set_bc()
else:
    root["SETTINGS"]["PHYSICS"]["boundary_constraints"] = False

if root["SETTINGS"]["PHYSICS"]["fixed_boundary_source"] == "mds":
    OMFITx.Label(" Fix only extrema from MDS value", align="left")
    with OMFITx.same_row():
        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['fix_extrema']['fix_R_max']", "Rmax"
        )
        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['fix_extrema']['fix_R_min']", "Rmin"
        )
        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['fix_extrema']['fix_Z_max']", "Zmax"
        )
        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['fix_extrema']['fix_Z_min']", "Zmin"
        )
    OMFITx.Button("Check boundary difference", root["PLOTS"]["boundaryCheck"].runNoGUI)

#
# PRESSURE
#
OMFITx.Tab("Pressure")
_statefile = interface(statefile)
if _statefile is not None:
    OMFITx.CheckBox(
        "root['SETTINGS']['PHYSICS']['update_pressure_constraint']",
        "Update pressure constraint",
        updateGUI=True,
    )
    if root["SETTINGS"]["PHYSICS"]["update_pressure_constraint"]:
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['npoints_pressure_constraint']",
            "Number of points (max 200)",
            default=100,
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['pressure_constraint_location']",
            "Bias points towards edge (+) or Core (-)",
            default=0,
        )
        OMFITx.Label("p=a*Ptot+b*Pbeam+c")
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['sigpre_factor']",
            "Uncertainty as fraction of total pressure",
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['beam_sigpre']",
            "Uncertainty as fraction of fast-ion pressure",
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['min_sigpre']",
            "Minimum pressure uncertainty [N/m^2]",
        )
        OMFITx.Button(
            "Preview pressure constraint",
            "root['SCRIPTS']['pressureConstraint'].runNoGUI",
        )
    else:
        OMFITx.Label("Pressure constraint as per specification in the k-file")

        def remove_pressure(location=None):
            loc = root["INPUTS"]["kEQDSK"]
            ts = list(loc.keys())
            for j, t in enumerate(ts):
                pvars = [
                    "RPRESS",
                    "PRESSR",
                    "SIGPRE",
                    "FWTPRE",
                    "NPRESS",
                    "NBEAM",
                    "SIBEAM",
                    "PBEAM",
                    "DNBEAM",
                    "DMASS",
                    "NMASS",
                    "KPRFIT",
                    "NDOKIN",
                ]
                for pvar in pvars:
                    if pvar in loc[t]["IN1"]:
                        del loc[t]["IN1"][pvar]
            print("Pressure constraints removed from kfiles")

        OMFITx.Button("Remove pressure constraints", remove_pressure)
else:
    OMFITx.Label(
        "Pressure constraint is missing.\n\nDefine `statefile` in the DEPENDENCIES of "
        + rootName
        + " module to enable handling of pressure constraints",
        width=50,
        wrap=wrap,
    )
    if is_device(device, "KSTAR"):
        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['pressure_constraint_from_MDS']",
            "Use constraint from the MDS node",
            default=False,
            updateGUI=True,
            help="Apply pressure constraint with data from MDS EFIT node",
        )
        if root["SETTINGS"]["PHYSICS"]["pressure_constraint_from_MDS"]:
            OMFITx.Entry(
                "scratch['psi_p_constraint']",
                "Psi_n for p constraint",
                updateGUI=True,
                default=[0.0, 0.2, 0.4, 0.97, 0.999],
            )
            with OMFITx.same_row():
                OMFITx.Button(
                    "Apply P constraint",
                    "root['SCRIPTS']['KSTAR']['constraint_KSTAR'].runNoGUI",
                    width=20,
                )
                OMFITx.Button(
                    "Remove applied constraint",
                    lambda: root["SCRIPTS"]["KSTAR"]["constraint_KSTAR"].run(
                        reset=True
                    ),
                    width=20,
                )

#
# CURRENT
#
OMFITx.Tab("Current")
if _statefile is not None:
    mp = [False, root["SETTINGS"]["PHYSICS"]["update_current_constraint"]]
    if not root["SETTINGS"]["PHYSICS"]["update_current_constraint"]:
        mp = [False, 1.0]
    OMFITx.CheckBox(
        "root['SETTINGS']['PHYSICS']['update_current_constraint']",
        "Update current constraint",
        updateGUI=True,
        mapFalseTrue=mp,
    )
    if root["SETTINGS"]["PHYSICS"]["update_current_constraint"]:
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['JohMul']",
            "OH current multiplier",
            default=1.0,
        )
        OMFITx.ComboBox(
            "root['SETTINGS']['PHYSICS']['jboot_source']",
            ["statefile", "OMFITprofiles"],
            "Bootstrap source",
            default="statefile",
            updateGUI=True,
        )
        if root["SETTINGS"]["PHYSICS"]["jboot_source"] == "OMFITprofiles":
            OMFITx.Entry(
                "root['SETTINGS']['PHYSICS']['sigma_Jboot_fac']",
                "Sigma added to bootstrap current ",
                default=0.0,
                help="Adds this number of the OMFITprofiles DERIVED "
                     + "\njboot standard deviations to the nominal value.\n"
                     + "This is done prior to application of the multiplier",
            )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['JbootMul']",
            "Bootstrap current multiplier",
            default=1.0,
        )
        max_points = " (max ? pts)"
        if is_device(device, "DIII-D"):
            max_points = " (max 61 pts)"
        elif is_device(device, ("NSTX", "NSTX-U")):
            max_points = " (max 23 pts)"
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['npoints_current_constraint']",
            "Number of points" + max_points,
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['current_constraint_location']",
            "Bias points towards edge (+) or Core (-)",
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['update_current_constraint']",
            "Weight of current constraint",
            default=1.0,
            check=is_numeric,
            updateGUI=True,
        )
        OMFITx.Button(
            "Preview current constraint",
            "root['SCRIPTS']['currentConstraint'].runNoGUI",
        )
    else:
        OMFITx.Label("Current constraint as per specification in the k-file")

        def remove_current(location=None):
            loc = root["INPUTS"]["kEQDSK"]
            ts = list(loc.keys())
            for j, t in enumerate(ts):
                cvars1 = ["KZEROJ", "RZEROJ"]
                for cvar in cvars1:
                    if cvar in loc[t]["IN1"]:
                        del loc[t]["IN1"][cvar]
                cvars2 = ["SIZEROJ", "VZEROJ", "FWTXXJ"]
                for cvar in cvars2:
                    if cvar in loc[t]["INWANT"]:
                        del loc[t]["INWANT"][cvar]
            print("Current constraints removed from kfiles")

        OMFITx.Button("Remove current constraints", remove_current)
else:
    OMFITx.Label(
        "Current constraint is missing.\n\nDefine `statefile` in the DEPENDENCIES of "
        + rootName
        + " module to enable handling of current constraints",
        width=50,
        wrap=wrap,
    )

#
# SAFETY FACTOR
#
OMFITx.Tab("q")
opt = {"Disabled": False}
help = """
Constant value or string that is evaluated as function of `time`
e.g. -0.003198*time + 5.36869
"""
OMFITx.ComboBox(
    "root['SETTINGS']['PHYSICS']['q0']",
    opt,
    "|q| on axis",
    default=False,
    state="normal",
    help=help,
)


def check_qmin(x):
    condition = []
    for time in times:
        q0 = root["SETTINGS"]["PHYSICS"]["q0"]
        if isinstance(root["SETTINGS"]["PHYSICS"]["q0"], str):
            q0 = eval(root["SETTINGS"]["PHYSICS"]["q0"])
        qmin = x
        if isinstance(x, str):
            qmin = eval(x)
        condition.append(qmin < q0)
    return all(condition)


OMFITx.ComboBox(
    "root['SETTINGS']['PHYSICS']['qmin']",
    opt,
    "|q| min",
    default=False,
    state="normal",
    check=check_qmin,
    help="""
|q|_min < |q|_0

Constant value or string that is evaluated as function of `time`
e.g. -0.003198*time + 5.51869
""",
    updateGUI=True,
)

if root["SETTINGS"]["PHYSICS"]["qmin"]:
    OMFITx.Label("NOTE: |q|_min constraint requires multiple EFIT runs", align="left")


def remove_q_constraints(location=None):
    loc = root["INPUTS"]["kEQDSK"]
    ts = list(loc.keys())
    for j, t in enumerate(ts):
        qvars = ["QVFIT", "FWTQA"]
        for qvar in qvars:
            if qvar in loc[t]["IN1"]:
                del loc[t]["IN1"][qvar]
    print("q constraints removed from kfiles")


OMFITx.Button("Remove q constraints", remove_q_constraints)


def remove_isotherm_constraints(location=None):

    for k in times:
        if "INECE" in root["INPUTS"]["kEQDSK"][k]:
            del root["INPUTS"]["kEQDSK"][k]["INECE"]
            del root["INPUTS"]["kEQDSK"][k]["IN1"]["NBDRY"]
    # set it to False, because else the constrain will be
    # applied again in runEFITtime.py
    root["SETTINGS"]["PHYSICS"]["update_isote_constraint"] = False
    printi("Isothermal constrains were removed from k-files")


if is_device(device, ["NSTX", "NSTX-U"]):
    #
    # ECE (isothermal constrants)
    #

    OMFITx.Tab("Isothermal constraints")

    OMFITx.CheckBox(
        "root['SETTINGS']['PHYSICS']['update_isote_constraint']",
        "Update isothermal constraint",
        updateGUI=True,
        default=True,
    )
    if root["SETTINGS"]["PHYSICS"]["update_isote_constraint"]:

        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['TEMID']",
            "TEMID",
            default=200,
            help="location of Te isothermal constrain",
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['N_TEMID']",
            "N constrains",
            default=3,
            help="Number of HFS channels with Te > TEMID used as constrain",
        )

        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['use_MSE_axis']",
            "Constrain location of mag. axis from MSE data",
            default=True,
            help="use zero crossing of MSE data to estimate R "
            + "location of magnetic axis",
        )

        OMFITx.CheckBox(
            "root['SETTINGS']['PHYSICS']['Te_sepx_use']",
            "Constrain location of LFS separatrix",
            default=True,
            updateGUI=True,
        )

        if root["SETTINGS"]["PHYSICS"]["Te_sepx_use"]:
            OMFITx.Entry(
                "root['SETTINGS']['PHYSICS']['TESEP']",
                "TESEP",
                default=60,
                help="Te separatrixe temperature constraint",
            )

        OMFITx.Button(
            "Preview constraints",
            "root['SCRIPTS']['isothermal_constraint'].runNoGUI",
            updateGUI=True,
        )

    else:
        OMFITx.Label("Isothermal constraint as per specification in the k-file")

    if any(["INECE" in root["INPUTS"]["kEQDSK"][k] for k in times]):
        OMFITx.Button(
            "Remove constraints from k-file",
            remove_isotherm_constraints,
            updateGUI=True,
        )

#
# Rotation
#
OMFITx.Tab("Rotation")

if _statefile is not None:
    OMFITx.CheckBox(
        "root['SETTINGS']['PHYSICS']['update_rotation_constraint']",
        "Update rotation constraint",
        updateGUI=True,
    )
    if (
        root["SETTINGS"]["PHYSICS"]["update_rotation_constraint"]
        and not root["SETTINGS"]["PHYSICS"]["efit_ai"]
    ):
        rotation_options = {
            " no rotation (default)": 0,
            "Approximate first order form": 1,
            "include second order terms": 2,
            "exact two-fluid form": 3,
        }
        OMFITx.ComboBox(
            "root['SETTINGS']['PHYSICS']['rotation_model']",
            rotation_options,
            "Rotation Model",
            default=1,
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['rotation_nedge']",
            "Number of points near edge to skip",
            default=10,
        )
        OMFITx.Entry(
            "root['SETTINGS']['PHYSICS']['rotation_rel_sigma_min']",
            "Minimum uncertainty fraction on rotation",
            default=0.05,
        )
        OMFITx.Button("Preview constraints", "root['SCRIPTS']['rotationConstraint']")

    else:
        OMFITx.Label("Pressure constraint as per specification in the k-file")

        def remove_rotation(location=None):
            loc = root["INPUTS"]["kEQDSK"]
            ts = list(loc.keys())
            for j, t in enumerate(ts):
                loc[t]["IN1"]["KPRFIT"] = 1
                loc[t]["IN1"]["ICURRT"] = 2
                if "INVT" in loc[t]:
                    del loc[t]["INVT"]
            print("Remove rotation constraints removed from kfiles")

        OMFITx.Button("Remove rotation constraints", remove_rotation)

else:
    OMFITx.Label(
        "Pressure constraint is missing.\n\nDefine `statefile` in the DEPENDENCIES of "
        + rootName
        + " module to enable handling of pressure constraints",
        width=50,
        wrap=wrap,
    )
