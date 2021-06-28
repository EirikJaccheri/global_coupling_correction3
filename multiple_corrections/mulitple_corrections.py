import sys
import copy
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

from global_coupling3 import get_multiple_corrections
from global_coupling3 import create_model_and_response
from global_coupling3 import _change_value

from plot_mulitple_corrections import plot_multiple_corrections_bar_diagram
from plot_mulitple_corrections import plot_betabeating

LHC_PATH = f"/home/eirik/CERN/lhc/"
OUTPUTFILE_DIR = "outputfiles/"
BASE_SCRIPT_DIR = "/home/eirik/CERN/global_coupling_correction3/base_scripts/"
OPTICSFILE = "opticsfile.22"
QX = 0.31
QY = 0.32
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/multiple_corrections/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}"
ACCEL_SETTINGS = dict(ats=True,beam=1, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=0.45)

#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY)


CHANGE_DICT_EALIGN = {"%correct" : "0",
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

CHANGE_DICT_EALIGN_TILT = {"%correct" : "0",
        "%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%twiss_pattern" :  "BPM",
        "%QX" :  "62.31",
        "%QY" :  "60.32",
        "%DX" : "0.",
        "%DY" : "0.0004",
        "%PATTERN_TRIPLET" : "MQX.*R1",
        "%DPSI" : "0.0005",
        "%quad_component" :  "quadrupole",
        "%quad_pattern_1" :  "R5",
        "%quad_pattern_2" :  "R5",
        "%quad_strength" :  "0.",
        "%twiss_pattern" :  "BPM"}




#one source
BASE_SCRIPT1 = f"{BASE_SCRIPT_DIR}ealign_mcs_corrected_EFFCOMP.madx"
CHANGE_DICT1 = copy.deepcopy(CHANGE_DICT_EALIGN)
_change_value(CHANGE_DICT1,"%pattern_1","MQ.18R2.B1")
_change_value(CHANGE_DICT1,"%pattern_2","MQ.18R2.B1")
_change_value(CHANGE_DICT1,"%error_strength","0.0004")

#two sources
BASE_SCRIPT2 = f"{BASE_SCRIPT_DIR}ealign_mcs_corrected_EFFCOMP.madx"
CHANGE_DICT2 = copy.deepcopy(CHANGE_DICT_EALIGN)
_change_value(CHANGE_DICT2,"%pattern_1","MQ.18R2.B1")
_change_value(CHANGE_DICT2,"%pattern_2","MQ.32R1.B1")
_change_value(CHANGE_DICT2,"%error_strength","0.0003")


#random quadrupole
BASE_SCRIPT3 = f"{BASE_SCRIPT_DIR}ealign_mcs_corrected_EFFCOMP.madx"
CHANGE_DICT3 = copy.deepcopy(CHANGE_DICT_EALIGN)
_change_value(CHANGE_DICT3,"%pattern_1",".")
_change_value(CHANGE_DICT3,"%pattern_2",".")
_change_value(CHANGE_DICT3,"%error_strength","0.000001*gauss()")

#tilt in triplet
BASE_SCRIPT4 = f"{BASE_SCRIPT_DIR}ealign_mcs_corrected_TripletTilt.madx"
CHANGE_DICT4 = copy.deepcopy(CHANGE_DICT_EALIGN_TILT)
_change_value(CHANGE_DICT4,"%PATTERN_TRIPLET","MQX.*R1")
_change_value(CHANGE_DICT4,"%DPSI","0.0007") # tilt induces betabeating

#closed bump
BASE_SCRIPT5 = f"{BASE_SCRIPT_DIR}single_correction.madx"
CHANGE_DICT5 = {"%correct" : "0",
        "%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%knob_Re_value" :  "0.",
        "%knob_Im_value" :  "0.",
        "%error_component" :  "quadrupole",
        "%error_strength" :  "0.0",
        "%pattern_1" :  ".",
        "%pattern_2" :  ".",
        "%quad_component" :  "quadrupole",
        "%quad_pattern_1" :  "R5",
        "%quad_pattern_2" :  "R5",
        "%quad_strength" : "0.",
        "%twiss_pattern" :  "BPM",
        "%colknob1" :  "5.",
        "%colknob5" :  "0.",
        "%percentage" :  "1.",
        "%QX" :  "62.31",
        "%QY" :  "60.32"}

#bar diagram zero betabeating
BASE_SCRIPTS = [BASE_SCRIPT1,BASE_SCRIPT2,BASE_SCRIPT3,BASE_SCRIPT4,BASE_SCRIPT5]
CHANGE_DICTS = [CHANGE_DICT1,CHANGE_DICT2,CHANGE_DICT3,CHANGE_DICT4,CHANGE_DICT5]

PICKLE_NAME = "multiple_correction_pickle"

#get_multiple_corrections(BASE_SCRIPTS, CHANGE_DICTS, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = PICKLE_NAME, iterations=2)

plot_multiple_corrections_bar_diagram(OUTPUTFILE_DIR,PICKLE_NAME,"bar_diagram.pdf",MODEL_DIR, width = 0.3)

#betabeating bar-diagram 4.3% rms betabeat
CHANGE_DICTS_BETABEATING1 = copy.deepcopy(CHANGE_DICTS)
for change_dict in CHANGE_DICTS_BETABEATING1:
	_change_value(change_dict, "%quad_strength",  "0.000006")

PICKLE_NAME = "betabeat_bar_pickle"

#get_multiple_corrections(BASE_SCRIPTS, CHANGE_DICTS_BETABEATING1, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = PICKLE_NAME, iterations=2)

plot_multiple_corrections_bar_diagram(OUTPUTFILE_DIR,PICKLE_NAME,"bar_diagram_betabeating1.pdf",MODEL_DIR,width=0.3)

#high betabeating  8.7% beta-beating
PICKLE_NAME = "betabeat2_bar_pickle"
CHANGE_DICTS_BETABEATING2 = copy.deepcopy(CHANGE_DICTS)
for change_dict in CHANGE_DICTS_BETABEATING2:
	_change_value(change_dict, "%quad_strength",  "0.000012")


#get_multiple_corrections(BASE_SCRIPTS, CHANGE_DICTS_BETABEATING2, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = PICKLE_NAME, iterations=2)

#plot_multiple_corrections_bar_diagram(OUTPUTFILE_DIR,PICKLE_NAME,"bar_diagram_betabeating2.pdf",MODEL_DIR,width=0.3)


"""
#Betabeating_calculation
CHANGE_DICT1_BETABEAT1 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT1_BETABEAT1, "%quad_strength",  "0.000001")
PICKLE_NAME = "beta_beat_pickle"


CHANGE_DICT1_BETABEAT2 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT1_BETABEAT2, "%quad_strength",  "0.000005")
PICKLE_NAME = "beta_beat_pickle"


CHANGE_DICT1_BETABEAT3 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT1_BETABEAT3, "%quad_strength",  "0.00001")
PICKLE_NAME = "beta_beat_pickle"


CHANGE_DICT1_BETABEAT4 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT1_BETABEAT4, "%quad_strength",  "0.000015")
PICKLE_NAME = "beta_beat_pickle"
#get_multiple_corrections([BASE_SCRIPT1,BASE_SCRIPT1,BASE_SCRIPT1,BASE_SCRIPT1], [CHANGE_DICT1_BETABEAT1,CHANGE_DICT1_BETABEAT2,CHANGE_DICT1_BETABEAT3,CHANGE_DICT1_BETABEAT4], RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, pickle_name = PICKLE_NAME, iterations=2)

#plot_betabeating(OUTPUTFILE_DIR, PICKLE_NAME, MODEL_DIR, "beta_beat.pdf")

"""

