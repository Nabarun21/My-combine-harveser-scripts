#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;

int main(int argc, char* argv[]){

  printf ("Creating LFV MuTau_e datacards. \n ");

  string folder="lfvauxiliaries/datacards";
  string lumi="goldenJson12p9_fakesmethod2";
  string inputFile="LFV_fakes";
  string outputFile="HMuTau_mutaue_2016_input";
  string dirInput="Nab2016LFV";
  bool  binbybin=true;
  string categories="all";

  if (argc > 1)
    { int count=0;
      for (count = 1; count < argc; count++)
      {
        if(strcmp(argv[count] ,"--i")==0) inputFile=argv[count+1];
        if(strcmp(argv[count] ,"--o")==0) outputFile=argv[count+1];
        if(strcmp(argv[count] ,"--l")==0) lumi=argv[count+1];
        if(strcmp(argv[count] ,"--d")==0) dirInput=argv[count+1];
        if(strcmp(argv[count] ,"--f")==0) folder=argv[count+1];
        if(strcmp(argv[count] ,"--c")==0) categories=argv[count+1];
        if(strcmp(argv[count] ,"--b")==0) binbybin=true;

      }
    }


  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/lfvauxiliaries/shapes/";

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  ch::Categories  cats = {
	{0, "mutaue_gg"},
	{1, "mutaue_boost"},
	{21, "mutaue_2j_gg"},
	{22, "mutaue_2j_vbf"},
      };

      

   if (categories=="all")
     {
       cats = {
   	{0, "mutaue_gg"},
   	{1, "mutaue_boost"},
	{21, "mutaue_2j_gg"},
	{22, "mutaue_2j_vbf"},
       };
     }
   else if (categories=="0")
     {
      cats = {
        {0, "mutaue_gg"},};
     }
   else if (categories=="1")
     {
       cats = {
        {1, "mutaue_boost"},};
     }
   else if (categories=="21")
     {
       cats = {
        {21, "mutaue_2j_gg"},};
     }
   else if (categories=="22")
     {
       cats = {
        {22, "mutaue_2j_vbf"},};
     }


/*
  ch::Categories cats = {
      {-1, "mutau"},
      {0, "mutau_gg"},
      {1, "mutau_boost"},
      {2, "mutau_vbf"},
    };
*/

  // ch::Categories is just a typedef of vector<pair<int, string>>
  //! [part1]


  //! [part2]
  vector<string> masses = ch::MassesFromRange("125");
  // Or equivalently, specify the mass points explicitly:
  //    vector<string> masses = {"120", "125", "130", "135"};
  //! [part2]

  //! [part3]
  cb.AddObservations({"*"}, {"HMuTau"}, {"2016"}, {"mutaue"}, cats);
  //! [part3]

  //! [part4]
  vector<string> bkg_procs = {"DY", "Dibosons", "TT","T","WG","ggHTauTau","vbfHTauTau","FAKES"};
  cb.AddProcesses({"*"}, {"HMuTau"}, {"2016"}, {"mutaue"}, bkg_procs, cats, false);

  vector<string> sig_procs = {"LFVGG", "LFVVBF"};
  cb.AddProcesses(masses, {"HMuTau"}, {"2016"}, {"mutaue"}, sig_procs, cats, true);
  //! [part4]


  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;


  //! [part5]

  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "TT","WG","T","Dibosons","ggHTauTau","vbfHTauTau","FAKES"}}))
      .AddSyst(cb, "CMS_lumi", "lnN", SystMap<>::init(1.062));

//  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "WG", "TT","Dibosons","ggHTauTau","vbfHTauTau"}}))
//      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
//      ({"2015"}, 1.12));
  //! [part5]

  //! [part6]

  cb.cp().process({"LFVGG","ggHTauTau"})
      .AddSyst(cb, "pdf_gg", "lnN", SystMap<>::init(1.1));
  cb.cp().process({"LFVVBF","vbfHTauTau"})
      .AddSyst(cb, "pdf_vbf", "lnN", SystMap<>::init(1.1));

  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "WG", "TT","T","Dibosons","ggHTauTau","vbfHTauTau"}}))
      .AddSyst(cb, "CMS_eff_m", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "WG", "TT","T","Dibosons","ggHTauTau","vbfHTauTau"}}))
      .AddSyst(cb, "CMS_eff_e", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "WG", "TT","T","Dibosons","ggHTauTau","vbfHTauTau"}}))
      .AddSyst(cb, "CMS_eff_btag", "lnN", SystMap<>::init(1.03));

  //  cb.cp().process({"WJETSMC"})
  //  .AddSyst(cb, "norm_wjets", "lnN", SystMap<>::init(1.1));

  cb.cp().process({"FAKES"})
      .AddSyst(cb, "norm_fakes", "lnN", SystMap<>::init(1.4));

  //  cb.cp().process({"Fakes"})
  //  .AddSyst(cb,
  //    "norm_taufakes_mutauhad_uncor_$BIN", "lnN", SystMap<>::init(1.1));

  cb.cp().process({"DY"})
      .AddSyst(cb, "norm_dy", "lnN", SystMap<>::init(1.10));

  // cb.cp().process({"DY"})
  //     .AddSyst(cb,
  //       "norm_dy_$BIN", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"WG"})
      .AddSyst(cb, "norm_wg", "lnN", SystMap<>::init(1.1));

  cb.cp().process({"WG"})
      .AddSyst(cb,
        "norm_wg_$BIN", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"Dibosons"})
      .AddSyst(cb, "norm_WW ", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"TT"})
      .AddSyst(cb, "norm_tt ", "lnN", SystMap<>::init(1.06));

  cb.cp().process({"T"})
      .AddSyst(cb, "norm_t ", "lnN", SystMap<>::init(1.05));

  // cb.cp().process({"Dibosons"})
  //   .AddSyst(cb,
  //       "norm_WW_$BIN", "lnN", SystMap<>::init(1.05));

  // cb.cp().process({"TT"})
  //   .AddSyst(cb,
  //       "norm_TT_$BIN", "lnN", SystMap<>::init(1.05));

  //  cb.cp().process({"T"})
  //  .AddSyst(cb,
  //    "norm_T_$BIN", "lnN", SystMap<>::init(1.05));


  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "WG", "TT","T","Dibosons","ggHTauTau","vbfHTauTau","FAKES"}}))
      .AddSyst(cb, "CMS_MET_Jes","shape",SystMap<>::init(1.));

  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "WG", "TT","T","Dibosons","ggHTauTau","vbfHTauTau","FAKES"}}))
      .AddSyst(cb, "CMS_MET_Ues","shape",SystMap<>::init(1.));

  //  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "WG", "TT","T","Dibosons","ggHTauTau","vbfHTauTau","WJETSMC"}}))
  //    .AddSyst(cb, "CMS_MET_Tes","shape",SystMap<>::init(1.));

  //cb.cp().process(ch::JoinStr({{"Fakes"}}))
  //  .AddSyst(cb, "FakeShapeMuTau","shape",SystMap<>::init(1.));


/*
  double DYJES[3]   ={1.016,1.041,1.252};
  double WGJES[3]   ={1.006,1.012,1.516};
  double TTJES[3]        ={1.115,1.091,1.045};
  double DibosonsJES[3]   ={1.076,1.191,1.0};
  double ggHTauTauJES[3] ={1.017,1.009,1.042};
  double vbfHTauTauJES[3]={1.129,1.035,1.023};
  double LFVGGJES[3]     ={1.019,1.023,1.071};
  double LFVVBFJES[3]    ={1.129,1.035,1.055};

  cb.cp().AddSyst(cb, "CMS_JES","lnN",SystMap<process,bin_id>::init 
            ({"DY"},{0},DYJES[0]) ({"DY"},{1},DYJES[1]) ({"DY"},{2},DYJES[2]) 
            ({"WG"},{0},WGJES[0]) ({"WG"},{1},WGJES[1]) ({"WG"},{2},WGJES[2]) 
            ({"TT"},{0},TTJES[0]) ({"TT"},{1},TTJES[1]) ({"TT"},{2},TTJES[2])
            ({"Dibosons"},{0},DibosonsJES[0]) ({"Dibosons"},{1},DibosonsJES[1]) ({"Dibosons"},{2},DibosonsJES[2])
            ({"ggHTauTau"},{0},ggHTauTauJES[0]) ({"ggHTauTau"},{1},ggHTauTauJES[1]) ({"ggHTauTau"},{2},ggHTauTauJES[2])
            ({"vbfHTauTau"},{0},vbfHTauTauJES[0]) ({"vbfHTauTau"},{1},vbfHTauTauJES[1]) ({"vbfHTauTau"},{2},vbfHTauTauJES[2])
            ({"LFVGG"},{0},LFVGGJES[0]) ({"LFVGG"},{1},LFVGGJES[1]) ({"LFVGG"},{2},LFVGGJES[2])
            ({"LFVVBF"},{0},LFVVBFJES[0]) ({"LFVVBF"},{1},LFVVBFJES[1]) ({"LFVVBF"},{2},LFVVBFJES[2])
  );


  double DYTES[3]   ={1.049,1.021,1.209};
  double WGTES[3]   ={1.008,1.045,2.042};
  double TTTES[3]        ={1.300,1.312,1.307};
  double DibosonsTES[3]   ={1.038,1.049,1.0};
  double ggHTauTauTES[3] ={1.766,1.712,1.681};
  double vbfHTauTauTES[3]={1.130,1.220,1.220};
  double LFVGGTES[3]     ={1.009,1.031,1.080};
  double LFVVBFTES[3]    ={1.006,1.033,1.049};

  cb.cp().AddSyst(cb, "CMS_TES","lnN",SystMap<process,bin_id>::init 
            ({"DY"},{0},DYTES[0]) ({"DY"},{1},DYTES[1]) ({"DY"},{2},DYTES[2]) 
            ({"WG"},{0},WGTES[0]) ({"WG"},{1},WGTES[1]) ({"WG"},{2},WGTES[2]) 
            ({"TT"},{0},TTTES[0]) ({"TT"},{1},TTTES[1]) ({"TT"},{2},TTTES[2])
            ({"Dibosons"},{0},DibosonsTES[0]) ({"Dibosons"},{1},DibosonsTES[1]) ({"Dibosons"},{2},DibosonsTES[2])
            ({"ggHTauTau"},{0},ggHTauTauTES[0]) ({"ggHTauTau"},{1},ggHTauTauTES[1]) ({"ggHTauTau"},{2},ggHTauTauTES[2])
            ({"vbfHTauTau"},{0},vbfHTauTauTES[0]) ({"vbfHTauTau"},{1},vbfHTauTauTES[1]) ({"vbfHTauTau"},{2},vbfHTauTauTES[2])
            ({"LFVGG"},{0},LFVGGTES[0]) ({"LFVGG"},{1},LFVGGTES[1]) ({"LFVGG"},{2},LFVGGTES[2])
            ({"LFVVBF"},{0},LFVVBFTES[0]) ({"LFVVBF"},{1},LFVVBFTES[1]) ({"LFVVBF"},{2},LFVVBFTES[2])
  );
*/

  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + dirInput+"/"+inputFile+".root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
//      aux_shapes + "Maria2015Data/LFV_2p11fb_mutauhad_1Dic.root",
      aux_shapes + dirInput+"/"+inputFile+".root",
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");



  //! [part8]
 if(binbybin){
 auto bbb = ch::BinByBinFactory()
   .SetAddThreshold(0.1)
   .SetMergeThreshold(0.5)
   .SetFixNorm(false);
//  bbb.MergeBinErrors(cb.cp().backgrounds());
 bbb.MergeBinErrors(cb.cp().process({"Dibosons","DY","WG","T","TT","ggHTauTau","vbfHTauTau","FAKES"}));
  bbb.AddBinByBin(cb.cp().backgrounds(), cb);
  }

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  boost::filesystem::create_directories(folder);
  boost::filesystem::create_directories(folder + "/"+lumi);


  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
//  TFile output("HMuTau_mutauhad_2015.input.root", "RECREATE");

    string textbinbybin="";
    if(binbybin) textbinbybin="_bbb";

    TFile output((folder + "/"+lumi+"/"+outputFile+"_"+lumi+textbinbybin+".root").c_str(), "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(folder + "/"+lumi+"/"+
          b +outputFile+textbinbybin+"_m" + m + "_"+lumi+".txt", output);
      
    }
  }
  if (categories=="all")
    {
      cb.cp().mass({"125", "*"}).bin({"HMuTau_mutaue_0_2016","HMuTau_mutaue_1_2016","HMuTau_mutaue_21_2016","HMuTau_mutaue_22_2016"}).WriteDatacard(folder + "/"+lumi+"/"+"HMuTau_mutaue_combined_2016"+textbinbybin+"_m125_"+lumi+".txt", output);
    }

  //! [part9]

}
