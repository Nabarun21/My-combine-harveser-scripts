import subprocess
import os
import sys

lumi="goldenjson_20fb"
if len(sys.argv)>1:
    lumi=sys.argv[1]
analyzer=""
if len(sys.argv)>2:
    analyzer=sys.argv[2]

regions=["combined","0","1","21","22"]

"""

print "PRINTING OUT EXPECTED LIMITS without bbb BY CATEGORY"
print ""
print ""
print ""




for region in regions:
    print "CALCULATING EXPECTED LIMIT FOR "+region+" CATEGORY"
    command="combine -M Asymptotic --run expected -C 0.95  -t -1 --minimizerStrategy 0 -n '-exp' -m 125  lfvauxiliaries/datacards/"+lumi+analyzer+"/HMuTau_mutaue_"+region+"_2016_m125_"+lumi+".txt"
    subprocess.call(command.split())
    print " "




print "PRINTING OUT EXPECTED LIMITS BY CATEGORY"
print ""
print ""
print ""

for region in regions:
    print "CALCULATING EXPECTED LIMIT FOR "+region+" CATEGORY"
    command="combine -M Asymptotic --run expected -C 0.95  -t -1 --minimizerStrategy 0 -n '-exp' -m 125  lfvauxiliaries/datacards/"+lumi+analyzer+"/HMuTau_mutaue_"+region+"_2016_bbb_m125_"+lumi+".txt"
    subprocess.call(command.split())
    print " "
"""


print "PRINTING OUT EXPECTED SIGNIFICANCES BY CATEGORY"
print ""
print ""
print ""

for region in regions:
    print "CALCULATING EXPECTED SIGNIFICANCE FOR "+region+" CATEGORY"
    command="combine -M ProfileLikelihood --significance lfvauxiliaries/datacards/"+lumi+analyzer+"/HMuTau_mutaue_"+region+"_2016_bbb_m125_"+lumi+".txt -t -1 --expectSignal=1  -m 125"

    subprocess.call(command.split())
    print " "

