import os
import pickle
import numpy as np
import tfs

from omc3.tbt.handler import read_tbt
from omc3.tbt.handler import write_tbt
from omc3.hole_in_one import hole_in_one_entrypoint
from omc3.global_correction import global_correction_entrypoint

from global_coupling3 import _tfs_converter
from global_coupling3 import _remove_abs_outliers

PYTHON2="python2"
BETA_BEAT_DIR="/home/eirik/CERN/beta-Beat/"
Get_LLM=f"{BETA_BEAT_DIR}GetLLM/"
CORRECT_FILE = "changeparameters_iter_correct.madx"	

def get_multiple_coupling_from_sdds(working_dir,outputfile_dir,data_dir,model_dir,sdds_files,sing_val,nattunes,tunes,turns
	,beam,pickle_name,responsematrix,accel_settings,variable_categories,remove_outliers=True,remove_acd_noise=False,model_sdds=None):
	coupling_dict = {}
	for sdds_file_temp in sdds_files:
		#hack to deal with data stored in different ways
		if '/' in sdds_file_temp:
			sdds_file =  sdds_file_temp.split('/')[-1]
			data_dir_local = f"{data_dir}{sdds_file.split('.')[0]}/"
		else:
			sdds_file =  sdds_file_temp
			data_dir_local = data_dir
			
		get_couple_from_sdds(working_dir,outputfile_dir,data_dir_local,model_dir,sdds_file,sing_val,nattunes,tunes,turns,
				beam,remove_acd_noise=remove_acd_noise,model_sdds=model_sdds)		
				
		df_free = tfs.read(f"{outputfile_dir}getcouple_free.out",index="NAME")
		df_free2 = tfs.read(f"{outputfile_dir}getcouple_free2.out",index="NAME")
		
		knob_dict = get_knob_settings(working_dir,
		outputfile_dir,
		["getcouple_free.out","getcouple_free2.out"],
		accel_settings,
		responsematrix,
		remove_outliers=remove_outliers,
		variable_categories=variable_categories)
		
		df_free["knob_Re"] = knob_dict["getcouple_free.out"][0]
		df_free["knob_Im"] = knob_dict["getcouple_free.out"][1]
		df_free2["knob_Re"] = knob_dict["getcouple_free2.out"][0]
		df_free2["knob_Im"] = knob_dict["getcouple_free2.out"][1]
		
		measurement_dict = {}
		measurement_dict["analytic"] = df_free
		measurement_dict["scaled"] = df_free2
		
		coupling_dict[sdds_file] = measurement_dict
		
		
	with open(f"{outputfile_dir}/{pickle_name}","wb") as f:
                pickle.dump(coupling_dict,f)


def get_couple_from_sdds(working_dir,outputfile_dir,data_dir,model_dir,sdds_file,sing_val,nattunes,tunes,turns,beam,remove_acd_noise=False,model_sdds=None):
	#TODO delete output of hole_in_one at some point

	#measurement_sdds = read_tbt(f"{data_dir}{sdds_file}")
	
	
	print(f"********************************* {sdds_file} ****************")
	#BPMs = ['BPMYA.5L4.B1','BPMYB.6L4.B1','BPM.7L4.B1']
	if remove_acd_noise:
		assert False, "remove acd noise not implemented"
		#trackone_sdds_noise = read_tbt(f"{working_dir}{outputfile_dir}/{sdds_name}{noise}.sdds")
		#model_sdds = read_tbt(f"{data_dir}{model_sdds}")
		#for key in model_sdds.matrices[0]:
		#	for BPM in BPMs:
		#		measurement_sdds.matrices[0][key].loc[BPM,:] = model_sdds.matrices[0][key].loc[BPM,:]
		#write_tbt(f"{working_dir}{outputfile_dir}/{sdds_name}{noise}",trackone_sdds_noise)
		
	hole_in_one_entrypoint(
	clean=True,
	harpy=True, 
	to_write=['lin', 'spectra'],
	files=[f"{data_dir}{sdds_file}"],
	model=f"{model_dir}twiss.dat",
	outputdir=f"{working_dir}hole_in_one_dir",
	nattunes = nattunes,
	tunes = tunes,
	accel="lhc",
	beam=beam,
	year=2018,
	turns=turns,
	sing_val=sing_val,
	turn_bits=18,
	tolerance=0.005,
	unit = "mm"
	)
	
	#remove old coupling files
	os.system(f"rm {outputfile_dir}get*.out")
	run_GetLLM=f"{PYTHON2} {Get_LLM}GetLLM.py --accel=LHCB{beam} --model={model_dir}twiss.dat --files={working_dir}hole_in_one_dir/{sdds_file} --output={working_dir}{outputfile_dir} \
	--tbtana=SUSSIX --bpmu=mm --lhcphase=1 --errordefs={model_dir}error_deffs.txt --coupling=1"

	os.system(run_GetLLM)
	
def get_knob_settings(working_dir,
	outputfile_dir,
	coupling_files,
	accel_settings,
	responsematrix,
	remove_outliers=True,
	variable_categories=["squeeze_knobs"],
	optics_params=["F1001R","F1001I"],
	weights=[1.,1.]):
	
	knob_dict = {}
	for coupling_file in coupling_files:
		measurement_df = tfs.read(f"{outputfile_dir}{coupling_file}", index="NAME")
		if remove_outliers:
			measurement_df = _remove_abs_outliers(measurement_df,"F1001R","F1001I",0.05)
		_tfs_converter(outputfile_dir, measurement_df, remove_outliers = remove_outliers)
		
		
		global_correction_entrypoint(
		**accel_settings,
		meas_dir=outputfile_dir,
		variable_categories=variable_categories,
		fullresponse_path=responsematrix,
		optics_params=optics_params,
		output_dir=outputfile_dir,
		weights=weights,
		svd_cut=0.01,
		max_iter=0,
		)
		
		with open(f"{outputfile_dir}{CORRECT_FILE}","r") as f:
			correction = f.read()
		
		assert variable_categories[0] == "coupling_knobs" , "only works for couplig knobs"
		print(correction.split(';'))
		for i in range(2):
			if 're' in correction.split(';')[i].lower():
				knob_Re = float(correction.split(';')[i].split(' ')[3])
			elif 'im' in correction.split(';')[i].lower():		
				knob_Im = float(correction.split(';')[i].split(' ')[3])
		knob_dict[coupling_file] = [knob_Re,knob_Im]
	return knob_dict	
		


		
