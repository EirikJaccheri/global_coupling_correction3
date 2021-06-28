import sys
import copy
import os
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/data_analysis2"

from global_coupling3 import create_model_and_response

from coupling_from_sdds import get_couple_from_sdds
from coupling_from_sdds import get_multiple_coupling_from_sdds

from plot_tracking import plot_f1001
from plot_tracking import plot_f1001_comparison

LHC_PATH = f"/home/eirik/CERN/lhc2018/2018/"
OUTPUTFILE_DIR = "outputfiles/"
OPTICSFILE = "opticsfile.1"
QX = 0.31
QY = 0.32
QX_DRIVEN = 0.30
QY_DRIVEN = 0.332
BEAM = 1
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/tracking/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}"
ACCEL_SETTINGS = dict(ats=True,beam=BEAM, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=6.5)

SING_VAL = 16
NATTUNES = [QX,QY,0.]
TUNES = [QX_DRIVEN,QY_DRIVEN,0.]
TURNS =[0,6600]
VARIABLE_CATEGORIES = ["coupling_knobs"]


#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN,variable_categories = VARIABLE_CATEGORIES)

TRACKONE_DIR = "UNCORRECTED_LOCAL_INJECTION"
#TRACKONE_DIR = "UNCORRECTED_LOCAL"
#TRACKONE_DIR = "EALIGN_MCS"
AC_DIPOLE_DIR="/home/eirik/cernbox/MESS/LHC/AC_Dipole_Tracking/"


copy_tracking_dir=f"cp -r {AC_DIPOLE_DIR}Outputdata {WORKING_DIR}{TRACKONE_DIR}"


#os.system(copy_tracking_dir)

PYTHON3 = "python3"
OMC3_DIR="/home/eirik/CERN/omc3/omc3/"
run_sdds_converter=f"{PYTHON3} {OMC3_DIR}tbt_converter.py --files={TRACKONE_DIR}/trackone --outputdir={WORKING_DIR}{OUTPUTFILE_DIR} \
--tbt_datatype=trackone"

#os.system(run_sdds_converter)

SDDS_FILE = "trackone.sdds"

DATA_DIR = OUTPUTFILE_DIR
COUPLING_FILES = [f"{TRACKONE_DIR}/Eirik_twiss_BPM.tfs",f"{OUTPUTFILE_DIR}/getcouple_free2.out"] #[f"{TRACKONE_DIR}/Eirik_twiss_BPM.tfs"]#
#get_couple_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,SDDS_FILE,SING_VAL,NATTUNES,TUNES,TURNS,BEAM)
plot_f1001_comparison(OUTPUTFILE_DIR,TRACKONE_DIR,TRACKONE_DIR,False,RDT= "F1010",plot_abs=True)
