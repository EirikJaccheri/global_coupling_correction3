import sys
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

import tfs  
import matplotlib.pyplot as plt
import numpy as np
import pickle

#from utilities import _add_coupling
from global_coupling3 import _remove_abs_outliers
from global_coupling3 import delQmin_old

import sdds
from omc3.tbt import handler

FONTSIZE=16
def plot_tbt_data(data_dir,sdds_file,BPM):
        sdds_data = handler.read_tbt(f"{data_dir}{sdds_file}","lhc")
        df = sdds_data.matrices[0]['X']
        
        fig , ax = plt.subplots()
        ax.plot(df.columns.values,df.loc[BPM,:],label=BPM)
        ax.set_xlabel("turns")
        ax.set_ylabel("AmplitudeX[m]")
        ax.legend()
        plt.tight_layout()
        #plt.savefig(f"plots/tbt_{name}{noise}{BPM}.pdf")
        plt.show()


def plot_f1001_comparison(outputfile_dir,coupling_files,sdds_file,Qx,Qy):
	label_dir = {
	"getcouple_free.out":"analytic",
	"getcouple_free2.out":"scaled",
	"getcouple.out" : "gett",
	}
	fig , ax = plt.subplots()
	suptitle_str = ""
	for coupling_file in coupling_files: 
		df = tfs.read(f"{outputfile_dir}{coupling_file}",index="NAME")
		df = _remove_abs_outliers(df,"F1001R","F1001I",0.05)
		S = df.loc[:,"S"]
		f_1001 = df.loc[:,"F1001R"] + 1j *  df.loc[:,"F1001I"]
		
		delQmin = delQmin_old(Qx,Qy,f_1001)
		suptitle_str += f"$\Delta Q_{{min}}^{{{label_dir[coupling_file]}}}$ = {delQmin : .3e}	"
		
		ax.plot(S,abs(f_1001),label = label_dir[coupling_file])
	ax.set_xlabel("position[m]")
	ax.set_ylabel("$|f_{1001}|$")
	ax.legend()
	
	fig.suptitle(suptitle_str)
	plt.savefig(f"plots/f1001_comparison_{sdds_file}.pdf")
	plt.show()

def plot_Cmin(outputfile_dir,pickle_name,Qx,Qy,beam):
	with open(f"{outputfile_dir}{pickle_name}",'rb') as p:
		coupling_dict = pickle.load(p)
	
	N_files = len(coupling_dict.keys())
	x_list = np.arange(0,N_files,1)
	x_labels = []
	Cmin_dict = {
	"analytic":np.zeros(N_files),
	"scaled":np.zeros(N_files)
	}
	for i,key in enumerate(coupling_dict):
		for compensation_method in coupling_dict[key]:
			df = coupling_dict[key][compensation_method]
			df = _remove_abs_outliers(df,"F1001R","F1001I",0.05)
			f_1001 = df.loc[:,"F1001R"] + 1j *  df.loc[:,"F1001I"]
			Cmin = delQmin_old(Qx,Qy,f_1001)
			Cmin_dict[compensation_method][i] = Cmin
		x_labels.append(key[22:30:])
		#print(str(key[22:30:]))
		print(x_labels)
	fig,ax = plt.subplots()
	ax.plot(x_list,Cmin_dict["analytic"],"x",label="analytic")
	ax.plot(x_list,Cmin_dict["scaled"],"x",label="scaled")
	
	plt.xticks(x_list,x_labels,rotation="vertical")
	ax.legend()
	plt.tight_layout()
	plt.savefig(f"plots/real_data_beam{beam}.pdf")
	plt.show()
	
def plot_knobs(outputfile_dir,pickle_name,Qx,Qy,beam,plot_abs=True):
	with open(f"{outputfile_dir}{pickle_name}",'rb') as p:
		coupling_dict = pickle.load(p)
	
	N_files = len(coupling_dict.keys())
	x_list = np.arange(0,N_files,1)
	x_labels = []
	knob_dict = {
	"analytic":np.zeros(N_files,dtype=np.complex_),
	"scaled":np.zeros(N_files,dtype=np.complex_)
	}
	for i,key in enumerate(coupling_dict):
		for compensation_method in coupling_dict[key]:
			df = coupling_dict[key][compensation_method]
			knob_Re =  coupling_dict[key][compensation_method]["knob_Re"][0]
			knob_Im =  coupling_dict[key][compensation_method]["knob_Im"][0]
			knob_dict[compensation_method][i] = knob_Re + 1j * knob_Im
		#x_labels.append(key[22:30:].replace('_',':'))
		x_labels.append(key[22:27:].replace('_',':'))
		
	if plot_abs:
		fig,ax = plt.subplots()
		unit = 1e-3
		ax.plot(x_list,abs(knob_dict["analytic"]),"x",label="analytic")
		ax.plot(x_list,abs(knob_dict["scaled"]),"x",label="scaled")
		ax.set_xlabel("time 6 aug 2018",fontsize=FONTSIZE)
		ax.set_ylabel(f"$|C^-|$",fontsize=FONTSIZE)
		plt.xticks(x_list,x_labels,rotation="horizontal")
		ax.legend(fontsize=FONTSIZE)
		plt.tight_layout()
		plt.savefig(f"plots/real_data_knob_beam{beam}_abs.pdf")
		print(f"analytic Real mean:","{:.3e}".format(np.mean(np.real(knob_dict["analytic"]))),"std:","{:.3e}".format(np.std(np.real(knob_dict["analytic"]))))
		print(f"analytic Imag mean:","{:.3e}".format(np.mean(np.imag(knob_dict["analytic"]))),"std:","{:.3e}".format(np.std(np.imag(knob_dict["analytic"]))))
		print(f"scaled Real mean:","{:.3e}".format(np.mean(np.real(knob_dict["scaled"]))),"std:","{:.3e}".format(np.std(np.real(knob_dict["scaled"]))))
		print(f"scaled Imag mean:","{:.3e}".format(np.mean(np.imag(knob_dict["scaled"]))),"std:","{:.3e}".format(np.std(np.imag(knob_dict["scaled"]))))
		plt.show()	
		
		
		
	else:
		fig , (ax1,ax2) = plt.subplots(2)	
		
		l1 = ax1.plot(x_list,np.real(knob_dict["analytic"])/1e-3,"x",label="analytic")
		l2 = ax1.plot(x_list,np.real(knob_dict["scaled"])/1e-3,"x",label="scaled")
		plt.setp(ax1.get_xticklabels(), visible=False)
		#ax1.set_xlabel("time",fontsize=FONTSIZE)
		ax1.set_ylabel("$Re\{C^-\}\,[10^{-3}]$",fontsize=FONTSIZE)
		ax1.tick_params(axis="y",labelsize=FONTSIZE)
		ax1.set_ylim(-2,2)
		#ax1.legend()
		
		l3 = ax2.plot(x_list,np.imag(knob_dict["analytic"])/1e-3,"x",label="analytic")
		l4 = ax2.plot(x_list,np.imag(knob_dict["scaled"])/1e-3,"x",label="scaled")
		#ax2.set_xlabel("time 6 aug 2018",fontsize=FONTSIZE)
		ax2.set_ylabel("$Im\{C^-\}\,[10^{-3}]$",fontsize=FONTSIZE)
		ax2.tick_params(axis="y",labelsize=FONTSIZE)
		ax2.set_ylim(-2,2)
		#ax2.legend(fontsize=FONTSIZE)
		
		fig.legend([l1,l2],labels=["analytic","scaled"],fontsize=FONTSIZE,loc="upper center",ncol=2,bbox_to_anchor=(0.56, 1.02),fancybox=False,shadow=False)
		plt.xticks(x_list,x_labels,rotation="horizontal",fontsize=14)
		plt.tight_layout()
		plt.savefig(f"plots/real_data_knob_beam{beam}_complex.pdf")
		plt.show()
	
			
