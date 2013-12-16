#import modules
import csv, sys, os, array, warnings, subprocess
import numpy as np
import time

fname=sys.argv[1]

#i=os.system('pdflatex '+fname)
#i=os.system('bibtex '+fname)
#i=os.system('pdflatex '+fname)
i=os.system('latex '+fname)
i=os.system('dvips -o'+fname+'.ps '+fname)
i=os.system('ps2pdf '+fname+'.ps')
i=os.system('rm -f *.aux *.log *.dvi')
i=os.system('open -a preview '+fname+'*.pdf &')

