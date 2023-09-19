'''
Combines all single-year templates into Run2 templates
'''
from glob import glob
import subprocess, os
from TwoDAlphabet.helpers import execute_cmd
import ROOT

years = ['16','16APV','17','18']
procs = ['ttbar','WJets','ZJets','TprimeB-1800-125']
jecs = ['JES','JER','JMS','JMR','PNetXbb','PNetTop']
Vars = ['up','down']

# %subs: (jec, var)*5
base_str = 'hadd -f rootfiles/THselection_HT750_{proc}_Run2%s%s.root rootfiles/THselection_HT750_{proc}_16%s%s.root rootfiles/THselection_HT750_{proc}_16APV%s%s.root rootfiles/THselection_HT750_{proc}_17%s%s.root rootfiles/THselection_HT750_{proc}_18%s%s.root'

for proc in procs:
    # hadd nominal first
    nom_str = base_str.format(proc=proc)
    execute_cmd(nom_str%('','','','','','','','','',''),dryrun=False)
    for jec in jecs:
	if (proc != 'TprimeB-1800-125') and ('PNet' in jec): continue
	for var in Vars:
	    execute_cmd(nom_str%('_'+jec,'_'+var,'_'+jec,'_'+var,'_'+jec,'_'+var,'_'+jec,'_'+var,'_'+jec,'_'+var),dryrun=False)
