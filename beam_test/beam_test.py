import sys
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')
sys.path.append('/home/eirik/CERN/global_coupling_correction3/single_correction/')
import os

from global_coupling3 import get_corrections
from global_coupling3 import create_model_and_response
from global_coupling3 import _change_value

from plot_single_correction import plot_single_correction

from plot_beam_test import plot_beam_test

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
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/beam_test/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}"
ACCEL_SETTINGS = dict(ats=True,beam=1, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=0.45)




#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN, variable_categories=["squeeze_knobs"],PROTON="PROTON_runIII")


BASE_SCRIPT_UNCORECTED_LOCAL = f"{BASE_SCRIPT_DIR}uncorected_local.madx"


CHANGE_DICT_EALIGN_UNCORECTED_LOCAL = {
        "%correct" : "0",
	"%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%twiss_pattern" :  "BPM",
        "%QX" :  str(62 + QX),
        "%QY" :  str(60 + QY),
	"%twiss_pattern" :  "BPM"}

get_corrections(BASE_SCRIPT_UNCORECTED_LOCAL , CHANGE_DICT_EALIGN_UNCORECTED_LOCAL, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS,variable_categories=["squeeze_knobs"] ,pickle_name = "correction_pickle",iterations=0)

plot_single_correction(OUTPUTFILE_DIR, "correction_pickle", f"uncorected_IP_{OPTICSFILE}_knobs{QX}{QY}.pdf",MODEL_DIR)


BASE_SCRIPT_UNCORECTED_LOCAL_INJECTIONCOR = f"{BASE_SCRIPT_DIR}uncorected_local_injectionCor.madx"


#get_corrections(BASE_SCRIPT_UNCORECTED_LOCAL_INJECTIONCOR , CHANGE_DICT_EALIGN_UNCORECTED_LOCAL, RESPONSEMATRIX, OUTPUTFILE_DIR, 			 		    ACCEL_SETTINGS,variable_categories=["squeeze_knobs"] ,pickle_name = "correction_pickle",iterations=1)

#plot_single_correction(OUTPUTFILE_DIR, "correction_pickle", f"TESTinjectionCor_IP_{OPTICSFILE}_knobs{QX}{QY}.pdf",MODEL_DIR)

def beam_test(optics,pickle_name,base_script):
	for i in optics:
		OPTICSFILE = f"opticsfile.{i}"
		pickle_name_local = f"{pickle_name}{OPTICSFILE}"
		
		MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}/"
		RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}"
		ACCEL_SETTINGS = dict(ats=True,beam=1, model_dir=MODEL_DIR,
		              year="2018", accel="lhc", energy=0.45)
		           
		CHANGE_DICT_EALIGN_UNCORECTED_LOCAL = {
			"%correct" : "0",
			"%lhc_path" : LHC_PATH,
			"%opticsfile" :   OPTICSFILE,
			"%twiss_pattern" :  "BPM",
			"%QX" :  str(62 + QX),
			"%QY" :  str(60 + QY),
			"%twiss_pattern" :  "BPM"}              
		#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY,variable_categories=["squeeze_knobs"],PROTON="PROTON_runIII")
		
		get_corrections(base_script , CHANGE_DICT_EALIGN_UNCORECTED_LOCAL, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS,variable_categories=["squeeze_knobs"] ,pickle_name = 				pickle_name_local,iterations=0)

pickle_name = "uncorected_local"
optics = [1,5,9,12]
#beam_test(optics,pickle_name,BASE_SCRIPT_UNCORECTED_LOCAL)
plot_beam_test(OUTPUTFILE_DIR,pickle_name,optics,"without correction","without_correction.pdf")

pickle_name = "corected_local"
#beam_test(optics,pickle_name,BASE_SCRIPT_UNCORECTED_LOCAL_INJECTIONCOR)
plot_beam_test(OUTPUTFILE_DIR,pickle_name,optics,"correction at injection","correctedInjection.pdf")
#/afs/cern.ch/eng/lhc/optics/runIII/RunIII_dev/2021_V3/PROTON 
