import numpy as np
import matplotlib.pyplot as plt
import pickle
import tfs

from global_coupling3 import _get_beta_beat

FONTSIZE = 16

def plot_multiple_corrections_bar_diagram(outputfile_dir, pickle_name, plot_name,model_dir,width=0.35):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_correction_dict = pickle.load(p)
	
	N_err = len(multiple_correction_dict)
	N_cor = len(next(iter(multiple_correction_dict.values())))
	
	rect_dict = {key : np.zeros(N_err) for key in next(iter(multiple_correction_dict.values()))}
	beta_beat_l = np.zeros(N_err)
	for i, key_err in enumerate(multiple_correction_dict):
		beta_beat_l[i] = _get_beta_beat(multiple_correction_dict[key_err][list(multiple_correction_dict[key_err].keys())[0]], model_dir)
		for key_corr in multiple_correction_dict[key_err]:
			rect_dict[key_corr][i] = multiple_correction_dict[key_err][key_corr]["deltaQmin"][0]
	print(beta_beat_l)
	
	
	x = np.arange(N_err)
	labels = [f"E{i}" for i in range(1,N_err + 1)]
	fig , ax = plt.subplots()
	for i , key in enumerate(rect_dict):
		if key == "measurement":
			label_str = "before correction"
		else:
			label_str = f"correction{str(int(key) + 1)}"
			
		ax.bar(x +  (i - (N_cor - 1)/2) *  width  , rect_dict[key] / 1e-3, width, label = label_str)
	
	x2_l = np.array([-0.5,0,1,2,3,4,4.5])
	ax.plot(x2_l,np.ones(len(x2_l)),label = "per mil level", color = "red")
	
	ax.set_xticks(x)
	ax.set_xticklabels(labels,fontsize=FONTSIZE)
	ax.tick_params(axis="y",labelsize=16)
	
	ax.set_ylabel("$\Delta Q_{min}\,[10^{-3}]$",fontsize=FONTSIZE) 
	ax.legend(fontsize = FONTSIZE)
	plt.tight_layout()
	plt.savefig(f"plots/{plot_name}")
	plt.show()
	
def plot_betabeating(outputfile_dir, pickle_name, model_dir, plot_name):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_correction_dict = pickle.load(p)
	
	N_err = len(multiple_correction_dict)
	N_cor = len(next(iter(multiple_correction_dict.values())))
	
	rect_dict = {key : np.zeros((N_err,2)) for key in next(iter(multiple_correction_dict.values()))}
	for i, key_err in enumerate(multiple_correction_dict):
		for key_corr in multiple_correction_dict[key_err]:
			rect_dict[key_corr][i][0] = multiple_correction_dict[key_err][key_corr]["deltaQmin"][0]
			rect_dict[key_corr][i][1] = _get_beta_beat(multiple_correction_dict[key_err][key_corr], model_dir)
	
	fig , ax = plt.subplots()
	beta_beat_list = rect_dict[list(rect_dict.keys())[0]].T[1]
	for i , key in enumerate(rect_dict):
		if key == "measurement":
			label_str = key
		else:
			label_str = f"correction{str(int(key) + 1)}"
		
		ax.plot(beta_beat_list, rect_dict[key].T[0], label = label_str)
	ax.legend(fontsize=FONTSIZE)
	ax.set_xlabel(r"$rms\{\Delta \beta_x / \beta_x^0\}$",fontsize=FONTSIZE)
	ax.set_ylabel(r"$\Delta Q_{min}$",fontsize=FONTSIZE)
	plt.tight_layout()
	plt.savefig(f"plots/{plot_name}")
	plt.show()
	
	


"""	
S , betx = _get_beta_beat(multiple_correction_dict[key_err][key_corr], model_dir, comparison = "rel_betx")
label_str = _get_beta_beat(multiple_correction_dict[key_err][key_corr], model_dir)
plt.plot(S, betx, label = label_str)
plt.legend()
plt.show()
"""
