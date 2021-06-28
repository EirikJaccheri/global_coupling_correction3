import sys
import copy
import numpy as np
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')



from global_coupling3 import get_corrections
from global_coupling3 import get_multiple_corrections
from global_coupling3 import get_multiple_twiss
from global_coupling3 import create_model_and_response
from global_coupling3 import _change_value


from plot_delQmin_est import plot_delQmin_est
from plot_delQmin_est import plot_sum_and_dif
from plot_delQmin_est import plot_tune_split
from plot_delQmin_est import plot_tune_split_test
from plot_delQmin_est import plot_multiple_coupling
from plot_delQmin_est import plot_f1001_f1010
from plot_delQmin_est import _get_lists

LHC_PATH = f"/home/eirik/CERN/lhc2018/2018/"
OUTPUTFILE_DIR = "outputfiles/"
BASE_SCRIPT_DIR = "/home/eirik/CERN/global_coupling_correction3/base_scripts/"
BASE_SCRIPT = f"{BASE_SCRIPT_DIR}single_correction_match_before.madx"
OPTICSFILE = "opticsfile.1"
QX = 0.29
QY = 0.31
QX_DRIVEN = 0.30
QY_DRIVEN = 0.332
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/delQmin_est/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}"
ACCEL_SETTINGS = dict(ats=True,beam=1, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=0.45)

#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN,variable_categories=["squeeze_knobs"])

CHANGE_DICT1 = {
	"%correct" : "0",
        "%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%knob_Re_value" :  "0.",
        "%knob_Im_value" :  "0.",
        "%error_component" :  "quadrupole",
        "%error_strength" :  "0.00001*gauss()",
        "%pattern_1" :  ".",
        "%pattern_2" :  ".",
        "%quad_component" :  "quadrupole",
        "%quad_pattern_1" :  "R5",
        "%quad_pattern_2" :  "R5",
        "%quad_strength" :  "0.",
        "%twiss_pattern" :  ".",
        "%colknob1" :  "0.",
        "%colknob5" :  "0.",
        "%percentage" :  "1",
        "%QX" :  str(62 + float(QX)),
        "%QY" :  str(60 + float(QY))
        }


CORRECTION_PICKLE1 = "delQmin_est_pickle"
#get_corrections(BASE_SCRIPT , CHANGE_DICT1, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, iterations=0,variable_categories=["squeeze_knobs"],pickle_name = CORRECTION_PICKLE1)
#plot_delQmin_est(OUTPUTFILE_DIR, CORRECTION_PICKLE1, "closed_bump.pdf",MODEL_DIR)


CHANGE_DICT2 = {
	"%correct" : "0",
        "%lhc_path" : LHC_PATH,
        "%opticsfile" :   OPTICSFILE,
        "%knob_Re_value" :  "0.",
        "%knob_Im_value" :  "0.",
        "%error_component" :  "quadrupole",
        "%error_strength" :  "0.00001*gauss()",
        "%pattern_1" :  ".",
        "%pattern_2" :  ".",
        "%quad_component" :  "quadrupole",
        "%quad_pattern_1" :  "R5",
        "%quad_pattern_2" :  "R5",
        "%quad_strength" :  "0.",
        "%twiss_pattern" :  ".",
        "%colknob1" :  "0.",
        "%colknob5" :  "0.",
        "%percentage" :  "1",
        "%QX" :  str(62 + float(QX)),
        "%QY" :  str(60 + float(QY))
        }
       
        
CHANGE_DICT4 = {"%correct" : "0",
	"%lhc_path" : LHC_PATH,
	"%opticsfile" :   OPTICSFILE,
	"%twiss_pattern" :  "BPM",
	"%QX" :  "62.31",
	"%QY" :  "60.32",
	"%DX" : "0.",
	"%DY" : "0.0004"}
        
CORRECTION_PICKLE2 = "sum_and_dif_pickle"
#get_corrections(BASE_SCRIPT , CHANGE_DICT2, RESPONSEMATRIX, OUTPUTFILE_DIR, ACCEL_SETTINGS, iterations=2,variable_categories=["squeeze_knobs"],pickle_name = CORRECTION_PICKLE2)
#plot_sum_and_dif(OUTPUTFILE_DIR, CORRECTION_PICKLE2, "closed_bump.pdf",MODEL_DIR)



#QY_list = np.concatenate((np.linspace(0.15,0.27,5),np.linspace(0.30,0.4,5)))
N = 30
QY_list = np.zeros(N)
QX_list = np.zeros(N)
delta_l = np.linspace(-0.1,0.1,N)
CHANGE_DICT_LIST = []
BASE_SCRIPT_LIST = []

CHANGE_DICT3 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT3,"%error_strength","0.00001*gauss()")
_change_value(CHANGE_DICT3,"%pattern_1","R5")
_change_value(CHANGE_DICT3,"%pattern_2","R7")
CHANGE_DICT_LIST2 = []


BASE_SCRIPT_LIST3 = []
CHANGE_DICT_LIST3 = []

BASE_SCRIPT_LIST4 = []
CHANGE_DICT_LIST4 = []


for i in range(len(delta_l)):
	QX_list[i] = 0.30 + delta_l[i] / 2
	QY_list[i] = 0.30 - delta_l[i]/ 2
	CHANGE_DICT_LOCAL = copy.deepcopy(CHANGE_DICT2)
	_change_value(CHANGE_DICT_LOCAL, "%QX",  str(62 + float(QX_list[i])))
	_change_value(CHANGE_DICT_LOCAL, "%QY",  str(60 + float(QY_list[i])))
	#CHANGE_DICT_LIST.append(CHANGE_DICT_LOCAL)
	#BASE_SCRIPT_LIST.append(BASE_SCRIPT)
	#
	
	#CHANGE_DICT_LOCAL2 = copy.deepcopy(CHANGE_DICT3)
	#_change_value(CHANGE_DICT_LOCAL2, "%QX",  str(62 + float(QX_list[i])))
	#_change_value(CHANGE_DICT_LOCAL2, "%QY",  str(60 + float(QY_list[i])))
	#CHANGE_DICT_LIST2.append(CHANGE_DICT_LOCAL2)
	
	CHANGE_DICT_LOCAL3 = copy.deepcopy(CHANGE_DICT4)
	#_change_value(CHANGE_DICT_LOCAL3, "%QX",  str(62 + float(QX_list[i])))
	#_change_value(CHANGE_DICT_LOCAL3, "%QY",  str(60 + float(QY_list[i])))
	#CHANGE_DICT_LIST3.append(CHANGE_DICT_LOCAL3)
	#BASE_SCRIPT_LIST3.append(f"{BASE_SCRIPT_DIR}ealign_mcs_match_before.madx")
	
	
	#CHANGE_DICT_LOCAL4 = copy.deepcopy(CHANGE_DICT2)
	#_change_value(CHANGE_DICT_LOCAL4,"%correct","1")
	#_change_value(CHANGE_DICT_LOCAL4,"%error_strength","0.0001*gauss()")
	#_change_value(CHANGE_DICT_LOCAL4, "%QX",  str(62 + float(QX_list[i])))
	#_change_value(CHANGE_DICT_LOCAL4, "%QY",  str(60 + float(QY_list[i])))
	###CHANGE_DICT_LIST4.append(CHANGE_DICT_LOCAL4)
	#BASE_SCRIPT_LIST4.append(f"{BASE_SCRIPT_DIR}single_correction_match_before_corrected.madx")
	
PICKLE_NAME = "twiss_pickle"

MODEL_CHANGES = {
 "%error_strength" :  "0.",
 "%twiss_pattern" :  ".",
}
CHANGE_DICT2_COL = copy.deepcopy(CHANGE_DICT2)
BASE_SCRIPT_LIST1 , CHANGE_DICT_LIST1 = _get_lists(BASE_SCRIPT,CHANGE_DICT2_COL,N)

#get_multiple_twiss(BASE_SCRIPT_LIST1, CHANGE_DICT_LIST1, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
plot_tune_split(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split2_coupledtunes.pdf", MODEL_DIR,QX_list, QY_list)
plot_tune_split_test(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split2_test.pdf", MODEL_DIR,QX_list, QY_list)

PICKLE_NAME = "twiss_pickle_tune_split2"

CHANGE_DICT3 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT3,"%error_strength","0.00001*gauss()")
_change_value(CHANGE_DICT3,"%pattern_1","R5")
_change_value(CHANGE_DICT3,"%pattern_2","R7")
BASE_SCRIPT_LIST2 , CHANGE_DICT_LIST2 = _get_lists(BASE_SCRIPT,CHANGE_DICT3,N)
#get_multiple_twiss(BASE_SCRIPT_LIST2, CHANGE_DICT_LIST2, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
plot_tune_split(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split_R5R7_coupled.pdf", MODEL_DIR,QX_list, QY_list)
plot_tune_split_test(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split3_R5R7_test.pdf", MODEL_DIR,QX_list, QY_list)

PICKLE_NAME = "twiss_pickle_tune_split3"

MODEL_CHANGES = {
 "%DY" : "0.",
 "%twiss_pattern" :  ".",
}

CHANGE_DICT_LOCAL3 = copy.deepcopy(CHANGE_DICT4)
BASE_SCRIPT_LIST3 , CHANGE_DICT_LIST3 = _get_lists(f"{BASE_SCRIPT_DIR}ealign_mcs_match_before.madx",CHANGE_DICT_LOCAL3,N)
#get_multiple_twiss(BASE_SCRIPT_LIST3, CHANGE_DICT_LIST3, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
plot_tune_split(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split_ealign_coupled.pdf", MODEL_DIR,QX_list, QY_list)
plot_tune_split_test(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split3_ealign_test.pdf", MODEL_DIR,QX_list, QY_list)

PICKLE_NAME = "twiss_pickle_tune_split4"


MODEL_CHANGES = {
 "%correct" : "0",
 "%error_strength" :  "0.",
 "%twiss_pattern" :  ".",
}

CHANGE_DICT_LOCAL4 = copy.deepcopy(CHANGE_DICT2)
_change_value(CHANGE_DICT_LOCAL4,"%correct","1")
_change_value(CHANGE_DICT_LOCAL4,"%error_strength","0.0001*gauss()")
_change_value(CHANGE_DICT_LOCAL4, "%QX",  str(62 + float(QX_list[i])))
_change_value(CHANGE_DICT_LOCAL4, "%QY",  str(60 + float(QY_list[i])))
BASE_SCRIPT_LIST4 , CHANGE_DICT_LIST4 = _get_lists(f"{BASE_SCRIPT_DIR}single_correction_match_before_corrected.madx",CHANGE_DICT_LOCAL4,N)
#get_multiple_twiss(BASE_SCRIPT_LIST4, CHANGE_DICT_LIST4, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
#plot_tune_split(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split4_SUM_coupled.pdf", MODEL_DIR,QX_list, QY_list)
#plot_tune_split_test(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split4_SUM_test.pdf", MODEL_DIR,QX_list, QY_list)


#at collision
PICKLE_NAME = "twiss_pickle_tune_split5"
MODEL_CHANGES = {
 "%error_strength" :  "0.",
 "%twiss_pattern" :  ".",
}

CHANGE_DICT2_COL = copy.deepcopy(CHANGE_DICT2)
_change_value( CHANGE_DICT2_COL, "%opticsfile", "opticsfile.19")
_change_value( CHANGE_DICT2_COL, "%error_strength", "0.000001*gauss()")
BASE_SCRIPT_LIST5 , CHANGE_DICT_LIST5 = _get_lists(BASE_SCRIPT,CHANGE_DICT2_COL,N)
#get_multiple_twiss(BASE_SCRIPT_LIST5, CHANGE_DICT_LIST5, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME, get_closest_tune= True)
plot_tune_split(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split5_coupled.pdf", MODEL_DIR,QX_list, QY_list)
plot_tune_split_test(OUTPUTFILE_DIR, PICKLE_NAME, "tune_split5_test.pdf", MODEL_DIR,QX_list, QY_list)

CHANGE_DICT11 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT11,"%error_strength","0.00003*gauss()")
_change_value(CHANGE_DICT11,"%pattern_1",".")
_change_value(CHANGE_DICT11,"%pattern_2",".")


CHANGE_DICT12 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT12,"%error_strength","0.00001*gauss()")
_change_value(CHANGE_DICT12,"%pattern_1","R5")
_change_value(CHANGE_DICT12,"%pattern_2","R7")

CHANGE_DICT13 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT13,"%error_strength","0.00001")
_change_value(CHANGE_DICT13,"%pattern_1","R5")
_change_value(CHANGE_DICT13,"%pattern_2","R5")

CHANGE_DICT14 = copy.deepcopy(CHANGE_DICT1)
_change_value(CHANGE_DICT14,"%error_strength","0.00001")
_change_value(CHANGE_DICT14,"%pattern_1","R4")
_change_value(CHANGE_DICT14,"%pattern_2","R8")


CHANGE_DICT_LIST2 = [CHANGE_DICT11, CHANGE_DICT12, CHANGE_DICT13, CHANGE_DICT14]
BASE_SCRIPT_LIST2 = [BASE_SCRIPT, BASE_SCRIPT, BASE_SCRIPT, BASE_SCRIPT]

PICKLE_NAME = "twiss_pickle2"
MODEL_CHANGES = {
 "%error_strength" :  "0.",
 "%twiss_pattern" :  ".",
}
#get_multiple_twiss(BASE_SCRIPT_LIST2, CHANGE_DICT_LIST2, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
#plot_multiple_coupling(OUTPUTFILE_DIR, PICKLE_NAME, "multiple_coupling.pdf", MODEL_DIR)

CHANGE_DICT_LIST2_collision = []
for change_dict in CHANGE_DICT_LIST2:
	change_dict_local = copy.deepcopy(change_dict)
	_change_value(change_dict_local,"%opticsfile","opticsfile.19")
	CHANGE_DICT_LIST2_collision.append(change_dict_local)

#get_multiple_twiss(BASE_SCRIPT_LIST2, CHANGE_DICT_LIST2_collision, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
#plot_multiple_coupling(OUTPUTFILE_DIR, PICKLE_NAME, "multiple_coupling_collision.pdf", MODEL_DIR)

#f1010 > f1001 cases
CHANGE_DICT21 = copy.deepcopy(CHANGE_DICT2)
_change_value(CHANGE_DICT21,"%error_strength","0")
_change_value(CHANGE_DICT21,"%colknob1","5")


CHANGE_DICT22 = copy.deepcopy(CHANGE_DICT2)
_change_value(CHANGE_DICT22,"%correct","1")
_change_value(CHANGE_DICT22,"%error_strength","0.0001*gauss()")

BASE_SCRIPT_CORRECTED = f"{BASE_SCRIPT_DIR}single_correction_match_before_corrected.madx"

CHANGE_DICT_LIST3 = [CHANGE_DICT22] #[CHANGE_DICT21,CHANGE_DICT22]
BASE_SCRIPT_LIST3 = [BASE_SCRIPT_CORRECTED] #[BASE_SCRIPT,BASE_SCRIPT_CORRECTED]

PICKLE_NAME = "twiss_pickle3"
MODEL_CHANGES = {
 "%error_strength" :  "0.",
 "%twiss_pattern" :  ".",
 "%colknob1" : "0.",
 "%correct" : "0."
}
#get_multiple_twiss(BASE_SCRIPT_LIST3, CHANGE_DICT_LIST3, MODEL_CHANGES, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
#plot_f1001_f1010(OUTPUTFILE_DIR, PICKLE_NAME, "abs_sum_resonance.pdf", MODEL_DIR)
#plot_multiple_coupling(OUTPUTFILE_DIR, PICKLE_NAME, "sum_resonance.pdf", MODEL_DIR)

PICKLE_NAME = "rog.pickle"
BASE_SCRIPT_ROG_l = [f"{BASE_SCRIPT_DIR}Rogelio_Lattice.madx"]
CHANGE_DICT_ROG_l = [{"%QX" : "2", "%QY" : "0"}]
MODEL_CHANGES_ROG = {}

#get_multiple_twiss(BASE_SCRIPT_ROG_l, CHANGE_DICT_ROG_l, MODEL_CHANGES_ROG, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
#plot_f1001_f1010(OUTPUTFILE_DIR, PICKLE_NAME, "abs_sum_resonance_rog.pdf", MODEL_DIR)
#plot_multiple_coupling(OUTPUTFILE_DIR, PICKLE_NAME, "sum_resonance_rog.pdf", MODEL_DIR)




PICKLE_NAME = "lhc_bump.pickle"
CHANGE_DICT_BUMP = copy.deepcopy(CHANGE_DICT2)
_change_value(CHANGE_DICT_BUMP, "%error_strength", "0.")
_change_value(CHANGE_DICT_BUMP, "%colknob5", "10")
_change_value(CHANGE_DICT_BUMP, "%percentage", "1")
_change_value(CHANGE_DICT_BUMP, "%opticsfile", "opticsfile.19")
BASE_SCRIPT_BUMP_l = [BASE_SCRIPT]
CHANGE_DICT_BUMP_l = [CHANGE_DICT_BUMP]
MODEL_CHANGES_BUMP = {"%colknob5" : "0"}
#get_multiple_twiss(BASE_SCRIPT_BUMP_l, CHANGE_DICT_BUMP_l, MODEL_CHANGES_BUMP, OUTPUTFILE_DIR, ACCEL_SETTINGS, PICKLE_NAME,get_closest_tune= True)
#plot_f1001_f1010(OUTPUTFILE_DIR, PICKLE_NAME, "abs_sum_resonance_bump.pdf", MODEL_DIR)
#plot_multiple_coupling(OUTPUTFILE_DIR, PICKLE_NAME, "sum_resonance_bump.pdf", MODEL_DIR)


