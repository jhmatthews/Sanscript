
import matplotlib.pyplot as plt

def read_params(param_filename):
	'''reads in a parameter file, with a string param'''
	param_file=open(param_filename, 'r')
	for line in param_file:
		data=line.split()
		'''note that we give our param file the following format:
		rcparamstr parameter stringvalue
		rcparamint parameter intvalue
		rcparamfl parameter floatvalue
		depending on whether they are ints or not'''


		if data[0]=='rcparamstr':plt.rcParams[data[1]] = data[2]
		if data[0]=='rcparamint': plt.rcParams[data[1]] = int(data[2])
		if data[0]=='rcparamfl': plt.rcParams[data[1]] = float(data[2])
		#print data[0]

	return (0)

'''
example param_file:

rcparamstr text.usetex True
rcparamstr font.family serif
rcparamstr axes.edgecolor black
rcparamfl lines.linewidth 1.2
rcparamfl axes.linewidth 1.5
rcparamint xtick.major.size 8      # major tick size in points
rcparamint ytick.major.size 8     # major tick size in points
rcparamstr axes.edgecolor black
rcparamstr axes.edgecolor black


#imsocool
'''

