import subprocess
import optimizer
import os
import shutil
for region in optimizer.regions["0"]:
   stringused="lfvauxiliaries/datacards/15fb_sys_k_4_check/HMuTaugg"+region+"_mutauhad_0_2015_bbb_m125_15fb_sys_k_4_check.txt"
   stringuesd_1='-exp'
   print "HMuTaugg"+region+"_mutauhad_0_2015_bbb_m125_15fb_sys_k_4_check.txt"
   subprocess.call(["combine", "-M","Asymptotic","--run","expected","-C","0.95","-t","-1","--minimizerStrategy","0","-n","-exp","-m","125",stringused])
   shutil.move("higgsCombine-exp.Asymptotic.mH125.root", "combineoutput/"+"gg"+region+".root")
for region in optimizer.regions["1"]:
   stringused="lfvauxiliaries/datacards/15fb_sys_k_4_check/HMuTauboost"+region+"_mutauhad_1_2015_bbb_m125_15fb_sys_k_4_check.txt"
   stringuesd_1='-exp'
   print "HMuTauboost"+region+"_mutauhad_1_2015_bbb_m125_15fb_sys_k_4_check.txt"
   subprocess.call(["combine", "-M","Asymptotic","--run","expected","-C","0.95","-t","-1","--minimizerStrategy","0","-n","-exp","-m","125",stringused])
   shutil.move("higgsCombine-exp.Asymptotic.mH125.root", "combineoutput/"+"boost"+region+".root")
for region in optimizer.regions["2"]:
   stringused="lfvauxiliaries/datacards/15fb_sys_k_4_check/HMuTauvbf"+region+"_mutauhad_2_2015_bbb_m125_15fb_sys_k_4_check.txt"
   stringuesd_1='-exp'
   print "HMuTauvbf"+region+"_mutauhad_2_2015_bbb_m125_15fb_sys_k_4_check.txt"
   subprocess.call(["combine", "-M","Asymptotic","--run","expected","-C","0.95","-t","-1","--minimizerStrategy","0","-n","-exp","-m","125",stringused])
   shutil.move("higgsCombine-exp.Asymptotic.mH125.root", "combineoutput/"+"vbf"+region+".root")
    
for i in range(3):
   stringused="lfvauxiliaries/datacards/15fb_sys_k_4_check/HMuTaudef_mutauhad_"+str(i)+"_2015_bbb_m125_15fb_sys_k_4_check.txt"
   print "HMuTaudef_mutauhad_"+str(i)+"_2015_bbb_m125_15fb_sys_k_4_check.txt"
   subprocess.call(["combine", "-M","Asymptotic","--run","expected","-C","0.95","-t","-1","--minimizerStrategy","0","-n","-exp","-m","125",stringused])
   shutil.move("higgsCombine-exp.Asymptotic.mH125.root", "combineoutput/"+"HMuTaudef"+str(i)+".root")
#for region in optimizer.regions["1"]:
#   subprocess.call(["LFVSimple","8","--i","boost"+region,"--o","boost"+region,"--l","15fb_sys_k_4_check","--name","boost"+region])
#for region in optimizer.regions["2"]:
#   subprocess.call(["LFVSimple","8","--i","vbf"+region,"--o","vbf"+region,"--l","15fb_sys_k_4_check","--name","vbf"+region])



