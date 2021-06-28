import matplotlib.pyplot as plt
import numpy as np
import tfs
import sys

sys.path.append('/home/eirik/CERN/global_coupling_correction3/global_coupling3/')

from global_coupling3 import _add_coupling 

def plot_f1001(outputfiles,coupling_files):
	fig , (ax1,ax2) = plt.subplots(2)
	for coupling_file in coupling_files:
		print(coupling_file)
		df = tfs.read(coupling_file)
		if "F1001R" not in df.columns:
			df = _add_coupling(df)
		S = df["S"].to_numpy()
		f_1001 = df["F1001R"].to_numpy() + 1j * df["F1001I"].to_numpy()
		ax1.plot(df["S"],np.real(f_1001),label = coupling_file)
		ax2.plot(df["S"],np.imag(f_1001),label = coupling_file)
	ax1.legend()
	ax2.legend()
	plt.show()
	
def plot_f1001_comparison(outputfile_dir,trackone_dir,name,remove_outliers,RDT = "F1001",plot_abs=True):
	getcouple_file = f"{outputfile_dir}/getcouple_free.out"
	getcouple_file2 = f"{outputfile_dir}/getcouple_free2.out"

	getcouple_df = tfs.read(getcouple_file,index="NAME")
	getcouple2_df = tfs.read(getcouple_file2,index="NAME")
	
	
	twiss_df = tfs.read(f"{trackone_dir}/Eirik_twiss_BPM.tfs",index="NAME")
	
	twiss_df = _add_coupling(twiss_df)
	
	merge_df = twiss_df.merge(getcouple_df,suffixes=("twiss","free"),left_on="NAME",right_on="NAME")
	merge2_df = twiss_df.merge(getcouple2_df,suffixes=("twiss","free2"),left_on="NAME",right_on="NAME")
	
	#if remove_outliers:
	#	merge_df = _remove_abs_outliers(merge_df,"F1001Rfree","F1001Ifree",0.05)
	#	merge2_df = _remove_abs_outliers(merge2_df,"F1001Rfree2","F1001Ifree2",0.05)
	
	f_free = merge_df[f"{RDT}Rfree"] + 1j * merge_df[f"{RDT}Ifree"]
	f_free2 = merge2_df[f"{RDT}Rfree2"] + 1j * merge2_df[f"{RDT}Ifree2"]
	
	f_twiss_free = merge_df[f"{RDT}Rtwiss"] + 1j * merge_df[f"{RDT}Itwiss"]
	f_twiss_free2 =  merge2_df[f"{RDT}Rtwiss"] + 1j * merge2_df[f"{RDT}Itwiss"]
	
	f_twiss = twiss_df[f"{RDT}R"] + 1j * twiss_df[f"{RDT}I"]
	
	Q1 = twiss_df.Q1
	Q2 = twiss_df.Q2

	
	if plot_abs:
		fig , ax = plt.subplots()
		#ax.plot(merge_df["Stwiss"],abs(f_free - f_twiss_free),label="$|f_{free} - f_{twiss}|$")
		#ax.plot(merge2_df["Stwiss"],abs(f_free2 - f_twiss_free2),label="$|f_{free2} - f_{twiss}|$")
		ax.plot(twiss_df["S"],abs(f_twiss),label = "twiss")
		ax.plot(merge_df["Stwiss"],abs(f_free),label="analytic")
		ax.plot(merge2_df["Stwiss"],abs(f_free2),label="scaled")
		ax.set_xlabel("Position[m]")
		ax.set_ylabel(f"|{RDT}|")
		ax.legend()
		fig.tight_layout(rect=[0, 0.03, 1, 0.95])
		plt.savefig("plots/" + f"tracking_comparison_{RDT}_{name}_removeOutliers{remove_outliers}.pdf")
		plt.show()
	else:
		fig , (ax1,ax2) = plt.subplots(2)
		ax1.plot(twiss_df["S"],np.real(f_twiss),label = "twiss")
		ax1.plot(merge_df["Stwiss"],np.real(f_free),label="analytic")
		ax1.plot(merge2_df["Stwiss"],np.real(f_free2),label="scaled")
		ax1.set_xlabel("Position[m]")
		ax1.set_ylabel(f"Re({RDT})")
		ax1.legend()
		
		ax2.plot(twiss_df["S"],np.imag(f_twiss),label = "twiss")
		ax2.plot(merge_df["Stwiss"],np.imag(f_free),label="analytic")
		ax2.plot(merge2_df["Stwiss"],np.imag(f_free2),label="scaled")
		ax2.set_xlabel("Position[m]")
		ax2.set_ylabel(f"Im({RDT})")
		ax2.legend()
		
		fig.tight_layout(rect=[0, 0.03, 1, 0.95])
		plt.savefig("plots/" + f"tracking_comparison_{name}_complex.pdf")
		plt.show()
