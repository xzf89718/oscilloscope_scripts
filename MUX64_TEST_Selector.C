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

using std::cout;
using std::endl;
using std::string;

void MUX64_TEST_Selector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   // Plotting style
   gROOT->SetStyle("ATLAS");
   gROOT->ForceStyle();
   gROOT->SetBatch(true);

   output_file = TFile::Open("output.root", "RECREATE");
   goodchannels = new TTree("goodchannels", "goodchannels");
   goodchannels->Branch("max_resistance", &max_resistance);
   goodchannels->Branch("max_voltagein", &max_voltagein);
   goodchannels->Branch("min_resistance", &min_resistance);
   goodchannels->Branch("min_voltagein", &min_voltagein);
   goodchannels->Branch("channel", &channel_to_write, "channel/I");
   goodchannels->Branch("nametag", nametag_to_write, "nametag[20]/C");

   badchannels = new TTree("badchannels", "badchannels");
   badchannels->Branch("max_resistance", &max_resistance);
   badchannels->Branch("max_voltagein", &max_voltagein);
   badchannels->Branch("min_resistance", &min_resistance);
   badchannels->Branch("min_voltagein", &min_voltagein);
   badchannels->Branch("channel", &channel_to_write, "channel/I");
   badchannels->Branch("nametag", nametag_to_write, "nametag[20]/C");
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
   // auto c1 = new TCanvas("c1", "c1", 800, 600);
   vector<double> voltage = dumper.GetDumpedVoltageIn();
   double *graph_voltage = &voltage[0];
   vector<double> resistance = dumper.GetDumpedOnResistance();
   double *graph_resistance = &resistance[0];
   vector<double> resistance_error = dumper.GetDumpedOnResistanceError();
   double *graph_error = &resistance_error[0];
   Char_t *_nametag = &nametag[0];
   strcpy(nametag_to_write, _nametag);
   int max_index = TMath::LocMax(resistance.size(), graph_resistance);
   int min_index = TMath::LocMin(resistance.size(), graph_resistance);
   max_voltagein = voltage.at(max_index);
   min_voltagein = voltage.at(min_index);
   max_resistance = resistance.at(max_index);
   min_resistance = resistance.at(min_index);
   channel_to_write = *channel;

   // auto zeros = new double[resistance_error.size()];
   // for (int i = 0; i < resistance_error.size(); i++)
   // {
   //    zeros[i] = 0.;
   // }
   // TGraphErrors graph1(dumper.GetDumpedVoltageIn().size(), graph_voltage, graph_resistance, zeros, graph_error);
   // graph1.Draw("ALP");
   // c1->Print((string(_nametag) + "_C" + std::to_string(*channel) + ".png").c_str());
   if(true){
   goodchannels->Fill();
   }
   else{
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
   }
   return true;
}