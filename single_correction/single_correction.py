import sys
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

import os

from global_coupling3 import get_corrections
from global_coupling3 import create_model_and_response
from global_coupling3 import _change_value

from plot_single_correction import plot_single_correction


#get a base_script
#make a model
#make a responsematrix

LHC_PATH = f"/home/eirik/CERN/lhc2018/2018/"
OUTPUTFILE_DIR = "outputfiles/"
BASE_SCRIPT_DIR = "/home/eirik/CERN/global_coupling_correction3/base_scripts/"
BASE_SCRIPT = f"{BASE_SCRIPT_DIR}single_correction.madx"
OPTICSFILE = "opticsfile.1"
QX = 0.31
QY = 0.32
QX_DRIVEN = 0.30
QY_DRIVEN = 0.332
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/single_correction/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}"
ACCEL_SETTINGS = dict(ats=True,beam=1, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=0.45)

#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN, variable_categories=["squeeze_knobs"])



CHANGE_DICT = {"%correct" : "0",
	"%lhc_path" : LHC_PATH,
	"%opticsfile" :   OPTICSFILE,
	"%knob_Re_value" :  "0.",
	"%knob_Im_value" :  "0.",
	"%error_component" :  "quadrupole",
	"%error_strength" :  "0.00002*gauss()",
	"%pattern_1" :  ".",
	"%pattern_2" :  ".",
	"%quad_component" :  "quadrupole",
	"%quad_pattern_1" :  "R5",
	"%quad_pattern_2" :  "R5",
	"%quad_strength" :  "0.",
	"%twiss_pattern" :  "BPM",
	"%colknob1" :  "5.",
	"%colknob5" :  "0.",
	"%percentage" :  "0.99",
	"%QX" :  "62.31",
	"%QY" :  "60.32"}



#get_corrections(BASE_SCRIPT , CHANGE_DICT, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, iterations=1)
#plot_single_correction(OUTPUTFILE_DIR, "correction_pickle", "closed_bump.pdf",MODEL_DIR)

BASE_SCRIPT_EALIGN = f"{BASE_SCRIPT_DIR}ealign_mcs.madx"
CHANGE_DICT_EALIGN = {"%correct" : "0",
        "%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%twiss_pattern" :  "BPM",
        "%QX" :  "62.31",
        "%QY" :  "60.32",
        "%DX" : "0.",
        "%DY" : "0.0004"}

#get_corrections(BASE_SCRIPT_EALIGN , CHANGE_DICT_EALIGN, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS,variable_categories=["MQSORG"], pickle_name = "correction_pickle2",iterations=1)

#plot_single_correction(OUTPUTFILE_DIR, "correction_pickle2", "ealign.pdf")


#error 2015

BASE_SCRIPT_2015 = f"{BASE_SCRIPT_DIR}error2015.madx"
CHANGE_DICT_2015 = {"%correct" : "0",
        "%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%twiss_pattern" :  "BPM",
        "%QX" :  "62.31",
        "%QY" :  "60.32"
        }
        
        

#get_corrections(BASE_SCRIPT_2015 , CHANGE_DICT_2015, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = "correction_pickle3",iterations=1)

#plot_single_correction(OUTPUTFILE_DIR, "correction_pickle3", "error2015.pdf")

BASE_SCRIPT_EALIGN_CORRECTED_EFFCOMP = f"{BASE_SCRIPT_DIR}ealign_mcs_corrected_EFFCOMP.madx"
CHANGE_DICT_EALIGN_CORRECTED_ONESOURCE = {"%correct" : "0",
	"%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%twiss_pattern" :  "BPM",
        "%QX" :  "62.31",
        "%QY" :  "60.32",
        "%DX" : "0.",
        "%DY" : "0.0004",
        "%error_component" :  "quadrupole",
	"%error_strength" :  "0.000001*gauss()",
	"%pattern_1" :  ".",
	"%pattern_2" :  ".",
	"%quad_component" :  "quadrupole",
	"%quad_pattern_1" :  "R5",
	"%quad_pattern_2" :  "R5",


	"%quad_strength" :  "0.",
	"%twiss_pattern" :  "BPM"}

#get_corrections(BASE_SCRIPT_EALIGN_CORRECTED_EFFCOMP , CHANGE_DICT_EALIGN_CORRECTED_GAUSS, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = "correction_pickle",iterations=1)

#plot_single_correction(OUTPUTFILE_DIR, "correction_pickle", "ealign_corrected_random_gauss.pdf")

BASE_SCRIPT_EALIGN_CORRECTED_EFFCOMP = f"{BASE_SCRIPT_DIR}ealign_mcs_corrected_EFFCOMP.madx"
CHANGE_DICT_EALIGN_CORRECTED_SINGLESOURCE = {"%correct" : "0",
	"%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%twiss_pattern" :  "BPM",
        "%QX" :  "62.31",
        "%QY" :  "60.32",
        "%DX" : "0.",
        "%DY" : "0.0004",
        "%error_component" :  "quadrupole",
	"%error_strength" :  "0.0004",
	"%pattern_1" :  "MQ.18R2.B1",
	"%pattern_2" :  "MQ.18R2.B1",
	"%quad_component" :  "quadrupole",
	"%quad_pattern_1" :  "R5",
	"%quad_pattern_2" :  "R5",
	"%quad_strength" :  "0.000006",
	"%twiss_pattern" :  "BPM"}

#get_corrections(BASE_SCRIPT_EALIGN_CORRECTED_EFFCOMP , CHANGE_DICT_EALIGN_CORRECTED_SINGLESOURCE, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = "correction_pickle",iterations=1)

plot_single_correction(OUTPUTFILE_DIR, "correction_pickle", "ealign_corrected_single_source.pdf",MODEL_DIR)


BASE_SCRIPT_EALIGN_CORRECTED_TILT = f"{BASE_SCRIPT_DIR}ealign_mcs_corrected_TripletTilt.madx"
CHANGE_DICT_EALIGN_CORRECTED_TILT = {"%correct" : "0",
	"%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%twiss_pattern" :  "BPM",
        "%QX" :  "62.31",
        "%QY" :  "60.32",
        "%DX" : "0.",
        "%DY" : "0.0004",
    	"%PATTERN_TRIPLET" : "MQX.*R1",
    	"%DPSI" : "0.0007",
	"%quad_component" :  "quadrupole",
	"%quad_pattern_1" :  "R5",
	"%quad_pattern_2" :  "R5",
	"%quad_strength" :  "0.",
	"%twiss_pattern" :  "BPM"}

#get_corrections(BASE_SCRIPT_EALIGN_CORRECTED_TILT , CHANGE_DICT_EALIGN_CORRECTED_TILT, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = "correction_pickle",iterations=1)

#plot_single_correction(OUTPUTFILE_DIR, "correction_pickle", "ealign_corrected_tilt.pdf")



















