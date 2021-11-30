#define MUX64_TEST_Selector_cxx
// The class definition in MUX64_TEST_Selector.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.

// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("MUX64_TEST_Selector.C")
// root> T->Process("MUX64_TEST_Selector.C","some options")
// root> T->Process("MUX64_TEST_Selector.C+")
//

#include "MUX64_TEST_Selector.h"
#include <TROOT.h>
#include <TH2.h>
#include <TStyle.h>
#include <TMath.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TFile.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TMultiGraph.h>
#include <TStyle.h>
#include <TTree.h>
#include <string>

#include <iostream>
#include <string.h>
#include <iterator>

using std::cout;
using std::endl;
using std::map;
using std::pair;
using std::string;
using std::vector;

void MUX64_TEST_Selector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   if(option == "dochisquare"){
      dochisquare = true;
      usechisquare = false;
   }
   else if (option == "usechisquare"){
      dochisquare = false;
      usechisquare = true;
   }
   else{
      std::cout << "option: dochisquare usechisquare\nAll of them not found. use dochisquare as default" << std::endl;
      dochisquare = true;
      usechisquare = false;
   }
   // Plotting style
   gROOT->SetStyle("ATLAS");
   gROOT->ForceStyle();
   gROOT->SetBatch(true);

   // Hardcoded measured voltage points number
   int n_voltage_points = 24;
   int n_measuretimes = 10;
   m_mapResist = new map<int, vector<double> *>;
   m_mapRelativeError = new map<int, double>;

   output_file = TFile::Open("output.root", "RECREATE");
   goodchannels = new TTree("goodchannels", "goodchannels");
   goodchannels->Branch("max_resistance", &max_resistance);
   goodchannels->Branch("max_voltagein", &max_voltagein);
   goodchannels->Branch("min_resistance", &min_resistance);
   goodchannels->Branch("min_voltagein", &min_voltagein);
   goodchannels->Branch("temperature", &temperature_to_write);
   goodchannels->Branch("channel", &channel_to_write, "channel/I");
   goodchannels->Branch("nametag", nametag_to_write, "nametag[20]/C");
   goodchannels->Branch("max_resistance_error", &max_resistance_error, "max_resistance_error/D");

   badchannels = new TTree("badchannels", "badchannels");
   badchannels->Branch("max_resistance", &max_resistance);
   badchannels->Branch("max_voltagein", &max_voltagein);
   badchannels->Branch("min_resistance", &min_resistance);
   badchannels->Branch("min_voltagein", &min_voltagein);
   badchannels->Branch("temperature", &temperature_to_write);
   badchannels->Branch("channel", &channel_to_write, "channel/I");
   badchannels->Branch("nametag", nametag_to_write, "nametag[20]/C");
   badchannels->Branch("max_resistance_error", &max_resistance_error, "max_resistance_error/D");

   // Init a sets of vecots to store measured resistance at each measure voltage
   for (int i = 0; i < n_voltage_points; i++)
   {
      m_mapResist->insert(pair<int, vector<double> *>(i, new vector<double>(n_measuretimes)));
      goodchannels->Branch((string("resistance_measure") + std::to_string(i)).c_str(), &(m_mapResist->find(i)->second));
      badchannels->Branch((string("resistance_measure") + std::to_string(i)).c_str(), &(m_mapResist->find(i)->second));

      goodchannels->Branch((string("relative_error_measure") + std::to_string(i)).c_str(), &(m_mapRelativeError->find(i)->second));
      badchannels->Branch((string("reltive_error_measure") + std::to_string(i)).c_str(), &(m_mapRelativeError->find(i)->second));
      cout << "Finish init map " << i << endl;
   }
   // hard coded with 24 bins
   if (dochisquare){
      goodMeanResistance = new TH1F("goodMeanResistance", "goodMeanResistance", n_voltage_points, 0., 1.);
      badMeanResistance = new TH1F("badMeanResistance", "badMeanResistance", n_voltage_points, 0., 1.);
   }
   if (usechisquare){
      mean_inputfile = TFile::Open("MUX64_mean.root", "READ");
      goodMeanResistance = (TH1F*)mean_inputfile->Get("goodMeanResistance");
      badMeanResistance = (TH1F*)mean_inputfile->Get("badMeanResistance");
   }
}

void MUX64_TEST_Selector::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).
   TString option = GetOption();
}

Bool_t MUX64_TEST_Selector::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // When processing keyed objects with PROOF, the object is already loaded
   // and is available via the fObject pointer.
   //
   // This function should contain the \"body\" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

   fReader.SetLocalEntry(entry);

   OnstateResistanceDumper dumper(*measuretimes, *load, Voltage_in, Current_in, Voltage_load, Current_power);
   // Dump the on-state resistance
   dumper.Dump();
   // Dump the on-state resistance voltage-by-voltage
   dumper.Dump(*m_mapResist);
   // auto c1 = new TCanvas("c1", "c1", 800, 600);
   vector<double> voltage = dumper.GetDumpedVoltageIn();
   double *graph_voltage = &voltage[0];
   vector<double> resistance = dumper.GetDumpedOnResistance();
   double *graph_resistance = &resistance[0];
   // calculate relateive error
   vector<double> resistance_error = dumper.GetDumpedOnResistanceError();
   vector<double> relative_resistance_error = dumper.GetDumpedOnRelativeError();
   for (int i = 0; i < relative_resistance_error.size(); i++)
   {
      m_mapRelativeError->find(i)->second = relative_resistance_error.at(i);
   }
   double *graph_error = &resistance_error[0];
   double *graph_relative_error = &relative_resistance_error[0];
   Char_t *_nametag = &nametag[0];
   strcpy(nametag_to_write, _nametag);
   int max_index = TMath::LocMax(resistance.size(), graph_resistance);
   int min_index = TMath::LocMin(resistance.size(), graph_resistance);
   max_voltagein = voltage.at(max_index);
   min_voltagein = voltage.at(min_index);
   max_resistance = resistance.at(max_index);
   min_resistance = resistance.at(min_index);
   channel_to_write = *channel;
   temperature_to_write = *temperature;

   int max_index_error = TMath::LocMax(relative_resistance_error.size(), graph_relative_error);
   int min_index_error = TMath::LocMin(relative_resistance_error.size(), graph_relative_error);
   max_resistance_error = relative_resistance_error.at(max_resistance_error);

   if (true)
   {
      goodchannels->Fill();
   }
   else
   {
      badchannels->Fill();
   }

   return kTRUE;
}

void MUX64_TEST_Selector::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.
}

void MUX64_TEST_Selector::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.
   goodchannels->Write();
   badchannels->Write();
   output_file->Write();
   for (auto iter = m_mapResist->begin(); iter != m_mapResist->end(); iter++)
   {
      delete iter->second;
   }
   delete m_mapResist;
   delete m_mapRelativeError;
   delete goodchannels;
   delete badchannels;
   output_file->Close();
}

OnstateResistanceDumper::OnstateResistanceDumper(const int measuretimes, const double load, doubleReader Voltage_in, doubleReader Current_in, doubleReader Voltage_load, doubleReader Current_power) : m_measuretimes(measuretimes), m_load(load), m_Voltage_in(Voltage_in), m_Current_in(Current_in), m_Voltage_load(Voltage_load), m_Current_power(Current_power)
{
   // Do some checks on size of inputs
   if (m_Voltage_in.GetSize() != m_Current_in.GetSize() || m_Voltage_in.GetSize() != m_Voltage_load.GetSize() || m_Voltage_in.GetSize() != m_Voltage_load.GetSize())
   {
      throw "Length of inputs no equal!";
   }
   //Initialize output vectors
   m_dumped_Voltage_in = vector<double>(m_Voltage_in.GetSize() / m_measuretimes);
   m_dumped_On_resistance = vector<double>(m_Voltage_in.GetSize() / m_measuretimes);
   m_dumped_On_resistance_error = vector<double>(m_Voltage_in.GetSize() / m_measuretimes);
   m_dumped_On_resistance_relative_error = vector<double>(m_Voltage_in.GetSize() / m_measuretimes);

   cout << "Finish initialize One OnstateResistanceDumper" << endl;
}

Bool_t OnstateResistanceDumper::Dump()
{
   for (size_t i = 0; i < (m_Voltage_in.GetSize() / m_measuretimes); i++)
   {

      vector<double> vec_resistance(m_measuretimes);
      vector<double> vec_voltage(m_measuretimes);
      for (Int_t j = 0; j < m_measuretimes; j++)
      {
         vec_voltage.at(j) = m_Voltage_in.At(i * m_measuretimes + j);
         vec_resistance.at(j) = (vec_voltage.at(j) - m_Voltage_load.At(i * m_measuretimes + j)) / m_Current_in.At(i * m_measuretimes + j);
      }
      m_dumped_Voltage_in.at(i) = TMath::Mean(vec_voltage.begin(), vec_voltage.end());
      m_dumped_On_resistance.at(i) = TMath::Mean(vec_resistance.begin(), vec_resistance.end());
      m_dumped_On_resistance_error.at(i) = TMath::StdDev(vec_resistance.begin(), vec_resistance.end());
      m_dumped_On_resistance_relative_error.at(i) = TMath::StdDev(vec_resistance.begin(), vec_resistance.end()) / m_dumped_On_resistance.at(i);
   }
   return true;
}

Bool_t OnstateResistanceDumper::Dump(const map<int, vector<double> *> &mapResist)
{
   for (size_t i = 0; i < (m_Voltage_in.GetSize() / m_measuretimes); i++)
   {
      auto iter_Resist = mapResist.find(i);
      vector<double> &vec_todump = *(iter_Resist->second);
      vector<double> vec_resistance(m_measuretimes);
      vector<double> vec_voltage(m_measuretimes);
      if (iter_Resist != mapResist.end())
      {
      }
      else
      {
         throw "vector not found to dump!";
      }
      for (Int_t j = 0; j < m_measuretimes; j++)
      {
         vec_voltage.at(j) = m_Voltage_in.At(i * m_measuretimes + j);
         vec_resistance.at(j) = (vec_voltage.at(j) - m_Voltage_load.At(i * m_measuretimes + j)) / m_Current_in.At(i * m_measuretimes + j);
         vec_todump.at(j) = vec_resistance.at(j);
      }
   }
   return true;
}