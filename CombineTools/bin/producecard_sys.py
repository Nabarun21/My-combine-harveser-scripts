import subprocess
import optimizer

cuts={} 
cuts[0]=optimizer.compute_regions_0jet(100000,100000,100000,1000,-1000000,-100000,100000,100000,-1000,1000)+['selected']
cuts[1]=optimizer.compute_regions_1jet(100000,100000,100000,1000,-1000000,-100000,100000,1000000,-10010,1000)+['selected']
cuts[21]=optimizer.compute_regions_2jetgg(100000,100000,100000,-1000,-1000000,109000,100000,1000000,100000,-10000,1000)+['selected']
cuts[22]=optimizer.compute_regions_2jetvbf(100000,100000,100000,-1000,-1000000,109000,100000,1000000,100000,-10000,1000)+['selected']

print cuts



"""
for region in cuts[0]:
   subprocess.call(["LFVoptim","10","--i","mutaue_gg"+region,"--o","gg"+region,"--l","goldenJson12p9_new","--c","0","--d","Nab2016LFV/optimshapes2"])
for region in cuts[1]:
   subprocess.call(["LFVoptim","10","--i","mutaue_boost"+region,"--o","boost"+region,"--l","goldenJson12p9_new","--c","1","--d","Nab2016LFV/optimshapes2"])
"""

for region in cuts[21]:
   subprocess.call(["LFVoptim","10","--i","mutaue_2j_gg"+region,"--o","2j_gg"+region,"--l","goldenJson12p9_new","--c","21","--d","Nab2016LFV/optimshapes2"])

for region in cuts[22]:
   subprocess.call(["LFVoptim","10","--i","mutaue_2j_vbf"+region,"--o","2j_vbf"+region,"--l","goldenJson12p9_new","--c","22","--d","Nab2016LFV/optimshapes2"])


