import sys
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

from global_coupling3 import _get_beta_beat

import numpy as np
import matplotlib.pyplot as plt
import tfs
import pickle



FONTSIZE = 16

def latex_float(f):
    float_str = "{0:.2e}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str

def plot_single_correction(outputfile_dir, pickle_name, savename, model_dir):
	with open(f"{outputfile_dir}/{pickle_name}","rb") as p:
		multiple_correction_dict = pickle.load(p)
		
	
	fig , ax = plt.subplots()
	suptitle = ""
	for key in multiple_correction_dict:
		delQmin = multiple_correction_dict[key]["deltaQmin"].to_numpy()[0]
		print(key,"betabeating",_get_beta_beat(multiple_correction_dict[key], model_dir))
		#S, b = _get_beta_beat(multiple_correction_dict[key], model_dir, comparison = "rel_betx")
		#plt.plot(S,b)
		#plt.show()
		print("*******")
		if key == "measurement":
			label = f"before correction $\Delta Q_{{min}} = {latex_float(delQmin)}$"
			suptitle += f"$\Delta Q_{{min}}^0$ = {delQmin :.3e}  "
		else:
			delQmin_str = latex_float(delQmin)
			label = f"correction {str(int(key) + 1)}  $\Delta Q_{{min}} = {latex_float(delQmin)}$"
			
		ax.plot(multiple_correction_dict[key]["S"] / 1000, abs(multiple_correction_dict[key]["F1001R"] + 1j * multiple_correction_dict[key]["F1001I"]),label = label)
	suptitle += f"$\Delta Q_{{min}}^{{cor}}$ = {delQmin :.3e}  "
	ax.legend(fontsize=FONTSIZE)
	ax.set_xlabel("position[km]",fontsize=FONTSIZE)
	ax.set_ylabel("$|f_{1001}|$",fontsize=FONTSIZE)
	ax.tick_params(axis="x",labelsize=16)
	ax.tick_params(axis="y",labelsize=16)
	
	#fig.suptitle(suptitle,fontsize=FONTSIZE)
	plt.tight_layout(rect=(0.01,0,1,1))
	plt.savefig(f"plots/{savename}")
	plt.show()
