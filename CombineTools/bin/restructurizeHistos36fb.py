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

lumidict['data_obs']=35862.0

lumidict['Diboson']=1.0
lumidict['WG']=1.0
lumidict['W']=1.0
lumidict['T']=1.0
lumidict['TT']=1.0
lumidict['WJETSMC']=1.0
lumidict['DY']=1.0
lumidict['Zothers']=1.0
lumidict['ZTauTau']=1.0
lumidict['ggH_htt']=1.0
lumidict['qqH_htt']=1.0
lumidict['ggH_hww']=1.0
lumidict['qqH_hww']=1.0
lumidict['LFVGG120']=1.0
lumidict['LFVVBF120']=1.0
lumidict['LFVGG125']=1.0
lumidict['LFVVBF125']=1.0
lumidict['LFVGG130']=1.0
lumidict['LFVVBF130']=1.0
lumidict['LFVGG150']=1.0
lumidict['LFVVBF150']=1.0
lumidict['QCD']=35862.0


lumidict2['data_obs']=35862.0
lumidict2['Diboson']=1.49334492783e-05
lumidict2['TT']=1.08709111195e-05
lumidict2['WJETSMC']=3e-04
lumidict2['DY']=2.1e-05
lumidict2['Zothers']=2.1e-05
lumidict2['ZTauTau']=2.1e-05
lumidict2['ggH_htt']=2.07e-06
lumidict2['qqH_htt']=4.2e-08
lumidict2['ggH_hww']=2.07e-06
lumidict2['qqH_hww']=4.2e-08
lumidict2['LFVGG125']=1.9e-06
lumidict2['LFVVBF125']=4.8e-08
lumidict2['LFVGG150']=1.9e-06
lumidict2['LFVVBF150']=4.8e-08
lumidict2['LFVGG130']=1.9e-06
lumidict2['LFVVBF130']=4.8e-08
lumidict2['LFVGG120']=1.9e-06
lumidict2['LFVVBF120']=4.8e-08
lumidict2['WG']=1.56725042226e-06
lumidict2['W']=1.56725042226e-06
lumidict2['T']=5.23465826064e-06
lumidict2['QCD']=float(1.0)/float(35862.0)




if sys.argv[3]=='colmass':
   fit_variable='h_collmass_pfmet'
elif sys.argv[3]=='BDT':
   fit_variable='BDT_value'
elif sys.argv[3]=='vismass':
   fit_variable='h_vismass'



print "making data from MC struct"

histos=[]
k=0
cat_now=['0','1','21','22']   #category names in analyzer
syst_names_now=['mesup','mesdown','eesup','eesdown','eresrhoup','eresrhodown','nosys','eresphidown','puup','pudown',
                'chargeduesdown','chargeduesup','ecaluesdown','ecaluesup','hcaluesdown','hcaluesup','hfuesdown','hfuesup',
                'jes_JetAbsoluteFlavMapDown',
                'jes_JetAbsoluteMPFBiasDown',
                'jes_JetAbsoluteScaleDown',
                'jes_JetAbsoluteStatDown',
                'jes_JetFlavorQCDDown',
                'jes_JetFragmentationDown',
                'jes_JetPileUpDataMCDown',
                'jes_JetPileUpPtBBDown',
                'jes_JetPileUpPtEC1Down',
                'jes_JetPileUpPtEC2Down',
                'jes_JetPileUpPtHFDown',
                'jes_JetPileUpPtRefDown',
                'jes_JetRelativeBalDown',
                'jes_JetRelativeFSRDown',
                'jes_JetRelativeJEREC1Down',
                'jes_JetRelativeJEREC2Down',
                'jes_JetRelativeJERHFDown',
                'jes_JetRelativePtBBDown',
                'jes_JetRelativePtEC1Down',
                'jes_JetRelativePtEC2Down',
                'jes_JetRelativePtHFDown',
                'jes_JetRelativeStatECDown',
                'jes_JetRelativeStatFSRDown',
                'jes_JetRelativeStatHFDown',
                'jes_JetSinglePionECALDown',
                'jes_JetSinglePionHCALDown',
                'jes_JetTimePtEtaDown',
                'jes_JetAbsoluteFlavMapUp',
                'jes_JetAbsoluteMPFBiasUp',
                'jes_JetAbsoluteScaleUp',
                'jes_JetAbsoluteStatUp',
                'jes_JetFlavorQCDUp',
                'jes_JetFragmentationUp',
                'jes_JetPileUpDataMCUp',
                'jes_JetPileUpPtBBUp',
                'jes_JetPileUpPtEC1Up',
                'jes_JetPileUpPtEC2Up',
                'jes_JetPileUpPtHFUp',
                'jes_JetPileUpPtRefUp',
                'jes_JetRelativeBalUp',
                'jes_JetRelativeFSRUp',
                'jes_JetRelativeJEREC1Up',
                'jes_JetRelativeJEREC2Up',
                'jes_JetRelativeJERHFUp',
                'jes_JetRelativePtBBUp',
                'jes_JetRelativePtEC1Up',
                'jes_JetRelativePtEC2Up',
                'jes_JetRelativePtHFUp',
                'jes_JetRelativeStatECUp',
                'jes_JetRelativeStatFSRUp',
                'jes_JetRelativeStatHFUp',
                'jes_JetSinglePionECALUp',
                'jes_JetSinglePionHCALUp',
                'jes_JetTimePtEtaUp']      #sysfolder names in analyzer


cat_then=['mutaue_0jet','mutaue_1jet','mutaue_2jet_gg','mutaue_2jet_vbf']

systematics=['CMS_MES_13TeVUp','CMS_MES_13TeVDown','CMS_EES_13TeVUp','CMS_EES_13TeVDown','CMS_Eresrho_13TeVUp','CMS_Eresrho_13TeVDown','CMS_Eresphi_13TeVUp','CMS_Eresphi_13TeVDown','CMS_Pileup_13TeVUp','CMS_Pileup_13TeVDown','CMS_MET_chargedUes_13TeVDown','CMS_MET_chargedUes_13TeVUp','CMS_MET_ecalUes_13TeVDown','CMS_MET_ecalUes_13TeVUp','CMS_MET_hcalUes_13TeVDown','CMS_MET_hcalUes_13TeVUp','CMS_MET_hfUes_13TeVDown','CMS_MET_hfUes_13TeVUp',
             'CMS_Jes_JetAbsoluteFlavMap_13TeVDown',
             'CMS_Jes_JetAbsoluteMPFBias_13TeVDown',
             'CMS_Jes_JetAbsoluteScale_13TeVDown',
             'CMS_Jes_JetAbsoluteStat_13TeVDown',
             'CMS_Jes_JetFlavorQCD_13TeVDown',
             'CMS_Jes_JetFragmentation_13TeVDown',
             'CMS_Jes_JetPileUpDataMC_13TeVDown',
             'CMS_Jes_JetPileUpPtBB_13TeVDown',
             'CMS_Jes_JetPileUpPtEC1_13TeVDown',
             'CMS_Jes_JetPileUpPtEC2_13TeVDown',
             'CMS_Jes_JetPileUpPtHF_13TeVDown',
             'CMS_Jes_JetPileUpPtRef_13TeVDown',
             'CMS_Jes_JetRelativeBal_13TeVDown',
             'CMS_Jes_JetRelativeFSR_13TeVDown',
             'CMS_Jes_JetRelativeJEREC1_13TeVDown',
             'CMS_Jes_JetRelativeJEREC2_13TeVDown',
             'CMS_Jes_JetRelativeJERHF_13TeVDown',
             'CMS_Jes_JetRelativePtBB_13TeVDown',
             'CMS_Jes_JetRelativePtEC1_13TeVDown',
             'CMS_Jes_JetRelativePtEC2_13TeVDown',
             'CMS_Jes_JetRelativePtHF_13TeVDown',
             'CMS_Jes_JetRelativeStatEC_13TeVDown',
             'CMS_Jes_JetRelativeStatFSR_13TeVDown',
             'CMS_Jes_JetRelativeStatHF_13TeVDown',
             'CMS_Jes_JetSinglePionECAL_13TeVDown',
             'CMS_Jes_JetSinglePionHCAL_13TeVDown',
             'CMS_Jes_JetTimePtEta_13TeVDown',
             'CMS_Jes_JetAbsoluteFlavMap_13TeVUp',
             'CMS_Jes_JetAbsoluteMPFBias_13TeVUp',
             'CMS_Jes_JetAbsoluteScale_13TeVUp',
             'CMS_Jes_JetAbsoluteStat_13TeVUp',
             'CMS_Jes_JetFlavorQCD_13TeVUp',
             'CMS_Jes_JetFragmentation_13TeVUp',
             'CMS_Jes_JetPileUpDataMC_13TeVUp',
             'CMS_Jes_JetPileUpPtBB_13TeVUp',
             'CMS_Jes_JetPileUpPtEC1_13TeVUp',
             'CMS_Jes_JetPileUpPtEC2_13TeVUp',
             'CMS_Jes_JetPileUpPtHF_13TeVUp',
             'CMS_Jes_JetPileUpPtRef_13TeVUp',
             'CMS_Jes_JetRelativeBal_13TeVUp',
             'CMS_Jes_JetRelativeFSR_13TeVUp',
             'CMS_Jes_JetRelativeJEREC1_13TeVUp',
             'CMS_Jes_JetRelativeJEREC2_13TeVUp',
             'CMS_Jes_JetRelativeJERHF_13TeVUp',
             'CMS_Jes_JetRelativePtBB_13TeVUp',
             'CMS_Jes_JetRelativePtEC1_13TeVUp',
             'CMS_Jes_JetRelativePtEC2_13TeVUp',
             'CMS_Jes_JetRelativePtHF_13TeVUp',
             'CMS_Jes_JetRelativeStatEC_13TeVUp',
             'CMS_Jes_JetRelativeStatFSR_13TeVUp',
             'CMS_Jes_JetRelativeStatHF_13TeVUp',
             'CMS_Jes_JetSinglePionECAL_13TeVUp',
             'CMS_Jes_JetSinglePionHCAL_13TeVUp',
             'CMS_Jes_JetTimePtEta_13TeVUp']      #sysfolder names in analyzer


histos={}
"""
datafile=ROOT.TFile('../../../../../CMSSW_8_0_25/src/UWHiggs/lfvemu36jes/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC/data_obs.root')


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
"""
binning=array.array( 'd', [-0.6,-0.5,-0.42,-0.34,-0.28,-0.22,-0.18,-0.14,-0.10,-0.06,-0.02,0.02,0.06,0.1,0.14,0.18,0.24,0.30])

binning1jet=array.array( 'd', [-0.6,-0.5,-0.42,-0.34,-0.26,-0.20,-0.16,-0.12,-0.08,-0.04,0.0,0.04,0.08,0.12,0.16,0.22,0.30])


binning2jet=array.array( 'd', [-0.6,-0.5,-0.42,-0.34,-0.28,-0.24,-0.20,-0.16,-0.12,-0.08,-0.04,0.0,0.04,0.08,0.12,0.16,0.20,0.24,0.28,0.30])
#binning2jet=binning
#print len(binning)

for key in cat_then:
   histos[key]=[]
for filename in os.listdir('../../../../../CMSSW_8_0_26_patch1/src/UWHiggs/lfv_postreg/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC'):
   if "FAKES" in filename or "ETau" in filename :continue
   file=ROOT.TFile('../../../../../CMSSW_8_0_26_patch1/src/UWHiggs/lfv_postreg/LFVHEMuAnalyzerMVA'+sys.argv[1]+sys.argv[2]+'fakesfromMC/'+filename)
   new_title=filename.split('.')[0]
   print new_title
   for i in range(4):
      if cat_now[i]=='':
         hist_path="os/gg/0/"+fit_variable
      else:
         hist_path="os/gg/"+cat_now[i]+"/selected/nosys/"+fit_variable
         histo=file.Get(hist_path)
         print histo
        # print histo.GetNbinsX()
         if sys.argv[3]=='BDT' and 'QCD' not in filename:
            if (i==0):
           # print "rebining"
               histo=histo.Rebin(len(binning)-1,"",binning)
            elif (i==1):
               histo=histo.Rebin(len(binning1jet)-1,"",binning1jet)
            else:
               histo=histo.Rebin(len(binning2jet)-1,"",binning2jet)
         elif 'QCD' not in filename:
            if (i==0):
               histo.Rebin(10)
            elif (i==1):
               histo.Rebin(10)
            elif (i==2):
               histo.Rebin(25)
            elif (i==3):
               histo.Rebin(25)
         if 'data' not in filename:
            histo.Scale(lumidict['data_obs']/lumidict[new_title])      
         if 'data' in filename:
            histo.SetBinErrorOption(ROOT.TH1.kPoisson)

#         lowBound=bounds[(cat_now[i],'nosys')][0]
 #        highBound=bounds[(cat_now[i],'nosys')][1]
         lowBound=0
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
            if lowBound==0:continue
            if (histo.GetBinContent(j)<=0) and "data" not in filename:# and "LFV" not in filename:
               histo.SetBinContent(j,0.001*float((lumidict['data_obs'])*float(lumidict2[new_title])))
               histo.SetBinError(j,1.8*float((lumidict['data_obs'])*float(lumidict2[new_title])))
#               print "found neg bin  ",j

#               print "found neg bin"
         histo.SetTitle(new_title)
         histo.SetName(new_title)
         new_histo=copy.copy(histo)
         histos[cat_then[i]].append(new_histo)
      for k in range(len(syst_names_now)):    
         if 'data' in filename:continue
         hist_path="os/gg/"+cat_now[i]+"/selected/"+syst_names_now[k]+"/"+fit_variable
         new_sys_title=new_title+"_"+systematics[k]
         histo_sys=file.Get(hist_path)
         if sys.argv[3]=='BDT' and 'QCD' not in filename:
            if (i==0):
               histo_sys=histo_sys.Rebin(len(binning)-1,"",binning)
            elif (i==1):
               histo_sys=histo_sys.Rebin(len(binning1jet)-1,"",binning1jet)
            else:
               histo_sys=histo_sys.Rebin(len(binning2jet)-1,"",binning2jet)
         elif "QCD" not in filename:
            if (i==0):
               histo_sys.Rebin(10)
            elif (i==1):
               histo_sys.Rebin(10)
            elif (i==2):
               histo_sys.Rebin(25)
            elif (i==3):
               histo_sys.Rebin(25)
         if 'data' not in filename:
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
            if lowBound==0:continue
            if (histo_sys.GetBinContent(j)<=0) and "data" not in filename:# and "LFV" not in filename:
               histo_sys.SetBinContent(j,0.001*float((lumidict['data_obs'])*float(lumidict2[new_title])))
               histo_sys.SetBinError(j,1.8*float((lumidict['data_obs'])*float(lumidict2[new_title])))
         histo_sys.SetTitle(new_sys_title)
         histo_sys.SetName(new_sys_title)
         new_histo_sys=copy.copy(histo_sys)
         histos[cat_then[i]].append(new_histo_sys)
	               

outputfile=ROOT.TFile("../../../lfvauxiliaries/shapes/Nab2016LFV/new_LFV_36fb_"+sys.argv[1]+".root","recreate")

print outputfile
outputfile.cd()
for key in histos.keys():
   dir0 = outputfile.mkdir(key);
  # print dir
   dir0.cd();
#   print key
   for histo in histos[key]:
 #     if "_" not in histo.GetName():
  #       print histo.GetName()
   #      print histo.GetBinContent(15)
    #     print histo.GetBinError(15)
      histo.Write()
outputfile.Close()


