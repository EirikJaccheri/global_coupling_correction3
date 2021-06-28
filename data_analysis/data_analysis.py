import sys
import copy
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/data_analysis"

from coupling_from_sdds import get_couple_from_sdds
from coupling_from_sdds import get_knob_settings
from coupling_from_sdds import get_multiple_coupling_from_sdds
from global_coupling3 import create_model_and_response

from omc3.plotting import plot_spectrum
from plot_data_analysis import plot_tbt_data
from plot_data_analysis import plot_f1001_comparison
from plot_data_analysis import plot_Cmin
from plot_data_analysis import plot_knobs
#1.make a model. How do i know the model?


LHC_PATH = f"/home/eirik/CERN/lhc2018/2018/"
OUTPUTFILE_DIR = "outputfiles/"
OPTICSFILE = "opticsfile.19"
QX = 0.313
QY = 0.317
BEAM = 1
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/data_analysis/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}"
ACCEL_SETTINGS = dict(ats=True,beam=BEAM, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=6.5)




DATA_DIR = "/home/eirik/cernbox/data07_08_18/BPM/"

#beam 1 
#SDDS_FILE = "Beam1@Turn@2018_08_06@23_04_17_790.sdds"
#SDDS_FILE = "Beam1@Turn@2018_08_06@23_03_32_240.sdds"

#beam 2
#SDDS_FILE = "Beam2@Turn@2018_08_06@23_04_16_658.sdds"
SDDS_FILE = "Beam2@Turn@2018_08_06@23_03_33_371.sdds"
#SDDS_FILE = "Beam2@Turn@2018_08_06@23_02_47_627.sdds"
#SDDS_FILE  = "Beam2@Turn@2018_08_06@23_02_01_578.sdds"

SDDS_FILES_BEAM1= [
"Beam1@Turn@2018_08_06@22_58_41_834.sdds",
"Beam1@Turn@2018_08_06@22_59_31_469.sdds",
"Beam1@Turn@2018_08_06@23_00_21_705.sdds",
"Beam1@Turn@2018_08_06@23_01_06_879.sdds",
"Beam1@Turn@2018_08_06@23_02_02_711.sdds",
"Beam1@Turn@2018_08_06@23_02_48_762.sdds",
"Beam1@Turn@2018_08_06@23_03_32_240.sdds",
"Beam1@Turn@2018_08_06@23_04_17_790.sdds"
]



SDDS_FILES_BEAM2= [
"Beam2@Turn@2018_08_06@22_57_56_956.sdds",
"Beam2@Turn@2018_08_06@22_58_40_701.sdds",
"Beam2@Turn@2018_08_06@22_59_32_600.sdds",
"Beam2@Turn@2018_08_06@23_00_20_574.sdds",
"Beam2@Turn@2018_08_06@23_01_08_022.sdds",
"Beam2@Turn@2018_08_06@23_02_01_578.sdds",
"Beam2@Turn@2018_08_06@23_02_47_627.sdds",
"Beam2@Turn@2018_08_06@23_03_33_371.sdds",
"Beam2@Turn@2018_08_06@23_04_16_658.sdds"]


SING_VAL = 12
NATTUNES = [QX,QY,0.]
QX_DRIVEN = QX - 0.012
QY_DRIVEN = QY + 0.012
TUNES = [QX_DRIVEN,QY_DRIVEN,0.]
TURNS = [0,6600]
VARIABLE_CATEGORIES = ["coupling_knobs"]
#creating model
#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN,variable_categories = VARIABLE_CATEGORIES)




#get_couple_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,SDDS_FILE,SING_VAL,NATTUNES,TUNES,TURNS,BEAM)
#plot_f1001_comparison(OUTPUTFILE_DIR,["getcouple.out","getcouple_free.out","getcouple_free2.out"],SDDS_FILE,QX,QY)

#knob_dict = get_knob_settings(WORKING_DIR,OUTPUTFILE_DIR,["getcouple_free.out","getcouple_free2.out"],ACCEL_SETTINGS,RESPONSEMATRIX,variable_categories = ["coupling_knobs"])
#print(knob_dict)
#plot_tbt_data(DATA_DIR,SDDS_FILE,"BPM.24R2.B1")


#plot_spectrum.main(files=[f"hole_in_one_dir/{SDDS_FILE}"],bpms=['BPM.24R2.B1'],combine_by=["files"],show_plots=True,output_dir="plots/spectrum")

#BEAM2
PICKLE_NAME = "multiple_coupling_pickle_beam2"
#get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,SDDS_FILES_BEAM2,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES,remove_acd_noise=False,model_sdds=None)

#plot_Cmin(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,2)
#plot_knobs(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,2,plot_abs=True)

#BEAM1
PICKLE_NAME = "multiple_coupling_pickle_beam1"
#get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,SDDS_FILES_BEAM1,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES,remove_acd_noise=False,model_sdds=None)

#plot_Cmin(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,1)
#plot_knobs(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,1,plot_abs=False)

#TEST
PICKLE_NAME = "multiple_coupling_pickle_TEST"
get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,["Beam1@Turn@2018_08_06@22_58_41_834.sdds"],SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES,remove_acd_noise=False,model_sdds=None)

plot_Cmin(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,1)
plot_knobs(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,1)


"""
DATA_DIR = "/home/eirik/CERN/tracking/tracking_files/EFFCOMP/"
SDDS_FILE = "trackone_n0.00132.sdds"
SING_VAL = 8
NATTUNES = [QX,QY,0.]
QX_DRIVEN = 0.30
QY_DRIVEN = 0.332
TUNES = [0.30,0.332,0.]
TURNS = [2000,8600]
create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN)

from omc3.tbt.handler import read_tbt
measurement_sdds = read_tbt(f"{DATA_DIR}{SDDS_FILE}")
print(measurement_sdds.matrices)
#/strength/ats/low-beta/ats_30cm_ctpps2.madx 
"""
