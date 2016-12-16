#from lfvmutau plotter
import os
from sys import argv, stdout, stderr
import ROOT
import sys
import copy
ROOT.gROOT.SetStyle("Plain")
#ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetOptStat(0)
lumidict2={}
lumidict={}

lumidict['data_obs']=36100.0

lumidict['Dibosons']=1.0
lumidict['WG']=1.0
lumidict['T']=1.0
lumidict['TT']=1.0
lumidict['WJETSMC']=1.0
lumidict['DY']=1.0
lumidict['ggHTauTau']=1.0
lumidict['vbfHTauTau']=1.0
lumidict['LFVGG125']=float(43.92)/float(44.14)
lumidict['LFVVBF125']=float(3.748)/float(3.82)
lumidict['QCD']=20076.0




lumidict2['data_obs']=36100.0
lumidict2['Dibosons']=5e-05
lumidict2['TT']=8.7e-06
lumidict2['WJETSMC']=1.5e-04
lumidict2['DY']=1.1e-05
lumidict2['ggHTauTau']=2.04e-06
lumidict2['vbfHTauTau']=4.2e-08
lumidict2['LFVGG125']=1.9e-06
lumidict2['LFVVBF125']=4.8e-08
lumidict2['WG']=8e-07
lumidict2['T']=3.5e-06
lumidict2['QCD']=float(1.0)/float(36100)






histos=[]
k=0
cat_now=['0','1','21','22']   #category names in analyzer
syst_names_now=['jetup','jetdown','tup','tdown','uup','udown']      #sysfolder names in analyzer

cat_then=['mutaue_gg','mutaue_boost','mutaue_2j_gg','mutaue_2j_vbf']

systematics=['JesDown','JesUp','TesUp','UesUp','TesDown','UesDown']

histos={}

for key in cat_then:
   histos[key]=[]
for filename in os.listdir('../../../../../CMSSW_8_0_13/src/UWHiggs/lfvemu20fb/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC'):
   if "FAKES" in filename:continue
   file=ROOT.TFile('../../../../../CMSSW_8_0_13/src/UWHiggs/lfvemu20fb/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC/'+filename)
   new_title=filename.split('.')[0]
   print new_title
   for i in range(4):
      if cat_now[i]=='':
         hist_path="os/gg/0/h_collmass_pfmet"
      else:
         hist_path="os/gg/"+cat_now[i]+"/selected/nosys/h_collmass_pfmet"
         histo=file.Get(hist_path)
         if (i==112):
            histo.Rebin(2)
         if (i==2):
            histo.Rebin(2)
         if (i==3):
            histo.Rebin(2)
         histo.Scale(lumidict['data_obs']/lumidict[new_title])      
         for j in range(histo.GetNbinsX()+1):
            if (histo.GetBinContent(j)<0) and "data" not in filename and "LFVs" not in filename:
               print filename
               histo.SetBinContent(j,0.001*float((lumidict['data_obs'])*float(lumidict2[new_title])))
               histo.SetBinError(j,1.8*float((lumidict['data_obs'])*float(lumidict2[new_title])))
            histo.SetTitle(new_title)
            histo.SetName(new_title)
            new_histo=copy.copy(histo)
            histos[cat_then[i]].append(new_histo)
      for k in range(len(syst_names_now)):    
         hist_path="os/gg/"+cat_now[i]+"/selected/"+syst_names_now[k]+"/h_collmass_pfmet"
         new_sys_title=new_title+"_CMS_MET_"+systematics[k]
         histo_sys=file.Get(hist_path)
         if (i==121):
            histo_sys.Rebin(1)
         if (i==2):
            histo_sys.Rebin(2)
         if (i==3):
            histo_sys.Rebin(2)
         histo_sys.Scale(lumidict['data_obs']/lumidict[new_title])
         for j in range(histo_sys.GetNbinsX()+1):
            if (histo_sys.GetBinContent(j)<0) and "data" not in filename and "LFVs" not in filename :
               print filename
               histo_sys.SetBinContent(j,0.001*float((lumidict['data_obs'])*float(lumidict2[new_title])))
               histo_sys.SetBinError(j,1.8*float((lumidict['data_obs'])*float(lumidict2[new_title])))
            histo_sys.SetTitle(new_sys_title)
            histo_sys.SetName(new_sys_title)
            new_histo_sys=copy.copy(histo_sys)
            histos[cat_then[i]].append(new_histo_sys)
	               

outputfile=ROOT.TFile("../../../lfvauxiliaries/shapes/Nab2016LFV/LFV_36fb.root","recreate")

print outputfile
outputfile.cd()
for key in histos.keys():
   dir0 = outputfile.mkdir(key);
   print dir
   dir0.cd();
   for histo in histos[key]:
      histo.Write()
outputfile.Close()


