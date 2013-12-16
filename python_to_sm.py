



def read_sm_commands(fname_cmd)
	format='jpg'
	fname_read=False
	which_to_plot=[]
	labels_to_plot=[]
	inp_cmd =open(fname_cmd,'r')
	print 'INPUTS:\n'
	for line in inp_cmd.readlines():
		data=line.split()
		if data[0][0]!='#':
			if data[0]=='rcparamstr': plt.rcParams[data[1]] = data[2]
			if data[0]=='rcparamint': plt.rcParams[data[1]] = int(data[2])
			if data[0]=='rcparamfl': plt.rcParams[data[1]] = float(data[2])
			if data[0]=='format': format=data[1]
