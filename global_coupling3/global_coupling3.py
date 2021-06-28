import numpy as np
import tfs
import copy
import pickle
import os
import path

import omc3.madx_wrapper as madx_wrapper
from omc3.global_correction import global_correction_entrypoint
from omc3.correction.constants import ERR, DELTA
from omc3.response_creator import create_response_entrypoint
from omc3.model_creator import create_instance_and_model

from optics_functions.coupling import coupling_via_cmatrix
from optics_functions.utils import prepare_twiss_dataframe

#constants
MADX_PATH = "/home/eirik/CERN/global_coupling_correction3/global_coupling3/madxCouplingEst"
CORRECT_FILE = "changeparameters_iter_correct.madx"	
DELTA_Q_MIN = "deltaQmin"

OMC3_DIR = "/home/eirik/CERN/omc3/omc3/"
LHC_PATH = f"/home/eirik/CERN/lhc2018/2018/"
VARIABLE_CATEGORIES = ["squeeze_knobs"]
PYTHON3 = "python3"


#scripts
def create_model_and_response(working_dir, model_dir, responsematrix, opticsfile, accel_settings, qx, qy, qx_driven, qy_driven, variable_categories = VARIABLE_CATEGORIES,PROTON="PROTON"):
	"""
	create_model=f"{PYTHON3} {OMC3_DIR}model_creator.py \
	--type=nominal --accel=lhc --year=2018 --beam=1 --nat_tunes {qx} {qy} \
	--drv_tunes 0.30 0.332 --driven_excitation acd --dpp=0.0 --energy=6.5 \
	--modifiers={LHC_PATH}{PROTON}/{opticsfile} \
	--fullresponse --output={working_dir}{model_dir} \
	--writeto={working_dir}{model_dir}job.twiss.madx \
	--logfile={working_dir}{model_dir}madx_log.txt"
	"""
	#dict(ats=True,beam=1, model_dir=MODEL_DIR,
        #             year="2018", accel="lhc", energy=0.45)
	
	#accel settings is bad code..
	
	create_instance_and_model(
	accel = accel_settings["accel"],
	year = accel_settings["year"],
	energy = accel_settings["energy"],
	beam = accel_settings["beam"],
	type="nominal",
	ats = True,
	nat_tunes = [qx, qy],
	drv_tunes = [qx_driven, qy_driven],
	driven_excitation ="acd",
	dpp = 0.,
	modifiers = f"{LHC_PATH}{PROTON}/{opticsfile}",
	outputdir = f"{working_dir}{model_dir}",
	writeto= f"{working_dir}{model_dir}job.twiss.madx",
	logfile= f"{working_dir}{model_dir}madx_log.txt"
	)
	
	copy_opticsfile=f"cp {LHC_PATH}{PROTON}/{opticsfile} {working_dir}{model_dir}modifiers.madx"
	os.system(copy_opticsfile)

	create_response_entrypoint(
		**accel_settings,
		delta_k = 0.00002,
		variable_categories = variable_categories,\
		outfile_path = f"{working_dir}{responsematrix}",
		)

def get_corrections(base_script, change_dict, responsematrix, outputfile_dir, accel_settings,pickle_name="correction_pickle", get_closest_tune = True, iterations=1, 
	variable_categories=VARIABLE_CATEGORIES, optics_params=["F1001R","F1001I"],weights=[1.,1.],add_errors_to_df = False):
	
	correction_dict = _get_correction_dict(base_script, change_dict, responsematrix, outputfile_dir, accel_settings,get_closest_tune, iterations, 
	variable_categories, optics_params, weights, add_errors_to_df)
	
	with open(f"{outputfile_dir}/{pickle_name}","wb") as f:
		pickle.dump(correction_dict,f)
		
def get_multiple_corrections(base_script_l, change_dict_l, responsematrix, outputfile_dir, accel_settings, pickle_name="multiple_correction_pickle", get_closest_tune = True, iterations=1, variable_categories=["squeeze_knobs"], optics_params=["F1001R","F1001I"],weights=[1.,1.],add_errors_to_df=False):
	
	multiple_correction_dict = {}
	for i in range(len(base_script_l)):
		base_script = base_script_l[i]
		change_dict_local = change_dict_l[i]
		multiple_correction_dict[str(i)] = _get_correction_dict(base_script, change_dict_local, responsematrix, outputfile_dir, accel_settings,get_closest_tune, iterations, 
	variable_categories, optics_params, weights, add_errors_to_df)
		
	
	with open(f"{outputfile_dir}/{pickle_name}","wb") as f:
		pickle.dump(multiple_correction_dict,f)
	

def get_multiple_twiss(base_script_l, change_dict_l, model_changes, outputfile_dir, accel_settings, pickle_name,get_closest_tune= True):
	multiple_twiss_dict = {}
	for i in range(len(base_script_l)):
		base_script = base_script_l[i]
		change_dict = change_dict_l[i]
		multiple_twiss_dict[str(i)] = _get_twiss_dict(base_script, change_dict, model_changes, outputfile_dir, accel_settings,get_closest_tune)
		
	
	with open(f"{outputfile_dir}/{pickle_name}","wb") as f:
		pickle.dump(multiple_twiss_dict,f)
		
#utilites
def _get_twiss_dict(base_script, change_dict, model_changes, outputfile_dir, accel_settings,get_closest_tune):
	twiss_dict = {}
	
	#model
	change_dict_model = copy.deepcopy(change_dict)
	for key in model_changes:
		_change_value(change_dict_model, key, model_changes[key])
	model_twiss_df = _get_twiss_df(base_script, change_dict_model, outputfile_dir)
	twiss_dict["model"] = model_twiss_df
	
	#with coupling
	twiss_df = _get_twiss_df(base_script, change_dict, outputfile_dir)
	if get_closest_tune:
		twiss_df[DELTA_Q_MIN] = _get_closest_tune(base_script, change_dict, outputfile_dir)
	twiss_dict["with coupling"] = _add_coupling(twiss_df)
	
	#For guignard
	df_errors = tfs.read(f"{outputfile_dir}/errors.out",index="NAME")
	model_twiss_df["K1SL"] = twiss_df["K1SL"]
	Guignard_df = prepare_twiss_dataframe(model_twiss_df,df_errors = df_errors,max_order = 2)
	twiss_dict["Guignard"] = Guignard_df
	return twiss_dict

def _get_correction_dict(base_script, change_dict, responsematrix, outputfile_dir, accel_settings,get_closest_tune, iterations, 
	variable_categories, optics_params, weights,add_errors_to_df):
	change_dict_local = copy.deepcopy(change_dict)
	twiss_df = _get_twiss_df(base_script, change_dict, outputfile_dir)
	if get_closest_tune:
		twiss_df[DELTA_Q_MIN] = _get_closest_tune(base_script, change_dict_local, outputfile_dir)
		
	if add_errors_to_df:
		df_errors = tfs.read(f"{outputfile_dir}/errors.out",index="NAME")
		twiss_df = prepare_twiss_dataframe(twiss_df,df_errors = df_errors,max_order = 2)	
		
	_tfs_converter(outputfile_dir, twiss_df)
	correction_dict = {"measurement" : twiss_df}
	#correction
	for iteration in range(iterations):
		#save previous correction
		if iteration > 0:
			with open(f"{outputfile_dir}{CORRECT_FILE}","r") as f:
				old_correction = f.read()
	
		global_correction_entrypoint(**accel_settings,
				                 meas_dir=outputfile_dir,
				                 variable_categories=variable_categories,
				                 fullresponse_path=responsematrix,
				                 optics_params=optics_params,
				                 output_dir=outputfile_dir,
				                 weights=weights,
				                 svd_cut=0.01,
				                 max_iter=0)
		#append previous correction
		if iteration > 0:
			with open(f"{outputfile_dir}{CORRECT_FILE}","a") as f:
				f.write(old_correction)

		_change_value(change_dict_local,"%correct","1")
		corrected_df = _get_twiss_df(base_script, change_dict_local, outputfile_dir)
		_tfs_converter(outputfile_dir, corrected_df)
		
		if get_closest_tune:
			corrected_df[DELTA_Q_MIN] = _get_closest_tune(base_script, change_dict_local, outputfile_dir)
		
		if add_errors_to_df:
			df_errors = tfs.read(f"{outputfile_dir}/errors.out",index="NAME")
			corrected_df = prepare_twiss_dataframe(corrected_df,df_errors = df_errors,max_order = 2)
			
		correction_dict[f"{iteration}"] = corrected_df
	return correction_dict

def _get_beta_beat(meas_df, model_dir, twiss_file = "twiss.dat", comparison = "betx_rms"):
	model_df = tfs.read(f"{model_dir}{twiss_file}", index = "NAME")
	merge_df = model_df.merge(meas_df,suffixes=("model","meas"),left_on="NAME",right_on="NAME")
	
	
	betx_rms = np.sqrt(np.mean(((merge_df["BETXmodel"] - merge_df["BETXmeas"]) / merge_df["BETXmodel"] )**2))
	bety_rms = np.sqrt(np.mean(((merge_df["BETYmodel"] - merge_df["BETYmeas"]) / merge_df["BETYmodel"] )**2))
	if comparison == "betx_rms":
		return betx_rms
	elif comparison == "rel_betx":
		return merge_df["Smodel"] , (merge_df["BETXmodel"] - merge_df["BETXmeas"]) / merge_df["BETXmodel"]
	else: 
		raise Exception("invalid comparison method") 
	
	

def _change_value(change_dict, key, value):
	assert key in change_dict.keys(), f"{key} not in change_dict"
	change_dict[key] = value

def _add_coupling(tfs_df):
    cpl = coupling_via_cmatrix(tfs_df)
    tfs_df["F1001R"] = np.real(cpl["F1001"])
    tfs_df["F1001I"] = np.imag(cpl["F1001"])
    tfs_df["F1010R"] = np.real(cpl["F1010"])
    tfs_df["F1010I"] = np.imag(cpl["F1010"])
    return tfs_df


def _remove_abs_outliers(df,fRe,fIm,percentage):
	abs_f = abs(df.loc[:,fRe] + 1j * df.loc[:,fIm])
	abs_sort = abs(abs_f - np.mean(abs_f)).sort_values(ascending=False)
	outlier_BPMS = abs_sort.index[0:int(len(abs_sort) * percentage)].to_numpy()
	return df.drop(outlier_BPMS)


def _tfs_converter(outputfile_dir, measurement_df, remove_outliers = False):
	if not ("F1001R" in measurement_df):
		measurement_df = _add_coupling(measurement_df)
	if remove_outliers:
		measurement_df = _remove_abs_outliers(measurement_df,"F1001R","F1001I",0.05)
			
		
	Re = "F1001R"
	Im = "F1001I"
	new = tfs.TfsDataFrame(index=measurement_df.index)
	new['NAME'] = measurement_df.index
	new[Re] = measurement_df.loc[:, Re]

	new[f"{ERR}{Re}"] = np.zeros(len(new.index))
	new[f"{ERR}{DELTA}{Re}"] = new[f"{ERR}{Re}"]
	new[f"{DELTA}{Re}"] = new[Re]

	new[Im] = measurement_df.loc[:, Im]
	new[f"{ERR}{Im}"] = np.zeros(len(new.index))
	new[f"{ERR}{DELTA}{Im}"] = new[f"{ERR}{Im}"]
	new[f"{DELTA}{Im}"] = new[Im]

	tfs.write(f"{outputfile_dir}/F1001.tfs",new)

def _get_updated_script(base_script, change_dict, assert_list=[]):
	with open(base_script,"r") as mask:	
		script = mask.read()
	
	for quantity in assert_list:
		assert quantity in script, f"{quantity} not in {base_script}"
	
	for key in change_dict:
		script = script.replace(key,change_dict[key])
	assert "%" not in script, f"% in script {base_script}"
	return script
	
def _get_twiss_df(base_script, change_dict, outputfile_dir, assert_list=[]):
	updated_script = _get_updated_script(base_script, change_dict, assert_list=assert_list)
	madx_wrapper.run_string(updated_script,log_file=f"{outputfile_dir}/madx_log.txt",madx_path = MADX_PATH)
	df = _add_coupling(tfs.read(f"{outputfile_dir}twiss.dat",index="NAME"))
	return df
	
def _get_closest_tune(base_script, change_dict, outputfile_dir):
	change_dict_local = copy.deepcopy(change_dict)
	QX , QY = float(change_dict_local["%QX"]) % 1 , float(change_dict_local["%QY"]) % 1
	Q_mean = (QX + QY) / 2
	QX_mean = np.floor(float(change_dict_local["%QX"])) + Q_mean
	QY_mean = np.floor(float(change_dict_local["%QY"])) + Q_mean
	_change_value(change_dict_local,"%QX",str(QX_mean))
	_change_value(change_dict_local,"%QY",str(QY_mean))
	df = _get_twiss_df(base_script, change_dict_local, outputfile_dir, assert_list=[])
	return abs(df["Q1"] - df["Q2"] - 2)
	
def delQmin_old(Qx,Qy,f):
        N = len(f)
        delta = np.abs(Qx%1 - Qy%1)
        return 4 * delta/N * np.sum(np.abs(f))

