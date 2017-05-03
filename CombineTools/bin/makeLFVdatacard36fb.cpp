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
  string lumi="goldenJson12p9_20fb";
  string inputFile="LFV_20fb";
  string outputFile="HMuTau_mutaue_2016_input";
  string dirInput="Nab2016LFV";
  bool  binbybin=true;
  string categories="all";
  string analyzer="";

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
        if(strcmp(argv[count] ,"--a")==0) analyzer=argv[count+1];
        if(strcmp(argv[count] ,"--b")==0) binbybin=false;

      }
    }

  cout<<"binbybin "<<binbybin<<endl;

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
	{1, "mutaue_0jet"},
	{2, "mutaue_1jet"},
	{3, "mutaue_2jet_gg"},
	{4, "mutaue_2jet_vbf"},
      };

      

   if (categories=="all")
     {
       cats = {
   	{1, "mutaue_0jet"},
   	{2, "mutaue_1jet"},
	{3, "mutaue_2jet_gg"},
	{4, "mutaue_2jet_vbf"},
       };
     }
   else if (categories=="0")
     {
      cats = {
        {1, "mutaue_0jet"},};
     }
   else if (categories=="1")
     {
       cats = {
        {2, "mutaue_1jet"},};
     }
   else if (categories=="21")
     {
       cats = {
        {3, "mutaue_2jet_gg"},};
     }
   else if (categories=="22")
     {
       cats = {
        {4, "mutaue_2jet_vbf"},};
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
  vector<string> bkg_procs = {"ZTauTau","Zothers", "Diboson", "TT","T","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W","QCD"};
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

  std::cout<<"MAKING DATA CARDS FOR SEMIDATA DRIVEN. Using Input file "<<inputFile<<endl;
  //! [part5]

  //lumi uncertainty
  cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W"}}))
      .AddSyst(cb, "CMS_lumi_13TeV", "lnN", SystMap<>::init(1.026));

//  cb.cp().process(ch::JoinStr({sig_procs, {"DY", "TT","Diboson","ggH_htt","qqH_htt"}}))
//      .AddSyst(cb, "lumi_$ERA", "lnN", SystMap<era>::init
//      ({"2015"}, 1.12));
  //! [part5]

  //! [part6]


  //theory uncertainty
  cb.cp().process({"LFVGG","ggH_htt","ggH_hww"})
    .AddSyst(cb,"QCDScale_ggH", "lnN", SystMap<>::init(1.039));

  cb.cp().process({"LFVVBF","qqH_htt","qqH_hww"})
    .AddSyst(cb,"QCDScale_qqH", "lnN", SystMap<>::init(1.004));

  cb.cp().process({"LFVGG","ggH_htt","ggH_hww"})
    .AddSyst(cb,"pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));

  cb.cp().process({"LFVVBF","qqH_htt","qqH_hww"})
    .AddSyst(cb,"pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));


  cb.cp().AddSyst(cb,"acceptance_scale_gg","lnN",SystMap<process,bin_id>::init
		  ({"LFVGG","ggH_htt"},{1},1.02)
		  ({"LFVGG","ggH_htt"},{2},0.996)
		  ({"LFVGG","ggH_htt"},{3},0.97)
		  ({"LFVGG","ggH_htt"},{4},0.97)
		  ({"ggH_hww"},{1},1.01)
		  ({"ggH_hww"},{2},0.996)
		  ({"ggH_hww"},{3},0.97)
		  ({"ggH_hww"},{4},0.97)
		  );

  cb.cp().AddSyst(cb,"acceptance_pdf_gg","lnN",SystMap<process,bin_id>::init
		  ({"LFVGG","ggH_htt"},{1},1.005)
		  ({"LFVGG","ggH_htt"},{2},1.005)
		  ({"LFVGG","ggH_htt"},{3},0.995)
		  ({"LFVGG","ggH_htt"},{4},0.995)
		  ({"ggH_hww"},{1},1.005)
		  ({"ggH_hww"},{2},0.998)
		  ({"ggH_hww"},{3},0.985)
		  ({"ggH_hww"},{4},0.985)
		  );


  cb.cp().AddSyst(cb,"acceptance_scale_vbf","lnN",SystMap<process,bin_id>::init
		  ({"LFVVBF","qqH_htt"},{1},1.01)
		  ({"LFVVBF","qqH_htt"},{2},1.006)
		  ({"LFVVBF","qqH_htt"},{3},0.999)
		  ({"LFVVBF","qqH_htt"},{4},0.999)
		  ({"qqH_hww"},{1},1.01)
		  ({"qqH_hww"},{2},1.003)
		  ({"qqH_hww"},{3},0.997)
		  ({"qqH_hww"},{4},0.997)
		  );

  cb.cp().AddSyst(cb,"acceptance_pdf_vbf","lnN",SystMap<process,bin_id>::init
		  ({"LFVVBF","qqH_htt"},{1},1.005)
		  ({"LFVVBF","qqH_htt"},{2},0.99)
		  ({"LFVVBF","qqH_htt"},{3},0.985)
		  ({"LFVVBF","qqH_htt"},{4},0.985)
		  ({"qqH_hww"},{1},1.01)
		  ({"qqH_hww"},{2},1.005)
		  ({"qqH_hww"},{3},0.998)
		  ({"qqH_hww"},{4},0.998)
		  );
 //    Uncertainty on BR for HTT @ 125 GeV
 cb.cp().process({"ggH_htt","qqH_htt"}).AddSyst(cb,"BR_htt_THU", "lnN", SystMap<>::init(1.017));
 cb.cp().process({"ggH_htt","qqH_htt"}).AddSyst(cb,"BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
 cb.cp().process({"ggH_htt","qqH_htt"}).AddSyst(cb,"BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));


 //    Uncertainty on BR of HWW @ 125 GeV
 cb.cp().process({"ggH_hww","qqH_hww"}).AddSyst(cb,"BR_hww_THU", "lnN", SystMap<>::init(1.0099));
 cb.cp().process({"ggH_hww","qqH_hww"}).AddSyst(cb,"BR_hww_PU_mq", "lnN", SystMap<>::init(1.0099));
 cb.cp().process({"ggH_hww","qqH_hww"}).AddSyst(cb,"BR_hww_PU_alphas", "lnN", SystMap<>::init(1.0066));





  // //muon-electron efficiencies
  cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W"}}))
      .AddSyst(cb, "CMS_eff_m_13TeV", "lnN", SystMap<>::init(1.02));

  cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W"}}))
      .AddSyst(cb, "CMS_eff_e_13TeV", "lnN", SystMap<>::init(1.02));


  //btag efficiencies
  // cb.cp().process({"Diboson"}).bin_id({0})
  //     .AddSyst(cb, "CMS_eff_btag_diboson_mutaue_gg", "lnN", SystMap<>::init(1.002));

  // cb.cp().process({"Diboson"}).bin_id({1})
  //     .AddSyst(cb, "CMS_eff_btag_diboson_mutaue_boost", "lnN", SystMap<>::init(1.014));

  // cb.cp().process({"Diboson"}).bin_id({21})
  //     .AddSyst(cb, "CMS_eff_btag_diboson_mutaue_2j_gg", "lnN", SystMap<>::init(1.023));

  // cb.cp().process({"Diboson"}).bin_id({22})
  //     .AddSyst(cb, "CMS_eff_btag_diboson_mutaue_2j_vbf", "lnN", SystMap<>::init(1.022));



  // cb.cp().process({"TT","T"}).bin_id({1})
  //     .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.022));

  // cb.cp().process({"TT","T"}).bin_id({2})
  //     .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.048));

  // cb.cp().process({"TT","T"}).bin_id({3})
  //     .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.065));

  // cb.cp().process({"TT","T"}).bin_id({4})
  //     .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.051));


  cb.cp().process({"TT"}).bin_id({2})
      .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.026));

  cb.cp().process({"TT"}).bin_id({3})
      .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.045));

  cb.cp().process({"TT"}).bin_id({4})
      .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.02));


  cb.cp().process({"T"}).bin_id({2})
      .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.025));

  cb.cp().process({"T"}).bin_id({3})
      .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.032));

  cb.cp().process({"T"}).bin_id({4})
      .AddSyst(cb, "CMS_eff_btag_13TeV", "lnN", SystMap<>::init(1.021));





  //norm uncertainties correlated

  cb.cp().process({"W"})
      .AddSyst(cb, "norm_w", "lnN", SystMap<>::init(1.1));

  cb.cp().process({"QCD"})
      .AddSyst(cb, "norm_qcd", "lnN", SystMap<>::init(1.30));

  //  cb.cp().process({"Fakes"})
  //  .AddSyst(cb,
  //    "norm_taufakes_mutauhad_uncor_$BIN", "lnN", SystMap<>::init(1.1));

  cb.cp().process({"ZTauTau"})
      .AddSyst(cb, "norm_ztt", "lnN", SystMap<>::init(1.10));


  cb.cp().process({"Zothers"})
      .AddSyst(cb, "norm_Zothers_mue", "lnN", SystMap<>::init(1.10));

  cb.cp().process({"Diboson"})
      .AddSyst(cb, "norm_Diboson ", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"TT"})
      .AddSyst(cb, "norm_TT ", "lnN", SystMap<>::init(1.10));

  cb.cp().process({"T"})
      .AddSyst(cb, "norm_T ", "lnN", SystMap<>::init(1.05));

  //normalizion uncertainties uncorrelated

  cb.cp().process({"ZTauTau"})
       .AddSyst(cb,
         "norm_ztt_$BIN", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"Zothers"})
       .AddSyst(cb,
         "norm_Zothers_$BIN", "lnN", SystMap<>::init(1.05));
  cb.cp().process({"W"})
      .AddSyst(cb,
        "norm_w_$BIN", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"Diboson"})
    .AddSyst(cb,"norm_Diboson_$BIN", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"TT"})
    .AddSyst(cb,"norm_TT_$BIN", "lnN", SystMap<>::init(1.05));

  cb.cp().process({"T"})
    .AddSyst(cb,
	     "norm_T_$BIN", "lnN", SystMap<>::init(1.05));


  // cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W"}}))
  //     .AddSyst(cb, "CMS_MET_Jes","shape",SystMap<>::init(1.));

  // TString UesNamesZtt[4]={"CMS_MET_chargedZTTgroupUes","CMS_MET_ecalZTTgroupUes","CMS_MET_hcalZTTgroupUes","CMS_MET_hfZTTgroupUes"};

  TString UesNames[4]={"CMS_MET_chargedUes_13TeV","CMS_MET_ecalUes_13TeV","CMS_MET_hcalUes_13TeV","CMS_MET_hfUes_13TeV"};


  for (int i=0; i<4;i++){
    cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers","ggH_htt","qqH_htt","ggH_hww","qqH_hww", "TT","T","Diboson","W","QCD"}}))
      .AddSyst(cb, UesNames[i].Data(), "shape", SystMap<>::init(1.00));
  }

  // for (int i=0; i<4;i++){
  //   cb.cp().process({"WG", "TT","T","Diboson","W"})
  //     .AddSyst(cb, UesNamesOthers[i].Data(), "shape", SystMap<>::init(1.00));
  // }


  // cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers","ggH_htt","qqH_htt"}}))
  //     .AddSyst(cb, "CMS_MET_UesZttgroup","shape",SystMap<>::init(1.));

  // cb.cp().process({"WG", "TT","T","Diboson","W"})
  //     .AddSyst(cb, "CMS_MET_UesOthers","shape",SystMap<>::init(1.));

  cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W","QCD"}}))
     .AddSyst(cb, "CMS_EES_13TeV","shape",SystMap<>::init(1.));

  // cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W","QCD"}}))
  //     .AddSyst(cb, "CMS_Eresrho","shape",SystMap<>::init(1.));
  // cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W","QCD"}}))
  //     .AddSyst(cb, "CMS_Eresphi","shape",SystMap<>::init(1.));


  cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W","QCD"}}))
      .AddSyst(cb, "CMS_MES_13TeV","shape",SystMap<>::init(1.));

  cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W","QCD"}}))
     .AddSyst(cb, "CMS_Pileup_13TeV","shape",SystMap<>::init(1.));


  TString JESNAMES[27]={"CMS_Jes_JetAbsoluteFlavMap_13TeV","CMS_Jes_JetAbsoluteMPFBias_13TeV","CMS_Jes_JetAbsoluteScale_13TeV", "CMS_Jes_JetAbsoluteStat_13TeV","CMS_Jes_JetFlavorQCD_13TeV", "CMS_Jes_JetFragmentation_13TeV", "CMS_Jes_JetPileUpDataMC_13TeV", "CMS_Jes_JetPileUpPtBB_13TeV", "CMS_Jes_JetPileUpPtEC1_13TeV", "CMS_Jes_JetPileUpPtEC2_13TeV","CMS_Jes_JetPileUpPtHF_13TeV","CMS_Jes_JetPileUpPtRef_13TeV","CMS_Jes_JetRelativeBal_13TeV","CMS_Jes_JetRelativeFSR_13TeV","CMS_Jes_JetRelativeJEREC1_13TeV", "CMS_Jes_JetRelativeJEREC2_13TeV","CMS_Jes_JetRelativeJERHF_13TeV","CMS_Jes_JetRelativePtBB_13TeV","CMS_Jes_JetRelativePtEC1_13TeV","CMS_Jes_JetRelativePtEC2_13TeV","CMS_Jes_JetRelativePtHF_13TeV","CMS_Jes_JetRelativeStatEC_13TeV","CMS_Jes_JetRelativeStatFSR_13TeV", "CMS_Jes_JetRelativeStatHF_13TeV","CMS_Jes_JetSinglePionECAL_13TeV", "CMS_Jes_JetSinglePionHCAL_13TeV","CMS_Jes_JetTimePtEta_13TeV"};


  for (int i=0; i<27;i++){
    cb.cp().process(ch::JoinStr({sig_procs, {"ZTauTau","Zothers", "TT","T","Diboson","ggH_htt","qqH_htt","ggH_hww","qqH_hww","W","QCD"}}))
      .AddSyst(cb, JESNAMES[i].Data(), "shape", SystMap<>::init(1.00));
  }

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
            ({"Zothers"},{0},DYJES[0]) ({"Zothers"},{1},DYJES[1]) ({"Zothers"},{2},DYJES[2]) 
            ({"WG"},{0},WGJES[0]) ({"WG"},{1},WGJES[1]) ({"WG"},{2},WGJES[2]) 
            ({"TT"},{0},TTJES[0]) ({"TT"},{1},TTJES[1]) ({"TT"},{2},TTJES[2])
            ({"Diboson"},{0},DibosonsJES[0]) ({"Diboson"},{1},DibosonsJES[1]) ({"Diboson"},{2},DibosonsJES[2])
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
            ({"Zothers"},{0},DYTES[0]) ({"Zothers"},{1},DYTES[1]) ({"Zothers"},{2},DYTES[2]) 
            ({"WG"},{0},WGTES[0]) ({"WG"},{1},WGTES[1]) ({"WG"},{2},WGTES[2]) 
            ({"TT"},{0},TTTES[0]) ({"TT"},{1},TTTES[1]) ({"TT"},{2},TTTES[2])
            ({"Diboson"},{0},DibosonsTES[0]) ({"Diboson"},{1},DibosonsTES[1]) ({"Diboson"},{2},DibosonsTES[2])
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
 bbb.MergeBinErrors(cb.cp().process({"ZTauTau","Diboson","Zothers","W","T","TT","ggH_htt","qqH_htt","ggH_hww","qqH_hww","QCD"}));
  bbb.AddBinByBin(cb.cp().backgrounds(), cb);
  }

  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  boost::filesystem::create_directories(folder);
  boost::filesystem::create_directories(folder + "/"+lumi+analyzer);


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

    TFile output((folder + "/"+lumi+analyzer+"/"+outputFile+"_"+lumi+textbinbybin+".root").c_str(), "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(folder + "/"+lumi+analyzer+"/"+
          b+textbinbybin+"_m" + m + "_"+lumi+".txt", output);
      
    }
  }
  if (categories=="all")
    {
      cb.cp().mass({"125", "*"}).bin({"HMuTau_mutaue_1_2016","HMuTau_mutaue_2_2016","HMuTau_mutaue_3_2016","HMuTau_mutaue_4_2016"}).WriteDatacard(folder + "/"+lumi+analyzer+"/"+"HMuTau_mutaue_combined_2016"+textbinbybin+"_m125_"+lumi+".txt", output);
    }

  //! [part9]

}
