#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Transpose la matrice en sortie du HCG de Maruki  
input : Fichier out HCG
        
output : matrice transposee avec reformatage des genotypes AA => A/A
"""

import numpy as np
import argparse
import os
import sys
import csv
pathCustom = '/home/glassalle/Documents/ESE/Hiplex/Developpement/v3/utils'
if not pathCustom in sys.path:
    sys.path.append(pathCustom)
from Hiplex_Lib import *
from Hiplex_SamLib import *



parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='InputFile', help='demultiplexed fastq.gz file, \'ind\' mode || Directory \'pop\' mode (required)')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
results = parser.parse_args()


###############################################################################
#                            On teste les arguments
###############################################################################    
###############################################################################
if results.InputFile:
        if os.path.isfile(results.InputFile):
            nomFile=os.path.basename(results.InputFile)
            BaseFile, BaseExt = os.path.splitext(results.InputFile)
            outFile=str(nomFile.split('.')[0])+"_tranpose.csv" 
            
        else :
            print " -i n'est pas un fichier"
            #sys.exit()     
else :
    print "infile non renseigne => fin du programme"
    sys.exit()
    
###############################################################################

###############################################################################    
newOutfile=open(outFile,"w")
ReadMatrice=csv.reader(open(results.InputFile,"r"),delimiter='\t')
matrice=[]
for ligne in ReadMatrice:
    matrice.append(ligne)
matrice2=np.array(matrice)
matrice3=np.transpose(matrice2)
tabGeno=['AA','AC','AG','AT','CA','CC','CG','CT','GA','GC','GG','GT','TA','TC','TG','TT']
for transLigne in matrice3:
    newLigne=''
    for element in transLigne:
        if element.upper() in tabGeno:
            element=str(element[0])+'/'+str(element[1])
            print element
        newLigne=str(newLigne)+"\t"+str(element)
    newLigne.strip() 
    newLigne=newLigne+'\n'
    newOutfile.write(newLigne)    
newOutfile.close()