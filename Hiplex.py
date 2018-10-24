#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:53:16 2018
@author: glassalle

Analyse globale d'un fichier de genotypage selon Hiplex
input : fichier fasta de reference avec les snps candiadts
        Fichier en sortie de sequenceur demultiplexé
        
output : Fichier pileup par individus
         fichiers csv par individus
         fichiers globale par pop
         fichier de log 
"""


import argparse
import os
import sys
pathCustom = '/home/glassalle/Documents/ESE/Hiplex/Developpement/v3/utils'
if not pathCustom in sys.path:
    sys.path.append(pathCustom)
from Hiplex_Lib import *
from Hiplex_SamLib import *



parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='InputFile', help='demultiplexed fastq.gz file, \'ind\' mode || Directory \'pop\' mode (required)')
parser.add_argument('-f', action='store', dest='fastaFile', help='reference fasta file (required)')
parser.add_argument('-o', action='store', dest='outdir', help='output directory (default :.)')
parser.add_argument('-p', action='store', dest='popNameFile', help='popFile : if no file, pop name=Global')
parser.add_argument('-mode', action='store', dest='mode', help='mode : Values pop/ind Default ind')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
results = parser.parse_args()


###############################################################################
#                            On teste les arguments
###############################################################################    
###############################################################################
if results.mode:
    if results.mode=="pop":
        mode="pop"
        
    elif results.mode=="ind":
        mode="ind"
    else:    
        print "mode inconnu: Fin de programme"
        sys.exit()
else:
    mode="ind"
    
###############################################################################
#argument 1
#on verifie le infile
if mode=="ind":
    if results.InputFile:
        if os.path.isfile(results.InputFile):
            nomFile=os.path.basename(results.InputFile)
            BaseFile, BaseExt = os.path.splitext(results.InputFile)
            individu=nomFile.split('.')[0] 
            if BaseExt == ".gz" or BaseExt == ".gzip" :
                a="gz"
                print "fichier gz --> ok !"
            elif BaseExt == ".fastq":
                a="fastq"
                print "fichier fastq --> ok !"
            else:    
                print "Fichiers non conforme. Fin du programme." 
                sys.exit()
        else :
            print " Fichier fastq non trouve Fin du programme."
            sys.exit()     
    else :
        print "infile non renseigne => fin du programme"
        sys.exit()
elif mode=="pop":
    if results.InputFile:
        if os.path.isdir(results.InputFile):
            nomDir=os.path.basename(results.InputFile)
            inputPath=os.path.abspath(results.InputFile)       
        else :
            print " Repertoire input invalide : Fin du programme."
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
#argument 1
#on verifie le fastafile
if results.fastaFile:
    if os.path.isfile(results.fastaFile):
        nomFastaFile=os.path.basename(results.fastaFile)
        BaseFasta, BaseExt = os.path.splitext(nomFastaFile)
        
        if BaseExt == ".fa" or BaseExt == ".fasta" :
            a="fa"
            print "fichier fasta --> ok !"
            #print "Extension OK"
        else:    
            print "Fichier fasta de reference non conforme. Fin du programme." 
            sys.exit() 
    else :
        print " Fichier fasta non trouve Fin du programme."
        sys.exit()     
else :
    print "reference fasta file non renseigne => fin du programme"
    sys.exit()

###############################################################################    
#argument 1
#on verifie le popFile
if results.popNameFile:
    if os.path.isfile(results.popNameFile):
        popFile=results.popNameFile
        
else :
    print "reference fasta file non renseigne => fin du programme"
    popFile=False

###############################################################################
#   Lancement des processus Samtools + pileup ananlyse en mode ind ou pop
###############################################################################

if mode=="pop":
    fichiers = [f for f in os.listdir(results.InputFile) if os.path.isfile(os.path.join(results.InputFile, f))] 
    print fichiers
    logFile=os.path.join(wpath,"GlobalPop.log")
    ligneLog0="individus"+"\t"+"Reads_Totaux"+"\t"+"Reads_Mappes"+"\t"+"Nbre_locus"
    initOutFile(logFile,ligneLog0)
    for file in fichiers:
        newF=os.path.join(inputPath,file)
        BaseFq, BaseExtfq = os.path.splitext(newF)
        if BaseExtfq == ".gz" or BaseExt == ".gzip" or BaseExtfq == ".fastq":
            nomFile=os.path.basename(newF)
            individu=nomFile.split('.')[0] 
            pupFile=samStage(results.fastaFile,newF,wpath)
            totale=pileupAnalysis(pupFile,wpath)
            lignelog=str(individu)+"\t"+str(countreads(newF))+"\t"+str(totale[1])+"\t"+str(totale[0])
            ajoutLigne(logFile,lignelog)                       
        else:    
            print "Fichiers non conforme."+file 
            #sys.exit() # On teste le format du fichier via son extension, serait mieux avec PySam.
elif mode=="ind":   
    pupFile=samStage(results.fastaFile,results.InputFile,wpath)
    totale=pileupAnalysis(pupFile,wpath)
###############################################################################
#   Lancement des processus GFE in 
###############################################################################

globalFile=os.path.join(wpath,"globalePop.csv")   
GFEMaruki=os.path.join(pathCustom,"./GFE") 
HGCMaruki=os.path.join(pathCustom,"./HGC") 
if popFile:
    GFEInListFile=global2pop(popFile,globalFile,wpath)
    for fichPop in GFEInListFile:
        print fichPop
        GFEInFile=global2gfe(fichPop,wpath)
        GFEOutFile=str(GFEInFile)[:-3]+".out"
        HGCOutFile=str(GFEInFile)[:-3]+"_HGC.out"
        commandeMaruki=str(GFEMaruki)+" -in "+str(GFEInFile)  +" -out "+str(GFEOutFile)  
        commandeMarukiHGC=str(HGCMaruki)+" -in "+str(GFEInFile)  +" -out "+str(HGCOutFile)
        print commandeMaruki
        os.system(commandeMaruki)
        os.system(commandeMarukiHGC)

else: 
    GFEInFile=global2gfe(globalFile,wpath)  
    ###############################################################################
    # Calcul GFE Maruki
    ###############################################################################
    GFEOutFile=str(GFEInFile)[:-3]+".out"
    HGCOutFile=str(GFEInFile)[:-3]+"_HGC.out"
    commandeMaruki=str(GFEMaruki)+" -in "+str(GFEInFile)  +" -out "+str(GFEOutFile) 
    commandeMarukiHGC=str(HGCMaruki)+" -in "+str(GFEInFile)  +" -out "+str(HGCOutFile)
    os.system(commandeMaruki)   
    os.system(commandeMarukiHGC)
    
    