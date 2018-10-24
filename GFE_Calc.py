#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:53:16 2018
INPUT : fichier Rover
Output : tableau avec les amorces

@author: glassalle
"""



#output : liste txt des sequences a conserver
#Chrystelle Delord &.G.Lassalle 10 OCTOBRE 2016

import argparse
import os
import csv
import sys
pathCustom = '/home/glassalle/Documents/ESE/Hiplex/Developpement/v3/utils'
# Si le chemin n'est pas configure
if not pathCustom in sys.path:
    sys.path.append(pathCustom)
from Hiplex_Lib import *
from Hiplex_GFELib import *


parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='InputFile', help='Input GFEFile')
parser.add_argument('-o', action='store', dest='outdir', help='output directory')

parser.add_argument('-ind', action='store', dest='individus', help='individu name (optional)')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
results = parser.parse_args()


###############################################################################
# On teste les arguments
###############################################################################    
#argument 1
#on verifie le infile
if results.InputFile:
    if os.path.isfile(results.InputFile):
        nomFile=os.path.basename(results.InputFile)
        BaseFile, BaseExt = os.path.splitext(results.InputFile)
        if BaseExt == ".IN":
            print "fichier input --> ok !"
        else:    
            print "Fichier non conforme. Fin du programme." 
            sys.exit() # On teste le format du fichier via son extension, serait mieux avec PySam.
    else :
        print " Fichier global non trouve Fin du programme."
        sys.exit()     
else :
    print "-i non renseigne => fin du programme"
    sys.exit()
    
###############################################################################
#argument 1
#on verifie le outfile
if results.outdir:
    if os.path.isdir(results.outdir):
        #print "Ok c\'est un fichier ...!!!" 
        nomdir=os.path.basename(results.outdir)
        wpath=os.path.abspath(results.outdir)
    else :
        print " Repertoire de travail invalide."
        sys.exit()     
else :
    print "-o non renseigne => repertoire actif"
    wpath=os.path.abspath('.')
    
###############################################################################
#                           MAIN
###############################################################################


ReadCsvFile=csv.reader(open(results.InputFile,"r"),delimiter='\t')
print "Demarrage lecture du fichier GFE_IN "+str(results.InputFile)        
#outFileIndiv=os.path.join(wpath,individu+".csv")

GFEOut=os.path.join(wpath,"TestGFEOut.csv")
ligne1="locus"+"\t"+"major"+"\t"+"minor"+"\t"+"Freq_major"+"\t"+"Freq_minor"+"\t"+"error"+"\t"+"etheroMaj"+"\t"+"etheroMin"+"\t"+"HomoMaj"+"\t"+"HomoMin"+"\t"+"DA-Max"+"\t"+"nba"+"\t"+"nbc"+"\t"+"nbg"+"\t"+"nbt"    
initOutFile(GFEOut,ligne1)


ligne=0
for refligne in ReadCsvFile: 
    ligne+=1
    if ligne!=1:
        locus=refligne[0]   
        nba=0
        nbc=0
        nbg=0
        nbt=0
        for i in range(3,(len(refligne))):
            quartet=refligne[i]
            quartet=quartet.split('/')
            nba=nba+int(quartet[0])
            nbc=nbc+int(quartet[1])
            nbg=nbg+int(quartet[2])
            nbt=nbt+int(quartet[3])
          
        res=GFE_Locus(nba,nbc,nbt,nbg)
        ligne0=str(locus)+" "+str(res[0])+" "+str(res[1])+" "+str(res[2])+" "+str(res[3])+" "+str(res[4])+" "+str(res[5])+" "+str(res[6])+" "+str(res[7])+" "+str(res[8])+" "+str(res[9])+" "+str(nba)+" "+str(nbc) +" "+str(nbg)+" "+str(nbt)
        print ligne0
        ajoutLigne(GFEOut,ligne0)


