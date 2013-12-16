import csv, sys, os, array, warnings
import matplotlib.pyplot as plt
import numpy as np


code_filename=sys.argv[1]+'.c'

functions=sys.argv[2]

grep_str=os.system('grep '+functions+' '+code_filename)


print grep_str
