#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:53:16 2018
INPUT : fichier Rover
Output : tableau avec les amorces

@author: glassalle
"""
import argparse
import os
import csv
import sys
pathCustom = '/home/glassalle/Documents/ESE/Hiplex/Developpement/v2/utils'
# Si le chemin n'est pas configure
if not pathCustom in sys.path:
    sys.path.append(pathCustom)
from Hiplex_Lib import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='InputFile', help='Global file')
parser.add_argument('-o', action='store', dest='OutFile', help='output directory')

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
        if BaseExt == ".txt" or BaseExt == ".text" or BaseExt == ".csv":
            a="text"
            print "fichier input --> ok !"
        else:    
            print "Fichier global non conforme. Fin du programme." 
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
if results.OutFile:
    if os.path.isfile(results.OutFile):
        #print "Ok c\'est un fichier ...!!!" 
        nomOutFile=results.OutFile
        wpath=os.path.abspath(results.OutFile)
    else :
        print " Fichier out renseigne."
        sys.exit()     
else :
    print "-o non renseigne => repertoire actif"
    wpath=os.path.abspath('.')
    nomOutFile=os.path.join(wpath,"GlobaleTarget.csv")

###############################################################################
#Analyse du fichier global en sortie du Hiplex_pop
###############################################################################
ReadCsvFile=csv.reader(open(results.InputFile,"r"),delimiter=';')
print "Demarrage lecture du fichier Global"        
lignelue=0
for refligne in ReadCsvFile:  
    lignelue+=1
    ligne=''
    if lignelue>1:
        if len(refligne)>1: #on élimine les lignes vides
            nomLocus=str(refligne[0])  
            posLue=str(refligne[2])
            posLocus=nomLocus.split("|")[1]
            ligne=''
            if int(posLocus)+1==int(posLue):
                for element in refligne:
                    ligne=ligne+str(element)+';'
                ajoutLigne(nomOutFile,ligne)   
    else:
        print refligne        
        for element in refligne:
            ligne=ligne+str(element)+';'
        initOutFile(nomOutFile,ligne)      