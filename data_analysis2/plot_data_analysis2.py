import tfs  
import matplotlib.pyplot as plt
import numpy as np
import pickle 

import sdds
from omc3.tbt import handler

import sys
sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

from global_coupling3 import _remove_abs_outliers
from global_coupling3 import delQmin_old

FONTSIZE = 16
               
def plot_tbt_data(worrking_dir,sdds_file,BPM):
        sdds_data = handler.read_tbt(sdds_file,"lhc")
        df = sdds_data.matrices[0]['X']
        print(df)
        
        fig , ax = plt.subplots()
        ax.plot(df.columns.values,df.loc[BPM,:],label=BPM)
        ax.set_xlabel("turns")
        ax.set_ylabel("AmplitudeX[m]")
        ax.legend()
        plt.tight_layout()
        plt.savefig(f"plots/tbt.pdf")
        plt.show()
        
def plot_f1001_comparison(outputfile_dir,coupling_files,sdds_file,Qx,Qy,plot_abs=True):
	label_dir = {
	"getcouple_free.out":"analytic",
	"getcouple_free2.out":"scaled",
	"getcouple.out" : "gett",
	}

	if plot_abs:
		fig , ax = plt.subplots()
	else:	
		fig , (ax1,ax2) = plt.subplots(2)
	suptitle_str = ""
	for coupling_file in coupling_files: 
		df = tfs.read(f"{outputfile_dir}{coupling_file}",index="NAME")
		df = _remove_abs_outliers(df,"F1001R","F1001I",0.05)
		S = df.loc[:,"S"]
		f_1001 = df.loc[:,"F1001R"] + 1j *  df.loc[:,"F1001I"]

		delQmin = delQmin_old(Qx,Qy,f_1001)
		suptitle_str += f"$|C^-|_{{{label_dir[coupling_file]}}}$ = {delQmin : .3e}   "

		if plot_abs:
			ax.plot(S,abs(f_1001),label = label_dir[coupling_file])
		else:	
			ax1.plot(S,np.real(f_1001),label = label_dir[coupling_file])
			ax2.plot(S,np.imag(f_1001),label = label_dir[coupling_file])
	if plot_abs:
		ax.set_xlabel("position[m]")
		ax.set_ylabel("$|f_{1001}|$")
		ax.legend()
	else:
		ax1.set_xlabel("position[m]")
		ax1.set_ylabel("$Re\{f_{1001}\}$")
		ax1.legend()

		ax2.set_xlabel("position[m]")
		ax2.set_ylabel("$Im\{f_{1001}\}$")
		ax2.legend()


	fig.suptitle(suptitle_str)
	plt.savefig(f"plots/f1001_comparison_{sdds_file}.pdf")
	plt.show()

def plot_abs_f1001(outputfile_dir,pickle_name):
	with open(f"{outputfile_dir}{pickle_name}",'rb') as p:
		coupling_dict = pickle.load(p)

	N_files = len(coupling_dict.keys())
	x_list = np.arange(0,N_files,1)
	x_labels = []
	avg_f_1001_dict = {}
	#getting average
	for i,key in enumerate(coupling_dict):
		for compensation_method in coupling_dict[key]:
			df = coupling_dict[key][compensation_method]
			f_1001 = df["F1001R"] + 1j * df["F1001I"]
			if compensation_method not in avg_f_1001_dict:
				avg_f_1001_dict[compensation_method] = f_1001
			else:
				avg_f_1001_dict[compensation_method] += f_1001
			#x_labels.append(key[22:30:].replace('_',':'))
		x_labels.append(key[22:27:].replace('_',':'))
		
	avg_f_1001_dict["analytic"] /= N_files
	avg_f_1001_dict["scaled"] /= N_files		
	avg_diff_dict = {
	"analytic":np.zeros(N_files,dtype=float),
        "scaled":np.zeros(N_files,dtype=float)
	}
	for i,key in enumerate(coupling_dict):
		for compensation_method in coupling_dict[key]:
			df = coupling_dict[key][compensation_method]
			f_1001 = df["F1001R"] + 1j * df["F1001I"]
			avg_diff_dict[compensation_method][i] = np.nanmean(abs(f_1001 - avg_f_1001_dict[compensation_method]) / abs(avg_f_1001_dict[compensation_method]))
	
	fig,ax = plt.subplots()
	ax.plot(x_list,avg_diff_dict["analytic"],label = "analytic")
	ax.plot(x_list,avg_diff_dict["scaled"],label = "scaled")
	ax.set_ylabel("$mean\{|f_{1001} - <f_{1001}>|\,/\,|<f_{1001}>|\}$")
	ax.set_ylim(0,1)
	ax.legend()
	plt.xticks(x_list,x_labels,rotation="horizontal")
	plt.savefig("plots/plot_abs_f1001_{sdds_file}.pdf")
	plt.show()

def plot_abs_f1001_difference(outputfile_dir,pickle_name):
	with open(f"{outputfile_dir}{pickle_name}",'rb') as p:
		coupling_dict = pickle.load(p)

	N_files = len(coupling_dict.keys())
	x_list = np.arange(0,N_files,1)
	x_labels = []
	abs_diff = np.zeros(N_files)
	
	for i,key in enumerate(coupling_dict):

		df = coupling_dict[key]["scaled"].merge( coupling_dict[key]["analytic"],suffixes=("scaled","analytic"),left_on="NAME",right_on="NAME")
		
		f_1001_scaled = df["F1001Rscaled"] + 1j * df["F1001Iscaled"]
		f_1001_analytic = df["F1001Ranalytic"] + 1j * df["F1001Ianalytic"]

		abs_diff[i] = np.mean(abs((f_1001_scaled - f_1001_analytic)) / (abs(f_1001_analytic)))
		x_labels.append(key[22:27:].replace('_',':'))

	fig,ax = plt.subplots()
	ax.plot(x_list,abs_diff)
	ax.set_ylabel("$mean\{|f_{1001}^{analytic} - f_{1001}^{scaled}|\,/\,|f_{1001}^{analytic}|\}$")
	ax.set_ylim(0,1)
	plt.xticks(x_list,x_labels,rotation="horizontal")
	plt.savefig("plots/plot_abs_f1001_difference_{sdds_file}.pdf")
	plt.show()

def plot_knob(outputfile_dir,pickle_name,Qx,Qy,beam,plot_abs=True):
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
                
                mean_scaled = np.mean(abs(knob_dict["scaled"]))
                std_scaled = np.std(abs(knob_dict["scaled"]))
                mean_analytic = np.mean(abs(knob_dict["analytic"]))
                std_analytic = np.std(abs(knob_dict["analytic"]))
                
                suptitle = f"$|C^-|_{{analytic}} = $ {mean_analytic : .3e} $\pm$ {std_analytic : .3e} \n $|C^-|_{{scaled}} = $ {mean_scaled : .3e} $\pm$ {std_scaled : .3e}"
                fig.suptitle(suptitle)
                print(f"scaled mean $|C^-|$ = {mean_scaled}")
                print(f"analytic mean $|C^-|$ = {mean_analytic}")
                
                plt.xticks(x_list,x_labels,rotation="horizontal")
                ax.legend(fontsize=FONTSIZE)
                ax.set_ylim(0,0.005)
                plt.tight_layout()
                plt.savefig(f"plots/real_data_knob_beam{beam}_abs.pdf")
                		
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

