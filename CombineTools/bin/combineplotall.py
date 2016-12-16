import subprocess
import optimizer
import os
import shutil
#import ROOT
from ROOT import *
import ROOT
import math
import numpy as np
import matplotlib.pyplot as pyplot
from array import array
gROOT.ProcessLine(
         "struct limit_t {\
         Double_t         limit_0;\
         }")
gROOT.SetBatch(ROOT.kTRUE)

regions={} 
regions["0"]=optimizer.compute_regions_0jet(100000,100000,100000,1000,-1000000,-100000,100000,100000,-1000)+['selected']
regions["1"]=optimizer.compute_regions_1jet(100000,100000,100000,1000,-1000000,-100000,100000,1000000,-10010)+['selected']
regions["2"]=optimizer.compute_regions_2jet(100000,100000,100000,-1000,-1000000,109000,100000,1000000,100000,-100000)+['selected']



samplelist=(("gg","0"),("boost","1"),("vbf","2"))
cutvarible={
            #     "0":['tPt','mPt','deltaPhi','tMtToPfMet_type1'],
                # "0":['tPt','mPt','DeltaPhi','tmetdeltaPhi','tMtToPfMet_type1'],
                 "0":['scaledePt'],
                 #"0":['deltaPhi','tMtToPfMet_type1'],
                 #"1":['tPt','mPt','tMtToPfMet_type1','DeltaPhi','tmetdeltaPhi'],
                 "1":['scaledePt'],
                 #"2":['tPt','mPt','tMtToPfMet_type1','vbfDeta','vbfMass']
                 "2":['scaledePT']
                # "1":['tMtToPfMet_type1'],
                # "2":['vbfMass','vbfDeta']
               }
def Readtree(filename,limitnumber,counts):
      filein=ROOT.TFile.Open(filename, "READ")
      limitTree=filein.Get("limit")
      #limit=-2.00
      nentries = limitTree.GetEntries();
      limit_s=limit_t()
      limitTree.SetBranchAddress("limit",AddressOf(limit_s,"limit_0"));
      for i in range(0,5):
         limitTree.GetEntry(i);
         limitnumber[i][counts]=limit_s.limit_0
for catogray in range(3):
   fh = open("limitplots/limit_"+samplelist[catogray][1]+".txt","a")
   for cuts in cutvarible[samplelist[catogray][1]]:
   
   
      limit=[[0.0 for x in range(15)] for y in range(6)]
      counts=0 
      for region in regions[samplelist[catogray][1]]:
         if cuts in region: 
            xvariable=region.split(cuts,1)[1]
            Readtree("combineoutput/"+samplelist[catogray][0]+region+".root",limit,counts)
            limit[5][counts]=float(xvariable)
            counts=counts+1
      #limit = np.array(limit)
      #print limit
      c= ROOT.TCanvas("c", "c", 700, 700)
      #mg =ROOT.TMultiGraph()
      leg =ROOT.TLegend(0.5833333,0.7142857,0.9060606,0.9006803)
      Yvariable=array("d",filter(lambda a: a != 0.0, limit[2]))
      Yvariable1l=array("d",filter(lambda a: a != 0.0, limit[1]))
      Yvariable1h=array("d",filter(lambda a: a != 0.0, limit[3]))
      Yvariable2l=array("d",filter(lambda a: a != 0.0, limit[0]))
      Yvariable2h=array("d",filter(lambda a: a != 0.0, limit[4]))
      Xvariable=array("d",filter(lambda a: a != 0.0, limit[5]))
      
      hist0=c.DrawFrame(np.amin(Xvariable)*0.5,0,np.amax(Xvariable)*1.5,np.amax(Yvariable2h)*1.5)
      hist0.GetXaxis().SetTitle(samplelist[catogray][0]+cuts)
      hist0.GetYaxis().SetTitle("95% CL limit on B(h#rightarrow#mu#tau)")
      #print Yvariable1l
      Xvariablezero=array('d',[])
      for i in range(len(Xvariable)):
         Xvariablezero.append(0.0)
      gr =ROOT.TGraph(len(Xvariable),Xvariable,Yvariable)
      #***********1sigma****************
      grshade =ROOT.TGraph(2*len(Xvariable))
      numberpoints=len(Xvariable)
      for i in range(len(Xvariable)):
            grshade.SetPoint(i,Xvariable[i],Yvariable1h[i])
            grshade.SetPoint(numberpoints+i,Xvariable[numberpoints-i-1],Yvariable1l[numberpoints-i-1])
      #****************2sigma********
      grshade2 =ROOT.TGraph(2*len(Xvariable))
      for i in range(len(Xvariable)):
            grshade2.SetPoint(i,Xvariable[i],Yvariable2h[i])
            grshade2.SetPoint(numberpoints+i,Xvariable[numberpoints-i-1],Yvariable2l[numberpoints-i-1])
      grshade.SetFillColor(kGreen)
      grshade2.SetFillColor(kYellow)
      #grshade2.GetXaxis().SetTitle("tpt")
      grshade2.Draw("f")
      gr.SetMarkerStyle(20)
      gr.SetLineWidth(2)
      grshade.Draw("f")
      entry=leg.AddEntry(gr,"Expected","p");
      entry=leg.AddEntry(grshade," 1 std deviation","f")
      entry.SetFillColor(kGreen)
      entry.SetFillStyle(1001)
      entry.SetLineStyle(1);
      entry=leg.AddEntry(grshade2," 2 std deviation","f")
      entry.SetFillColor(kYellow)
      entry.SetFillStyle(1001)
      entry.SetLineStyle(1)
      gr.Draw("pl")
      leg.Draw()
      c.SaveAs("limitplots/"+samplelist[catogray][0]+cuts+".pdf")
      #fh.write("GGtpt\n")
      #fh.write("\n")
      DAT =  np.column_stack((Xvariable,Yvariable))
      name=np.array([samplelist[catogray][0]+cuts])
      np.savetxt(fh,name,delimiter=" ", fmt="%s")
      np.savetxt(fh, DAT, delimiter="      ", fmt="%s") 
   #np.savetxt('limit.txt',(Xvariable,Yvariable),fmt="%f") 
   #np.savetxt('limit.txt',Yvariable,delimiter=',') 
   #fh.write(Xvariable)
   #fh.write(Yvariable)
   #fh.write("******************")
   fh.close()
   
   #gr.GetXaxis().SetTitle("tpt")
   #XvariablezeroVec = ROOT.TVectorD(len(Xvariablezero),Xvariablezero)
   #XvariableVec = ROOT.TVectorD(len(Xvariable),Xvariable)
   #YvariableVec = ROOT.TVectorD(len(Yvariable),Yvariable)
   #Yvariable1lVec = ROOT.TVectorD(len(Yvariable1l),np.subtract(Yvariable,Yvariable1l))
   #Yvariable1hVec = ROOT.TVectorD(len(Yvariable1h),np.subtract(Yvariable1h,Yvariable))
   #systErrorsRatio = ROOT.TGraphAsymmErrors(XvariableVec,YvariableVec,XvariablezeroVec,XvariablezeroVec,Yvariable1lVec,Yvariable1hVec)
   #gr.GetYaxis().SetRangeUser(0,15)
   #systErrorsRatio.SetFillColorAlpha(920+2,0.35)
   #systErrorsRatio.SetMarkerSize(1.5)
   #systErrorsRatio.SetLineColor(kBlue)
   #systErrorsRatio.SetMarkerColor(kBlue+2)
   #systErrorsRatio.SetMarkerStyle(5)
   #systErrorsRatio.SetLineWidth(1)
   #systErrorsRatio.Draw('P,sames')
   print Yvariable 
   print Xvariable 
   #print Yvariable1h 
   #print np.subtract(Yvariable1h,Yvariable) 
   #hist=ROOT.TH2F("tpt","tpt",100,0,100)
   #for region in optimizer.regions["0"]:
   #   stringused="lfvauxiliaries/datacards/2fb/HMuTau_gg"+region+"_mutauhad_0_2016_bbb_m125_2fb.txt"
   #   stringuesd_1='-exp'
   #   subprocess.call(["combine", "-M","Asymptotic","--run","expected","-C","0.95","-t","-1","--minimizerStrategy","0","-n","-exp","-m","125",stringused])
   #   shutil.move("higgsCombine-exp.Asymptotic.mH125.root", "combineoutput/"+"gg"+region+".root")
   #for region in optimizer.regions["1"]:
   #   stringused="lfvauxiliaries/datacards/2fb/HMuTau_boost"+region+"_mutauhad_1_2016_bbb_m125_2fb.txt"
   #   stringuesd_1='-exp'
   #   subprocess.call(["combine", "-M","Asymptotic","--run","expected","-C","0.95","-t","-1","--minimizerStrategy","0","-n","-exp","-m","125",stringused])
   #   shutil.move("higgsCombine-exp.Asymptotic.mH125.root", "combineoutput/"+"boost"+region+".root")
   #for region in optimizer.regions["2"]:
   #   stringused="lfvauxiliaries/datacards/2fb/HMuTau_vbf"+region+"_mutauhad_2_2016_bbb_m125_2fb.txt"
   #   stringuesd_1='-exp'
   #   subprocess.call(["combine", "-M","Asymptotic","--run","expected","-C","0.95","-t","-1","--minimizerStrategy","0","-n","-exp","-m","125",stringused])
   #   shutil.move("higgsCombine-exp.Asymptotic.mH125.root", "combineoutput/"+"vbf"+region+".root")
       
   #for region in optimizer.regions["1"]:
   #   subprocess.call(["LFVSimple","8","--i","boost"+region,"--o","boost"+region,"--l","2fb","--name","boost"+region])
   #for region in optimizer.regions["2"]:
   #   subprocess.call(["LFVSimple","8","--i","vbf"+region,"--o","vbf"+region,"--l","2fb","--name","vbf"+region])
   
   
