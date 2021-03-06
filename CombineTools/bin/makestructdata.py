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
lumidict['data_obs']=12900.0

lumidict['Dibosons']=1.0
lumidict['WG']=1.0
lumidict['T']=1.0
lumidict['TT']=1.0
lumidict['WJETSMC']=1.0
lumidict['DY']=1.0
lumidict['ggHTauTau']=1.0
lumidict['vbfHTauTau']=1.0
lumidict['LFVGG125']=1.0
lumidict['LFVVBF125']=1.0

lumidict2['data_obs']=12900.0
lumidict2['Dibosons']=(51464.3410853+15586.5844012+24674.8466258)/3
lumidict2['TT']=11238.5784361
lumidict2['WJETSMC']=18552834.9
lumidict2['DY']=48393999.7
lumidict2['ggHTauTau']=539963.339559
lumidict2['vbfHTauTau']=6321802.00748
lumidict2['LFVGG125']=423834.24408
lumidict2['LFVVBF125']=4045357.52401
lumidict2['WG']=8527
lumidict2['T']=12544







histos=[]
k=0
cat_now=['0','1','2']   #category names in analyzer
syst_names_now=['jetup','jetdown','tup','tdown','uup','udown']      #sysfolder names in analyzer
cat_then=['mutaue_gg','mutaue_boost','mutaue_vbf']

systematics=['JesDown','JesUp','TesUp','UesUp','TesDown','UesDown']

histos={}

for key in cat_then:
   histos[key]=[]

for filename in os.listdir('../../../../../CMSSW_8_0_8/src/UWHiggs/lfvemu/LFVHEMuAnalyzerMVA'):
   file=ROOT.TFile('../../../../../CMSSW_8_0_8/src/UWHiggs/lfvemu/LFVHEMuAnalyzerMVA/'+filename)
   new_title=filename.split('.')[0]
   print new_title
   for i in range(3):
      if cat_now[i]=='':
         hist_path="os/gg/0/h_collmass_pfmet"
      else:
          hist_path="os/gg/"+cat_now[i]+"/selected/nosys/h_collmass_pfmet"
          histo=file.Get(hist_path)
          if (i==3 or i==2 ):
             histo.Rebin(2)
          for j in range(histo.GetNbinsX()+1):
              if histo.GetBinContent(j)<=0:
                  histo.SetBinContent(j,0.001*float((lumidict['data_obs'])/float(lumidict2[new_title])))
                  histo.SetBinError(j,1.8*float((lumidict['data_obs'])/float(lumidict2[new_title])))
          histo.Scale(lumidict['data_obs']/lumidict[new_title])      
          histo.SetTitle(new_title)
          histo.SetName(new_title)
          new_histo=copy.copy(histo)
          histos[cat_then[i]].append(new_histo)
      for k in range(len(syst_names_now)):    
          hist_path="os/gg/"+cat_now[i]+"/selected/"+syst_names_now[k]+"/h_collmass_pfmet"
          new_sys_title=new_title+"_CMS_MET_"+systematics[k]
          histo_sys=file.Get(hist_path)
          if (i==3 or i==2 ):
             histo_sys.Rebin(2)
          for j in range(histo_sys.GetNbinsX()+1):
            if histo_sys.GetBinContent(j)<=0:
               histo_sys.SetBinContent(j,0.001*float((lumidict['data_obs'])/float(lumidict2[new_title])))
               histo_sys.SetBinError(j,1.8*float((lumidict['data_obs'])/float(lumidict2[new_title])))
          histo_sys.Scale(lumidict['data_obs']/lumidict[new_title])
          histo_sys.SetTitle(new_sys_title)
          histo_sys.SetName(new_sys_title)
          new_histo_sys=copy.copy(histo_sys)
          histos[cat_then[i]].append(new_histo_sys)
               

outputfile=ROOT.TFile("../../../lfvauxiliaries/shapes/Nab2016LFV/LFV_12p9.root","recreate")

print outputfile
outputfile.cd()
for key in histos.keys():
   dir0 = outputfile.mkdir(key);
   print dir
   dir0.cd();
   for histo in histos[key]:
      histo.Write()
outputfile.Close()


