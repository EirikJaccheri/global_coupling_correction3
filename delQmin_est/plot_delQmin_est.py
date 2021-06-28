import sys
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')
from global_coupling3 import _change_value
from global_coupling3 import _get_beta_beat

from optics_functions.coupling import closest_tune_approach

import numpy as np
import matplotlib.pyplot as plt
import tfs
import pandas as pd
import pickle
import cmath
import copy

FONTSIZE = 16

def delQmin_old(df,Q1=None,Q2=None):
	if Q1 == None:
		Q1 = df["Q1"] % 1
		Q2 = df["Q2"] % 1
		
	delta = Q1 - Q2
	f = df["F1001R"].to_numpy()  + 1j * df["F1001I"].to_numpy()	
	return 4 * abs(delta) * np.mean(abs(f))

def delQmin_old_modified(df, Q1=None, Q2 = None):
	if Q1 == None:
		Q1 = df["Q1"] % 1
		Q2 = df["Q2"] % 1

	f1001 = df["F1001R"].to_numpy() + 1j * df["F1001I"].to_numpy()
	f1010 = df["F1010R"].to_numpy() + 1j * df["F1010I"].to_numpy()
	
	delta = Q1 - Q2
	delQ_min_l = delta * 4 * abs(f1001) / (1 + 4*(abs(f1001)**2)) # - abs(f1010)**2
	return abs(np.mean(delQ_min_l))

#(np.cos(2*np.pi*Q1) - np.cos(2*np.pi*Q2)) / (np.pi*(np.sin(2*np.pi*Q1) + np.sin(2*np.pi*Q2))) / (1 + 4*(abs(f1001)**2 - abs(f1010)**2))

def delQmin_new(df,model_df = None,Q1=None,Q2=None,prefactor_delta = 0):
	
	f = df["F1001R"].to_numpy()  + 1j * df["F1001I"].to_numpy()	
	f1010 = df["F1010R"].to_numpy()  + 1j * df["F1010I"].to_numpy()
	if Q1 == None:
		Q1 = model_df["Q1"] % 1
		Q2 = model_df["Q2"] % 1
	delta = Q1 - Q2
	L = model_df["LENGTH"]
	S = model_df["S"].to_numpy()
	MUX = model_df["MUX"].to_numpy()
	MUY = model_df["MUY"].to_numpy()
	N = len(f)
	deltaS_list = [np.abs(S[i +1] - S[i]) for i in range(N-1)]
	deltaS_list.append(S[-1] - S[-2])
	deltaS = np.array(deltaS_list)
	return abs(4 * delta / L * np.sum(deltaS * f * np.exp(1j * 2*np.pi*(MUX - MUY + prefactor_delta * delta * S / L  ))))

def delQmin_new_modified(df,model_df = None,Q1=None,Q2=None,prefactor_delta = 0):
	
	f = df["F1001R"].to_numpy()  + 1j * df["F1001I"].to_numpy()	
	f1010 = df["F1010R"].to_numpy()  + 1j * df["F1010I"].to_numpy()	
	if Q1 == None:
		Q1 = model_df["Q1"] % 1
		Q2 = model_df["Q2"] % 1
	delta = Q1 - Q2
	L = model_df["LENGTH"]
	S = model_df["S"].to_numpy()
	MUX = model_df["MUX"].to_numpy()
	MUY = model_df["MUY"].to_numpy()
	N = len(f)
	deltaS_list = [np.abs(S[i +1] - S[i]) for i in range(N-1)]
	deltaS_list.append(S[-1] - S[-2])
	deltaS = np.array(deltaS_list)
	
	print(delta - abs((1 - np.exp(2*np.pi*1j*delta)) / 2 / np.pi))
	
	return abs(4 * delta / L * np.sum(deltaS * f /  (1 + 4*(abs(f)**2)) * np.exp(1j * 2*np.pi*(MUX - MUY + prefactor_delta * delta * S / L  ))))
	#return abs(4 * delta * np.sum(f * np.exp(1j * 2 * np.pi * (MUX - MUY))))  
	

		
		
def delQmin_guignard(df, model_dir = None, Q1 = None, Q2 = None , prefactor_delta = 0):
	
	index = df.index[df["K1SL"].to_numpy().nonzero()]
	df = df.loc[index,:]
	k = df["K1SL"].to_numpy()
	if model_dir == None:
		model_df = df
	else:
		model_dir = tfs.read(f"{model_dir}twiss_elements.dat",index="NAME")[df.index]	
		
	betx , bety = model_df["BETX"].to_numpy() , model_df["BETY"].to_numpy()
	mux , muy = model_df["MUX"].to_numpy() , model_df["MUY"].to_numpy()
	S = model_df["S"].to_numpy()
	L = model_df["LENGTH"]
	
	if Q1 == None or Q2 == None:
		Q1 = model_df["Q1"]
		Q2 = model_df["Q2"]
	delta = Q1 - Q2 - 2
	return np.abs(np.sum(np.sqrt(betx*bety) * k * np.exp(-2*np.pi*1j*(mux - muy - prefactor_delta * delta * S / L ))) / (2*np.pi))
"""
def convert_coupling_rdts(df):
	f1001_Cmat = df["F1001R"].to_numpy() + 1j * df["F1001I"].to_numpy()
	f1010_Cmat = df["F1010R"].to_numpy() + 1j * df["F1010I"].to_numpy()
	
	sqrt = np.vectorize(cmath.sqrt)
	arcsinh = np.vectorize(cmath.asinh)
	
	sinh2P = 2 * sqrt(-abs(f1001_Cmat)**2 + abs(f1010_Cmat)**2)
	P = 1/2 * arcsinh(sinh2P)
	
	f1001 = (2 * P / sinh2P) * f1001_Cmat
	f1010 = (2 * P / sinh2P) * f1010_Cmat
	
	df["F1001R"] = np.real(f1001)
	df["F1001I"] = np.imag(f1001)
	df["F1010R"] = np.real(f1010)
	df["F1010I"] = np.imag(f1010)
"""	
def convert_coupling_rdts2(df):
	f1001_Cmat = df["F1001R"].to_numpy() + 1j * df["F1001I"].to_numpy()
	f1010_Cmat = df["F1010R"].to_numpy() + 1j * df["F1010I"].to_numpy()
	
	
	sqrt = np.vectorize(cmath.sqrt)
	arctanh = np.vectorize(cmath.atanh)
	
	tanh2P = 2 * sqrt(-abs(f1001_Cmat)**2 + abs(f1010_Cmat)**2)
	P = 1/2 * arctanh(tanh2P)
	
	f1001 = (2 * P / tanh2P) * f1001_Cmat
	f1010 = (2 * P / tanh2P) * f1010_Cmat
	
	
	df["F1001R"] = np.real(f1001)
	df["F1001I"] = np.imag(f1001)
	df["F1010R"] = np.real(f1010)
	df["F1010I"] = np.imag(f1010)



	
def plot_delQmin_est(outputfile_dir, pickle_name, savename, model_dir):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_correction_dict = pickle.load(p)
		
	fig , ax = plt.subplots()
	suptitle = ""
	for key in multiple_correction_dict:
		delQmin = multiple_correction_dict[key].loc[:,"deltaQmin"].to_numpy()[0]
		df = multiple_correction_dict[key]
		df["F1001"] = df["F1001R"] + 1j * df["F1001I"]
		
		if key == "measurement":
			label = "before correction"
			suptitle += f"$\Delta Q_{{min}}^0$ = {delQmin :.3e}  "
		else:
			label = f"correction {str(int(key) + 1)}"
			
		ax.plot(multiple_correction_dict[key]["S"], abs(multiple_correction_dict[key]["F1001R"] + 1j * multiple_correction_dict[key]["F1001I"]),label = label)
	suptitle += f"$\Delta Q_{{min}}^{{cor}}$ = {delQmin :.3e}  "
	ax.legend(fontsize=FONTSIZE)
	ax.set_xlabel("position[m]",fontsize=FONTSIZE)
	ax.set_ylabel("$|f_{1001}|$",fontsize=FONTSIZE)
	fig.suptitle(suptitle,fontsize=FONTSIZE)
	plt.savefig(f"plots/{savename}")
	plt.tight_layout()
	plt.show()
	
	
def plot_sum_and_dif(outputfile_dir, pickle_name, savename, model_dir):
	
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_correction_dict = pickle.load(p)
		
	
	fig , ax1 = plt.subplots()
	suptitle = "before cor     after cor \n"
	for key in multiple_correction_dict:
		delQmin = multiple_correction_dict[key]["deltaQmin"].to_numpy()[0]
		
		df = multiple_correction_dict[key]
		df["F1001"] = df["F1001R"] + 1j * df["F1001I"]
		df["1010"] = df["F1010R"] + 1j * df["F1010I"]
	
		if key == "measurement":
			label = "before correction"
			suptitle += f"$\Delta Q_{{min}}^0$ = {delQmin :.3e}  "
		else:
			label = f"correction {str(int(key) + 1)}"
			
		ax1.plot(multiple_correction_dict[key]["S"], abs(df["F1001"].to_numpy()) - abs(df["1010"].to_numpy()),label = label)
		
	suptitle += f"$\Delta Q_{{min}}^{{cor}}$ = {delQmin :.3e}  "
	ax1.legend(fontsize=FONTSIZE)
	ax1.set_xlabel("position[m]",fontsize=FONTSIZE)
	ax1.set_ylabel("$|f_{1001}| - |f_{1010}|$",fontsize=FONTSIZE)
	
	fig.suptitle(suptitle,fontsize=FONTSIZE)
	plt.savefig(f"plots/{savename}")
	plt.tight_layout()
	plt.show()
	
			
def plot_tune_split(outputfile_dir, pickle_name, savename, model_dir, QX_l, QY_l):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_twiss_dict = pickle.load(p)
	
	tune_split_l = []
	delQmin_l = []
	delQmin_TobRog_l = []
	delQmin_Franchi_l = []
	delQmin_Calaga_l = []
	delQmin_Guignard_l = []
	test = []
	for i, key in enumerate(multiple_twiss_dict):
		model_df = multiple_twiss_dict[key]["model"]
		coupling_df = multiple_twiss_dict[key]["with coupling"]
		Guignard_df = multiple_twiss_dict[key]["Guignard"]
		
		#Q1 = model_df["Q1"] % 1
		#Q2 = model_df["Q2"] % 1
		Q1 = coupling_df["Q1"] % 1
		Q2 = coupling_df["Q2"] % 1
		
		coupling_df["F1001"] = coupling_df["F1001R"] + 1j * coupling_df["F1001I"]
		coupling_df["1010"] = coupling_df["F1010R"] + 1j * coupling_df["F1010I"]
		delQmin_Calaga = np.abs(np.mean(closest_tune_approach(coupling_df,method="calaga").to_numpy()))
		delQmin_Guignard = delQmin_guignard(Guignard_df,prefactor_delta = 1)
		
	
		#convert_coupling_rdts2(coupling_df) model_df.loc[coupling_df.index,:]
		
		test.append(coupling_df["DQMIN"])
		delQmin_TobRog = delQmin_new_modified(coupling_df,model_df = coupling_df,Q1=Q1,Q2=Q2,prefactor_delta = -1)
		delQmin_Franchi = delQmin_old_modified(coupling_df,Q1=Q1,Q2=Q2)
		
		
		tune_split_l.append( model_df["Q1"] % 1 - model_df["Q2"] % 1)
		delQmin_l.append(coupling_df["deltaQmin"][0])
		delQmin_TobRog_l.append(delQmin_TobRog)
		delQmin_Franchi_l.append(delQmin_Franchi)
		delQmin_Calaga_l.append(delQmin_Calaga)
		delQmin_Guignard_l.append(delQmin_Guignard)
	
	delQmin_l = np.array(delQmin_l)
	delQmin_TobRog_l = np.array(delQmin_TobRog_l)
	delQmin_Franchi_l = np.array(delQmin_Franchi_l)
	delQmin_Calaga_l = np.array(delQmin_Calaga_l)
	delQmin_Guignard_l = np.array(delQmin_Guignard_l)	
	
	test = np.array(test)
	print((test - delQmin_TobRog_l) / delQmin_TobRog_l)
			
	fig , ax = plt.subplots()

	ax.plot(tune_split_l, 1000 * delQmin_Calaga_l, label = "TEAPOT")
	ax.plot(tune_split_l, 1000 * delQmin_Guignard_l, label = "Guignard")
	ax.plot(tune_split_l, 1000 * delQmin_Franchi_l, label = "Franchi")
	ax.plot(tune_split_l, 1000 * delQmin_TobRog_l, label = "Rdt Phase Avg")
	ax.plot(tune_split_l, 1000 * delQmin_l, label = "Matching")
	#ax.plot(tune_split_l, 1000 * test, label = "DELQMIN")
	
	ax.set_ylabel("$\Delta Q_{min}\,[10^{-3}]$",fontsize = FONTSIZE)
	ax.set_xlabel("$\Delta$",fontsize = FONTSIZE)
	ax.tick_params(axis="x",labelsize=16)
	ax.tick_params(axis="y",labelsize=16)
	#ax.set_ylim(0,5)
	ax.legend(fontsize = FONTSIZE)
	plt.tight_layout()
	plt.savefig(f"plots/{savename}")
	plt.show()


def plot_tune_split_test(outputfile_dir, pickle_name, savename, model_dir, QX_l, QY_l):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_twiss_dict = pickle.load(p)
	
	tune_split_l = []
	delQmin_l = []
	delQmin_TobRog_l = []
	delQmin_Franchi_l = []
	delQmin_Calaga_l = []
	delQmin_Guignard_l = []
	test = []
	for i, key in enumerate(multiple_twiss_dict):
		model_df = multiple_twiss_dict[key]["model"]
		coupling_df = multiple_twiss_dict[key]["with coupling"]
		Guignard_df = multiple_twiss_dict[key]["Guignard"]
		
		Q1 = model_df["Q1"] % 1
		Q2 = model_df["Q2"] % 1
		#Q1 = coupling_df["Q1"] % 1
		#Q2 = coupling_df["Q2"] % 1
		
		coupling_df["F1001"] = coupling_df["F1001R"] + 1j * coupling_df["F1001I"]
		coupling_df["1010"] = coupling_df["F1010R"] + 1j * coupling_df["F1010I"]
		delQmin_Calaga = np.abs(np.mean(closest_tune_approach(coupling_df,method="calaga").to_numpy()))
		delQmin_Guignard = delQmin_guignard(Guignard_df,prefactor_delta = 1)
		
	
		convert_coupling_rdts2(coupling_df)
		
		delQmin_TobRog = delQmin_new(coupling_df,model_df = model_df.loc[coupling_df.index,:],Q1=Q1,Q2=Q2,prefactor_delta = 0)
		delQmin_Franchi = delQmin_old(coupling_df,Q1=Q1,Q2=Q2)
		
		tune_split_l.append( model_df["Q1"] % 1 - model_df["Q2"] % 1)
		delQmin_l.append(coupling_df["deltaQmin"][0])
		delQmin_TobRog_l.append(delQmin_TobRog)
		delQmin_Franchi_l.append(delQmin_Franchi)
		delQmin_Calaga_l.append(delQmin_Calaga)
		delQmin_Guignard_l.append(delQmin_Guignard)
	
	tune_split_l = np.array(tune_split_l)
	delQmin_l = np.array(delQmin_l)
	delQmin_TobRog_l = np.array(delQmin_TobRog_l)
	delQmin_Franchi_l = np.array(delQmin_Franchi_l)
	delQmin_Calaga_l = np.array(delQmin_Calaga_l)
	delQmin_Guignard_l = np.array(delQmin_Guignard_l)	
	
	fig , ax = plt.subplots()
	ax.plot(tune_split_l, 1000 * delQmin_Calaga_l, label = "TEAPOT")
	ax.plot(tune_split_l, 1000 * delQmin_Guignard_l, label = "Guignard")
	ax.plot(tune_split_l, 1000 * delQmin_Franchi_l, label = "Franchi")
	ax.plot(tune_split_l, 1000 * delQmin_TobRog_l, label = "Rdt Phase Avg")
	ax.plot(tune_split_l, 1000 * delQmin_l, label = "Matching")
	
	ax.set_ylabel("$\Delta Q_{min}\,[10^{-3}]$",fontsize = FONTSIZE)
	ax.set_xlabel("$\Delta$",fontsize = FONTSIZE)
	ax.tick_params(axis="x",labelsize=16)
	ax.tick_params(axis="y",labelsize=16)
	#ax.set_ylim(0,5)
	ax.legend(fontsize = FONTSIZE)
	plt.tight_layout()
	plt.savefig(f"plots/{savename}")
	plt.show()

def plot_f1001_f1010(outputfile_dir, pickle_name, savename, model_dir):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_twiss_dict = pickle.load(p)
	
	
	for i, key in enumerate(multiple_twiss_dict):
		model_df = multiple_twiss_dict[key]["model"]
		coupling_df = multiple_twiss_dict[key]["with coupling"]
		Guignard_df = multiple_twiss_dict[key]["Guignard"]
		
	
		S = coupling_df["S"] / 1000
		f1001 = coupling_df["F1001R"] + 1j * coupling_df["F1001I"]
		f1010 = coupling_df["F1010R"] + 1j * coupling_df["F1010I"]
		
		Q1 = coupling_df["Q1"] % 1
		Q2 = coupling_df["Q2"] % 1
		
		coupling_df["F1001"] = f1001
		coupling_df["1010"] = f1010
		delQmin_Calaga = np.abs(np.mean(closest_tune_approach(coupling_df,method="calaga").to_numpy()))
		delQmin_Guignard = delQmin_guignard(Guignard_df,prefactor_delta = 1)
	
		#convert_coupling_rdts2(coupling_df)
		
		delQmin_TobRog = delQmin_new_modified(coupling_df,model_df = model_df.loc[coupling_df.index,:],Q1=Q1,Q2=Q2,prefactor_delta = -1)
		delQmin_Franchi = delQmin_old_modified(coupling_df,Q1=Q1,Q2=Q2)
		
		
		
		fig , ax = plt.subplots()
		ax.plot(S,abs(f1001),label = "$|f_{1001}|$")
		ax.plot(S,abs(f1010),label = "$|f_{1010}|$")
		
		ax.set_xlabel("position [km]",fontsize=FONTSIZE)
		ax.set_ylabel("$|f_{jklm}|$",fontsize=FONTSIZE)
		ax.tick_params(axis="x",labelsize=16)
		ax.tick_params(axis="y",labelsize=16)
		ax.legend(fontsize=FONTSIZE)
		plt.tight_layout()
		plt.savefig(f"plots/{savename}")
		plt.show()
		
	
	
def plot_multiple_coupling(outputfile_dir, pickle_name, savename, model_dir):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_twiss_dict = pickle.load(p)
	
	x = []
	label_l = []
	delQmin_l = []
	delQmin_TobRog_l = []
	delQmin_Franchi_l = []
	delQmin_Calaga_l = []
	delQmin_Guignard_l = []
	for i, key in enumerate(multiple_twiss_dict):
		model_df = multiple_twiss_dict[key]["model"]
		coupling_df = multiple_twiss_dict[key]["with coupling"]
		Guignard_df = multiple_twiss_dict[key]["Guignard"]
		
		#Q1 = model_df["Q1"] % 1
		#Q2 = model_df["Q2"] % 1
		Q1 = coupling_df["Q1"] % 1
		Q2 = coupling_df["Q2"] % 1
		
		coupling_df["F1001"] = coupling_df["F1001R"] + 1j * coupling_df["F1001I"]
		coupling_df["1010"] = coupling_df["F1010R"] + 1j * coupling_df["F1010I"]
		
		
		delQmin_Calaga = np.abs(np.mean(closest_tune_approach(coupling_df,method="calaga").to_numpy()))
		delQmin_Guignard = delQmin_guignard(Guignard_df,prefactor_delta = 1)
	
		#convert_coupling_rdts(coupling_df)
		
		#delQmin_TobRog = delQmin_new(coupling_df,model_df = model_df.loc[coupling_df.index,:],Q1=Q1,Q2=Q2,prefactor_delta = -1)
		#delQmin_Franchi = delQmin_ol(coupling_df)
		delQmin_TobRog = delQmin_new_modified(coupling_df,model_df = model_df.loc[coupling_df.index,:],Q1=Q1,Q2=Q2,prefactor_delta = -1)
		delQmin_Franchi = delQmin_old_modified(coupling_df,Q1=Q1,Q2=Q2)
		
		
		x.append(i+1)
		label_l.append(f"E{i + 1}")
		delQmin_l.append(coupling_df["deltaQmin"][0])
		delQmin_TobRog_l.append(delQmin_TobRog)
		delQmin_Franchi_l.append(delQmin_Franchi)
		delQmin_Calaga_l.append(delQmin_Calaga)
		delQmin_Guignard_l.append(delQmin_Guignard)
	
	skew_index = Guignard_df["K1SL"].to_numpy().nonzero()
	print(Guignard_df.loc[Guignard_df.index[skew_index],["BETX","BETY","K1SL"]])
	
	x = np.array(x)
	delQmin_l = np.array(delQmin_l)
	delQmin_TobRog_l = np.array(delQmin_TobRog_l)
	delQmin_Franchi_l = np.array(delQmin_Franchi_l)
	delQmin_Calaga_l = np.array(delQmin_Calaga_l)
	delQmin_Guignard_l = np.array(delQmin_Guignard_l)
	
	print(delQmin_l)
	print(delQmin_TobRog_l)
	print(delQmin_Franchi_l)
	print(delQmin_Calaga_l)
	print(delQmin_Guignard_l)
	
	
	width = 0.15	
	fig , ax = plt.subplots()
	ax.bar(x - 1.5 * width,100 *  (delQmin_Calaga_l - delQmin_l) / delQmin_l, width, label = "Teapot")
	ax.bar(x - 0.5 * width,100 *  (delQmin_Guignard_l - delQmin_l) / delQmin_l, width, label = "Guignard")
	ax.bar(x + 0.5 * width,100 *  (delQmin_Franchi_l - delQmin_l) / delQmin_l, width, label = "Franchi")
	ax.bar(x + 1.5 * width,100 *  (delQmin_TobRog_l - delQmin_l) / delQmin_l, width, label = "Rdt Phase Avg")
	
	
	ax.set_ylabel(r"$\left(\Delta Q_{min}^{est} - \Delta Q_{min}^{match}\right)$ [%]",fontsize=FONTSIZE)
	ax.set_xticks(x)
	ax.set_xticklabels(label_l,fontsize=FONTSIZE)
	ax.tick_params(axis="y",labelsize=16)
	#ax.set_ylim(0,0.005)
	ax.legend(loc='lower center',fontsize=12, bbox_to_anchor=(0.5, 1.03),
          fancybox=True, shadow=False, ncol=5)
	ax.set_ylim(-100,100)
	
	plt.tight_layout()
	plt.savefig(f"plots/{savename}")
	plt.show()


def _get_lists(base_script,change_dict,N):
	delta_l = np.linspace(-0.1,0.1,N)
	change_dict_list = []
	base_script_list = []
	
	for i in range(len(delta_l)):
		QX = 0.30 + delta_l[i] / 2
		QY = 0.30 - delta_l[i]/ 2
		change_dict_local = copy.deepcopy(change_dict)
		_change_value(change_dict_local, "%QX",  str(62 + float(QX)))
		_change_value(change_dict_local, "%QY",  str(60 + float(QY)))
		change_dict_list.append(change_dict_local)
		base_script_list.append(base_script)
	return base_script_list, change_dict_list
	
	
	

