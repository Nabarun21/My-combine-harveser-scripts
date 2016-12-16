import subprocess
import optimizer

cuts={} 
cuts[0]=optimizer.compute_regions_0jet(100000,100000,100000,1000,-1000000,-100000,100000,100000,-1000)+['selected']
cuts[1]=optimizer.compute_regions_1jet(100000,100000,100000,1000,-1000000,-100000,100000,1000000,-10010)+['selected']
cuts[2]=optimizer.compute_regions_2jet(100000,100000,100000,-1000,-1000000,109000,100000,1000000,100000,-100000)+['selected']




for region in cuts[0]:
   subprocess.call(["LFV","10","--i","mutaue_gg"+region,"--o","gg"+region,"--l","goldenJson12p9","--c","0","--d","Nab2016LFV/optimshapes","--b"])
for region in cuts[1]:
   subprocess.call(["LFV","10","--i","mutaue_boost"+region,"--o","boost"+region,"--l","goldenJson12p9","--c","1","--d","Nab2016LFV/optimshapes","--b"])
for region in cuts[2]:
   subprocess.call(["LFV","10","--i","mutaue_vbf"+region,"--o","vbf"+region,"--l","goldenJson12p9","--c","2","--d","Nab2016LFV/optimshapes","--b"])


