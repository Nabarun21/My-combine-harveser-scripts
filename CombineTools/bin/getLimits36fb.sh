#!/bin/bash                                                                                                                                 
                                                                                                                                          
usage='Usage: -a <current analyzer version  name>  -lumi <luminosity in pb> -jobid <jobid, unused option>'

args=`getopt rdlp: -- "$@"`
if test $? != 0
     then
         echo $usage
         exit 1
fi

eval set -- "$args"


for i
 do
    case "$i" in
      -analyzer) shift; analyzer=$2;shift;;
      -lumi) shift; luminosity=$2;shift;;
      -jobid) shift;jobid=$2;shift;;
      -analtype) shift;analtype=$2;shift;;
    esac
done



echo "PRODUCING LIMITS USING SEMI-DATA DRIVEN METHOD"
echo ""
echo ""
echo ""
echo "PRODUCING LIMITS FOR 36 /fb"
echo ""
echo ""

python restructurizeHistos36fb.py $analyzer $luminosity $analtype #produces root file from analyzer results that is used to make the datacards

makeLFVdatacard36fb --i new_LFV_36fb_$analyzer --l $analtype"_goldenjson_36fb" --a $analyzer  #produces datacards

makeLFVdatacard36fb --i new_LFV_36fb_$analyzer --l $analtype"_goldenjson_36fb" --a $analyzer --b  true #produces datacards without bin_by_bin

python limits.py $analtype"_goldenjson_36fb" $analyzer   #produces limits

echo ""
echo ""
echo ""
echo ""
echo ""


#echo "PRODUCING LIMITS USING FAKERATE METHOD"
#
#
#
#
#
#
#echo ""
#echo ""
#echo ""
#echo "PRODUCING LIMITS FOR 36 /fb"
#echo ""
#echo ""
#
#python makestructdata36fbfakemethod.py $analyzer $luminosity  $analtype
#
#makeLFVdatacard36fbfakemethod --i new_LFV_fakes_36fb_$analyzer --l goldenjson_36fb_fakemethod --a $analyzer
#
#python limits.py goldenjson_36fb_fakemethod $analyzer
#




