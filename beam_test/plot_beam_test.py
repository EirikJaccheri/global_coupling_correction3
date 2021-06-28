import numpy as np
import matplotlib.pyplot as plt
import pickle

FONTSIZE = 16

def plot_beam_test(outputfile_dir,pickle_name,optics,label,filename):
	
	pos_l = np.arange(0,len(optics),1)
	deltaQmin_l = np.zeros(len(optics)) 
	for i , optics in enumerate(optics):
		with open(f"{outputfile_dir}/{pickle_name}opticsfile.{optics}","rb") as p:
			multiple_correction_dict = pickle.load(p)
		
		for key in multiple_correction_dict:
			delQmin = multiple_correction_dict[key]["deltaQmin"].to_numpy()[0]
			print(optics,delQmin)
			deltaQmin_l[i] = delQmin

	
	labels = ["11","8.3","4.1","2.1"]
	
	fig , ax = plt.subplots()
	ax.plot(pos_l,deltaQmin_l,"x",label=label)
	plt.xticks(pos_l, labels,fontsize = FONTSIZE) 
	ax.set_xlabel(r"$\beta *$",fontsize = FONTSIZE)
	ax.set_ylabel(r"$\Delta Q_{min}$",fontsize = FONTSIZE)
	ax.legend(fontsize=FONTSIZE,loc="upper left")
	ax.set_ylim(0,0.04)
	plt.tight_layout()
	plt.savefig(f"plots/{filename}")
	plt.show()
