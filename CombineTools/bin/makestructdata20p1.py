#from lfvmutau plotter
import array
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

lumidict['data_obs']=20076.0

lumidict['Dibosons']=1.0
lumidict['WG']=1.0
lumidict['T']=1.0
lumidict['TT']=1.0*float(809.0)/float(831.76)
lumidict['WJETSMC']=1.0
lumidict['DY']=1.0
lumidict['ggHTauTau']=float(43.92)/float(48.58)
lumidict['vbfHTauTau']=float(3.748)/float(3.782)
lumidict['LFVGG125']=float(43.92)/float(48.58)
lumidict['LFVVBF125']=float(3.748)/float(3.782)
lumidict['QCD']=20076.0




lumidict2['data_obs']=20076.0
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
lumidict2['QCD']=float(1.0)/float(20076.0)

if sys.argv[3]=='mass':
   fit_variable='h_collmass_pfmet'
elif sys.argv[3]=='BDT':
   fit_variable='BDT_value'


histos=[]
k=0
cat_now=['0','1','21','22']   #category names in analyzer
syst_names_now=['jetup','jetdown','tup','tdown','uup','udown']      #sysfolder names in analyzer

cat_then=['mutaue_gg','mutaue_boost','mutaue_2j_gg','mutaue_2j_vbf']

systematics=['JesDown','JesUp','TesUp','UesUp','TesDown','UesDown']

histos={}

datafile=ROOT.TFile('../../../../../CMSSW_8_0_13/src/UWHiggs/lfvemu20fb/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC/data_obs.root')
bounds={}
for i in range(4):
   if cat_now[i]=='':
      hist_path="os/gg/0/"+fit_variable
   else:
      hist_path="os/gg/"+cat_now[i]+"/selected/nosys/"+fit_variable
      the_histo=datafile.Get(hist_path)
      data_histo=the_histo.Clone()
#      data_histo.Rebin(4)
#      if (i==2):
#         data_histo.Rebin(2)
#      elif (i==3):
#         data_histo.Rebin(2)
      lowDataBin = 1
      highDataBin = data_histo.GetNbinsX()

      for j in range(1,data_histo.GetNbinsX()+1):
         if (data_histo.GetBinContent(j) > 0):
            lowDataBin = j
            break

      for j in range(data_histo.GetNbinsX(),0,-1):
         if (data_histo.GetBinContent(j) > 0):
            print data_histo.GetBinContent(j),"  ",j
            highDataBin = j
            break
      bounds[(cat_now[i],'nosys')]=(lowDataBin,highDataBin)
      for k in range(len(syst_names_now)):    
         hist_path="os/gg/"+cat_now[i]+"/selected/"+syst_names_now[k]+"/"+fit_variable
         the_histo_sys=datafile.Get(hist_path)
         data_histo_sys=the_histo_sys.Clone()
 #        data_histo_sys.Rebin(4)
 #        if (i==2):
 #           data_histo_sys.Rebin(2)
 #        if (i==3):
 #           data_histo_sys.Rebin(2)
         lowDataBin = 1
         highDataBin = data_histo_sys.GetNbinsX()

         for j in range(1,data_histo_sys.GetNbinsX()+1):
            if (data_histo_sys.GetBinContent(j) > 0):
               lowDataBin = j
               break

         for j in range(data_histo_sys.GetNbinsX(),0,-1):
            if (data_histo_sys.GetBinContent(j) > 0):
               highDataBin = j
               break
         bounds[(cat_now[i],syst_names_now[k])]=(lowDataBin,highDataBin)
      
print bounds


binning=array.array( 'd', [-0.6,-0.5,-0.42,-0.34,-0.28,-0.22,-0.18,-0.14,-0.10,-0.06,-0.02,0.02,0.06,0.1,0.14,0.18,0.24,0.30])

binning1jet=array.array( 'd', [-0.6,-0.5,-0.42,-0.34,-0.26,-0.20,-0.16,-0.12,-0.08,-0.04,0.0,0.04,0.08,0.12,0.16,0.22,0.30])


binning2jet=array.array( 'd', [-0.6,-0.5,-0.42,-0.34,-0.28,-0.24,-0.20,-0.16,-0.12,-0.08,-0.04,0.0,0.04,0.08,0.12,0.16,0.20,0.24,0.28,0.30])

#binning2jet=binning
print len(binning)

for key in cat_then:
   histos[key]=[]
for filename in os.listdir('../../../../../CMSSW_8_0_13/src/UWHiggs/lfvemu20fb/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC'):
   if "FAKES" in filename or "ETau" in filename :continue
   file=ROOT.TFile('../../../../../CMSSW_8_0_13/src/UWHiggs/lfvemu20fb/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC/'+filename)
   new_title=filename.split('.')[0]
   print new_title
   for i in range(4):
      if cat_now[i]=='':
         hist_path="os/gg/0/"+fit_variable
      else:
         hist_path="os/gg/"+cat_now[i]+"/selected/nosys/"+fit_variable
         histo=file.Get(hist_path)
         if sys.argv[3]=='BDT':
            if (i==0):
           # print "rebining"
               histo=histo.Rebin(len(binning)-1,"",binning)
            elif (i==1):
               histo=histo.Rebin(len(binning1jet)-1,"",binning1jet)
            else:
               histo=histo.Rebin(len(binning2jet)-1,"",binning2jet)
         else:
            if (i==1):
               histo.Rebin(1)
            elif (i==2):
                  histo.Rebin(2)
            elif (i==3):
               histo.Rebin(2)
         histo.Scale(lumidict['data_obs']/lumidict[new_title])      
#         lowBound=bounds[(cat_now[i],'nosys')][0]
 #        highBound=bounds[(cat_now[i],'nosys')][1]
         lowBound=1
         highBound=histo.GetNbinsX()
         for bin in range(1,highBound):
            if histo.GetBinContent(bin) != 0:
#               print histo.GetBinContent(bin),bin
               lowBound = bin
               break
         for bin in range(histo.GetNbinsX(),lowBound,-1):
            if histo.GetBinContent(bin) != 0:
               highBound = bin
               break
         for j in range(lowBound, highBound+1):
            if (histo.GetBinContent(j)<=0) and "data" not in filename and "LFV" not in filename:
               histo.SetBinContent(j,0.001*float((lumidict['data_obs'])*float(lumidict2[new_title])))
               histo.SetBinError(j,1.8*float((lumidict['data_obs'])*float(lumidict2[new_title])))
#               print "found neg bin  ",j

#               print "found neg bin"
         histo.SetTitle(new_title)
         histo.SetName(new_title)
         new_histo=copy.copy(histo)
         histos[cat_then[i]].append(new_histo)
      for k in range(len(syst_names_now)):    
         hist_path="os/gg/"+cat_now[i]+"/selected/"+syst_names_now[k]+"/"+fit_variable
         new_sys_title=new_title+"_CMS_MET_"+systematics[k]
         histo_sys=file.Get(hist_path)
         if sys.argv[3]=='BDT':
            if (i==0):
               histo_sys=histo_sys.Rebin(len(binning)-1,"",binning)
            elif (i==1):
               histo_sys=histo_sys.Rebin(len(binning1jet)-1,"",binning1jet)
            else:
               histo_sys=histo_sys.Rebin(len(binning2jet)-1,"",binning2jet)
         else:
            if (i==1):
               histo_sys.Rebin(1)
            elif (i==2):
                  histo_sys.Rebin(2)
            elif (i==3):
               histo_sys.Rebin(2)
        
         histo_sys.Scale(lumidict['data_obs']/lumidict[new_title])

         lowBound=1
         highBound=histo_sys.GetNbinsX()

         
#         lowBound=bounds[(cat_now[i],syst_names_now[k])][0]
 #        highBound=bounds[(cat_now[i],syst_names_now[k])][1]
         for bin in range(1,highBound):
            if histo_sys.GetBinContent(bin) != 0:
               lowBound = bin
               break
         for bin in range(histo_sys.GetNbinsX(),lowBound,-1):
            if histo_sys.GetBinContent(bin) != 0:
               highBound = bin
               break
         
         for j in range(lowBound, highBound+1):
            if (histo_sys.GetBinContent(j)<=0) and "data" not in filename and "LFV" not in filename:
               histo_sys.SetBinContent(j,0.001*float((lumidict['data_obs'])*float(lumidict2[new_title])))
               histo_sys.SetBinError(j,1.8*float((lumidict['data_obs'])*float(lumidict2[new_title])))
         histo_sys.SetTitle(new_sys_title)
         histo_sys.SetName(new_sys_title)
         new_histo_sys=copy.copy(histo_sys)
         histos[cat_then[i]].append(new_histo_sys)
	               

outputfile=ROOT.TFile("../../../lfvauxiliaries/shapes/Nab2016LFV/LFV_20fb_"+sys.argv[1]+".root","recreate")

print outputfile
outputfile.cd()
for key in histos.keys():
   dir0 = outputfile.mkdir(key);
   print dir
   dir0.cd();
   print key
   for histo in histos[key]:
      if "_" not in histo.GetName():
         print histo.GetName()
         print histo.GetBinContent(15)
         print histo.GetBinError(15)
      histo.Write()
outputfile.Close()


