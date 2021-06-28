import sys
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')
sys.path.append('/home/eirik/CERN/global_coupling_correction3/single_correction/')
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
BASE_SCRIPT = f"{BASE_SCRIPT_DIR}ealign_mcs.madx"
OPTICSFILE = "opticsfile.22"
QX = 0.31
QY = 0.32
QX_DRIVEN = 0.30 
QY_DRIVEN = 0.332
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/KQS_correction/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}"
ACCEL_SETTINGS = dict(ats=True ,beam=1, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=0.45)

#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN,variable_categories = ["MQSORG"])


CHANGE_DICT = {"%correct" : "0",
	"%lhc_path" : LHC_PATH,
	"%opticsfile" :   OPTICSFILE,
	"%twiss_pattern" :  "BPM",
	"%QX" :  "62.31",
	"%QY" :  "60.32",
	"%DX" : "0.",
	"%DY" : "0.0004"}
PICKLE_NAME_EALIGN = "correction_pickle_ealign"


get_corrections(BASE_SCRIPT , CHANGE_DICT, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS,variable_categories = ["MQSORG"], pickle_name = PICKLE_NAME_EALIGN, iterations=3)

plot_single_correction(OUTPUTFILE_DIR, PICKLE_NAME_EALIGN, "triple_correction_MQSORG.pdf", MODEL_DIR)
