# My-combine-harveser-scripts
Repo to store combine harvester scripts for limit calculation

If we wanna get the limits for analyser names: Analyzer_{analyzer_name} #This needs to obviously have been run and then preprocess.sh run for it

First copy the shapes over:
```
cp -r path_to_lepton_flavor_analysis/MyLeptonFlavorViolationAnalysis/lfv_highmass/preprocessed_inputs/$analyzer_name$luminosity/selection/ ../../../lfvauxiliaries/shapes/your_folder_to_store_shapes/$analyzer_name

```
Make the data cards:

```

makeHighMassDatacard --i h_collmass_pfmet --l 36fb --a $analyzer_name --d $analyzer_name


```

Run the limits:

```
python limitsHighMass.py  36fb $analyzer_name

```

To plot limit_vs_mass

```

cp project_limits_with_bands.py lfvauxiliaries/datacards/36fb$analyzer_name/
cp datacards*lst lfvauxiliaries/datacards/36fb$analyzer_name/				
cd lfvauxiliaries/datacards/36fb$analyzer_name


python project_limits_with_bands.py --filelist datacards.lst  --channel me --masslist 200,300,450,600,750,900 --category combined
python project_limits_with_bands.py --filelist datacards_0jet.lst  --channel me --masslist 200,300,450,600,750,900 --category 0_jet
python project_limits_with_bands.py --filelist datacards_1jet.lst  --channel me --masslist 200,300,450,600,750,900 --category 1_jet

```