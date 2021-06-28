import sys
import copy
import os
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/data_analysis2"

from global_coupling3 import create_model_and_response

from coupling_from_sdds import get_couple_from_sdds
from coupling_from_sdds import get_multiple_coupling_from_sdds

from plot_data_analysis2 import plot_tbt_data
from plot_data_analysis2 import plot_f1001_comparison
from plot_data_analysis2 import plot_knob
from plot_data_analysis2 import plot_abs_f1001_difference
from plot_data_analysis2 import plot_abs_f1001




#BEAM 2
DATA_DIR = "/home/eirik/cernbox/old_fills/3607/BPM/"

B2_Kicks = [f"Beam2@Turn@2015_04_09@02_13_09_115.sdds",f"Beam2@Turn@2015_04_09@01_58_48_846.sdds"]

B2_Tune_Kicks = [f"Beam2@Turn@2015_04_09@01_25_36_552.sdds",f"Beam2@Turn@2015_04_09@01_28_10_125.sdds"]

#first one has weird spike
#LHCB2 kicks
#Qx=0.28
#Qy=0.31
#ACQx=0.27
#ACQy=0.32
#|c-|=0.005

#bad measurements..
B2_AC_5GeV = [f"Beam2@Turn@2015_04_08@23_50_39_632.sdds",f"Beam2@Turn@2015_04_08@23_53_43_729.sdds",f"Beam2@Turn@2015_04_08@23_57_10_579.sdds",f"Beam2@Turn@2015_04_09@00_00_25_664.sdds",f"Beam2@Turn@2015_04_09@00_09_46_247.sdds",f"Beam2@Turn@2015_04_09@00_12_17_214.sdds"]

B2_AC_8GeV = [f"Beam2@Turn@2015_04_09@00_32_13_138.sdds",f"Beam2@Turn@2015_04_09@00_34_23_143.sdds",f"Beam2@Turn@2015_04_09@00_36_10_402.sdds",f"Beam2@Turn@2015_04_09@00_37_29_062.sdds",f"Beam2@Turn@2015_04_09@00_39_25_311.sdds"]

#LHCB2 kicks
#Qx=0.278
#Qy=0.308
#ACQx=0.268
#ACQy=0.318

B2_AC_1 = ["Beam2@Turn@2015_04_09@02_44_28_851.sdds",
"Beam2@Turn@2015_04_09@02_46_58_027.sdds",
"Beam2@Turn@2015_04_09@02_49_20_875.sdds",
"Beam2@Turn@2015_04_09@02_59_21_462.sdds",
"Beam2@Turn@2015_04_09@03_00_37_208.sdds",
"Beam2@Turn@2015_04_09@03_02_15_581.sdds",
"Beam2@Turn@2015_04_09@03_03_24_717.sdds",
"Beam2@Turn@2015_04_09@03_05_08_143.sdds"]# "Beam2@Turn@2015_04_09@02_51_05_160.sdds"

#LHCB2 kicks
#Qx=0.2806
#Qy=0.3106
#ACQx=0.2706
#ACQy=0.3206


B2_AC_2 = [
"Beam2@Turn@2015_04_09@03_15_47_209.sdds",
"Beam2@Turn@2015_04_09@03_17_11_804.sdds",
"Beam2@Turn@2015_04_09@03_18_38_849.sdds",
"Beam2@Turn@2015_04_09@03_19_55_979.sdds",
"Beam2@Turn@2015_04_09@03_21_32_174.sdds",
"Beam2@Turn@2015_04_09@03_23_29_898.sdds"]


#fresh beam_
#LHCB2 kicks
#Qx=0.278
#Qy=0.310
#ACQx=0.268
#ACQy=0.320

B2_AC_3 = ["Beam2@Turn@2015_04_09@04_18_33_348.sdds",
"Beam2@Turn@2015_04_09@04_19_48_301.sdds",
"Beam2@Turn@2015_04_09@04_21_29_517.sdds",
"Beam2@Turn@2015_04_09@04_22_41_225.sdds",
"Beam2@Turn@2015_04_09@04_24_02_360.sdds",
"Beam2@Turn@2015_04_09@04_25_45_212.sdds"]

	
LHC_PATH = f"/home/eirik/CERN/lhc2018/2018/"
OUTPUTFILE_DIR = "outputfiles/"
OPTICSFILE = "opticsfile.1"
QX = 0.278
QY = 0.31
QX_DRIVEN = 0.268
QY_DRIVEN = 0.32
BEAM = 2
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/data_analysis2/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}"
ACCEL_SETTINGS = dict(ats=True,beam=BEAM, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=6.5)

SING_VAL = 16
NATTUNES = [QX,QY,0.]
TUNES = [QX_DRIVEN,QY_DRIVEN,0.]
TURNS = [0,6600]
VARIABLE_CATEGORIES = ["coupling_knobs"]


#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN,variable_categories = VARIABLE_CATEGORIES)

#turn by turn data
#plot_tbt_data(WORKING_DIR,B2_AC_8GeV[0],"BPM.28R5.B2")

#kick
SDDS_FILE = B2_Kicks[0]
COUPLING_FILES = ["getcouple.out"] #
get_couple_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,SDDS_FILE,SING_VAL,NATTUNES,TUNES,TURNS,BEAM)
plot_f1001_comparison(OUTPUTFILE_DIR,COUPLING_FILES,SDDS_FILE,QX,QY,plot_abs=False)

#f1001 comparison
SDDS_FILE = B2_AC_1[3]
COUPLING_FILES = ["getcouple_free.out","getcouple_free2.out"] #["getcouple.out"] #
#get_couple_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,SDDS_FILE,SING_VAL,NATTUNES,TUNES,TURNS,BEAM)
#plot_f1001_comparison(OUTPUTFILE_DIR,COUPLING_FILES,SDDS_FILE,QX,QY,plot_abs=False)
	
PICKLE_NAME = "ac_b2_8GeV.pickle"
#get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,B2_AC_8GeV,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES)
#plot_knob(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,BEAM,plot_abs=False)
#plot_abs_f1001_difference(OUTPUTFILE_DIR,PICKLE_NAME)
#plot_abs_f1001(OUTPUTFILE_DIR,PICKLE_NAME)

B2_AC_ALL = B2_AC_3
PICKLE_NAME = "ac_b2_all"
get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,B2_AC_ALL,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES)
#plot_knob(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,BEAM,plot_abs=False)
#plot_abs_f1001_difference(OUTPUTFILE_DIR,PICKLE_NAME)
#plot_abs_f1001(OUTPUTFILE_DIR,PICKLE_NAME)
	



#BEAM 1

DATA_DIR = "/home/eirik/cernbox/old_fills/3607/BPM/"

#LHCB1 kicks
#Qx=0.2798
#Qy=0.3101
#ACQx=0.27
#ACQy=0.32
#|c-|=0.004
#dp/p=

B1_AC  = ["Beam1@Turn@2015_04_09@00_33_57_607.sdds",f"Beam1@Turn@2015_04_09@00_36_24_743.sdds",f"Beam1@Turn@2015_04_09@00_37_46_837.sdds",f"Beam1@Turn@2015_04_09@00_39_03_894.sdds",f"Beam1@Turn@2015_04_09@00_40_19_519.sdds",f"Beam1@Turn@2015_04_09@01_08_05_535.sdds"]	

#Qx=0.278
#Qy=0.308
#ACQx=0.268
#ACQy=0.318
#|c-|=0.004

#52 is somehow bad 04_52_29
B1_AC_2 = ["Beam1@Turn@2015_04_09@02_44_52_772.sdds",
"Beam1@Turn@2015_04_09@02_48_34_046.sdds",
"Beam1@Turn@2015_04_09@02_57_27_156.sdds",
"Beam1@Turn@2015_04_09@02_58_49_356.sdds",
"Beam1@Turn@2015_04_09@03_00_00_563.sdds",
"Beam1@Turn@2015_04_09@03_01_38_809.sdds",
"Beam1@Turn@2015_04_09@03_02_55_488.sdds",
"Beam1@Turn@2015_04_09@03_05_48_346.sdds",
"Beam1@Turn@2015_04_09@03_06_54_742.sdds"]


#Qx=0.281
#Qy=0.311
#ACQx=0.271
#ACQy=0.321
#|c-|=0.004
#dp/p= -50Hz, +0.4(YASP)

#05:15:00 - 3% 3% -> only 2000 turns
B1_AC_3 = ["Beam1@Turn@2015_04_09@03_16_35_730.sdds",
"Beam1@Turn@2015_04_09@03_18_10_729.sdds",
"Beam1@Turn@2015_04_09@03_19_27_774.sdds",
"Beam1@Turn@2015_04_09@03_20_35_270.sdds",
"Beam1@Turn@2015_04_09@03_21_44_370.sdds",
"Beam1@Turn@2015_04_09@03_23_02_028.sdds"]

#tunes are to different
#Qx= 0.31
#Qy= 0.32
#ACQx= 0.30
#ACQy= 0.33
#|c-|=
#dp/p=

B1_AC_4 = ["Beam1@Turn@2015_04_09@06_00_50_059.sdds",
"Beam1@Turn@2015_04_09@06_01_35_660.sdds",
"Beam1@Turn@2015_04_09@06_04_25_394.sdds",
"Beam1@Turn@2015_04_09@06_05_46_335.sdds"]



LHC_PATH = f"/home/eirik/CERN/lhc2018/2018/"
OUTPUTFILE_DIR = "outputfiles/"
OPTICSFILE = "opticsfile.1"
QX = 0.2798
QY = 0.3101
QX_DRIVEN = 0.27
QY_DRIVEN = 0.32
BEAM = 1
WORKING_DIR = "/home/eirik/CERN/global_coupling_correction3/data_analysis2/"
MODEL_DIR = f"model_{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}/"
RESPONSEMATRIX = f"{OUTPUTFILE_DIR}fullresponse{OPTICSFILE}_Qx{QX}_Qy{QY}_beam{BEAM}"
ACCEL_SETTINGS = dict(ats=True,beam=BEAM, model_dir=MODEL_DIR,
                      year="2018", accel="lhc", energy=6.5)

SING_VAL = 16
NATTUNES = [QX,QY,0.]
TUNES = [QX_DRIVEN,QY_DRIVEN,0.]
TURNS = [0,6600]
VARIABLE_CATEGORIES = ["coupling_knobs"]

#create_model_and_response(WORKING_DIR, MODEL_DIR, RESPONSEMATRIX, OPTICSFILE, ACCEL_SETTINGS, QX, QY, QX_DRIVEN, QY_DRIVEN,variable_categories = VARIABLE_CATEGORIES)


SDDS_FILE = B1_AC_2[6]
COUPLING_FILES = ["getcouple_free.out","getcouple_free2.out"]#["getcouple.out"]
#get_couple_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,SDDS_FILE,SING_VAL,NATTUNES,TUNES,TURNS,BEAM)
#plot_f1001_comparison(OUTPUTFILE_DIR,COUPLING_FILES,SDDS_FILE,QX,QY,plot_abs=False)
	

PICKLE_NAME = "ac_b1.pickle"
#get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,B1_AC,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES)
#plot_knob(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,BEAM,plot_abs=False)
#plot_abs_f1001_difference(OUTPUTFILE_DIR,PICKLE_NAME)
#plot_abs_f1001(OUTPUTFILE_DIR,PICKLE_NAME)


PICKLE_NAME = "ac_b1_2.pickle"
#get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,B1_AC_2,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES)
#plot_knob(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,BEAM,plot_abs=False)
#plot_abs_f1001_difference(OUTPUTFILE_DIR,PICKLE_NAME)
#plot_abs_f1001(OUTPUTFILE_DIR,PICKLE_NAME)


PICKLE_NAME = "ac_b1_3.pickle"
#get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,B1_AC_3,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES)
#plot_knob(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,BEAM,plot_abs=False)
#plot_abs_f1001_difference(OUTPUTFILE_DIR,PICKLE_NAME)
#plot_abs_f1001(OUTPUTFILE_DIR,PICKLE_NAME)

B1_AC_ALL = B1_AC+B1_AC_2+B1_AC_2+B1_AC_3
print(B1_AC_ALL)
PICKLE_NAME = "ac_b1_all"
#get_multiple_coupling_from_sdds(WORKING_DIR,OUTPUTFILE_DIR,DATA_DIR,MODEL_DIR,B1_AC_ALL,SING_VAL,NATTUNES,TUNES,TURNS,BEAM,PICKLE_NAME,RESPONSEMATRIX,ACCEL_SETTINGS,VARIABLE_CATEGORIES)
plot_knob(OUTPUTFILE_DIR,PICKLE_NAME,QX,QY,BEAM,plot_abs=True)
plot_abs_f1001_difference(OUTPUTFILE_DIR,PICKLE_NAME)
plot_abs_f1001(OUTPUTFILE_DIR,PICKLE_NAME)

