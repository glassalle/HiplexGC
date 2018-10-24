#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

@author: glassalle
"""
import argparse
import os
import sys
# Definition du chemin des scripts
pathCustom = '/home/glassalle/Documents/ESE/Hiplex/Developpement/v3/utils'
# Si le chemin n'est pas configure
if not pathCustom in sys.path:
    sys.path.append(pathCustom)
from Hiplex_Lib import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='InputFile', help='Global file')
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
#Analyse du fichier global en sortie du Hiplex_pop
###############################################################################

GFEInFile=global2gfe(results.InputFile,wpath)
GFEMaruki=os.path.join(pathCustom,"./GFE") 
MarukiOut=os.path.join(wpath,"GFEMaruki.out") 
commandeMaruki=str(GFEMaruki)+" -in "+str(GFEInFile)+" -out "+str(MarukiOut) 
print commandeMaruki
os.system(commandeMaruki)
