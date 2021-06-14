#define single_channel_selector_cxx
// The class definition in single_channel_selector.h has been generated automatically
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
// root> T->Process("single_channel_selector.C")
// root> T->Process("single_channel_selector.C","some options")
// root> T->Process("single_channel_selector.C+")
//

#include "single_channel_selector.h"
#include <TH2.h>
#include <TStyle.h>
#include "TH1F.h"
#include "TTree.h"
#include "TFile.h"
#include "TMath.h"
#include <iostream>
//using std::vector;
//using std::string;
void single_channel_selector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   m_baseline_voltage = -2.5;
   TString option = GetOption();
   TString output_filename = option;

   // // Initialize output file
   m_output_file = TFile::Open(output_filename, "RECREATE");
   // Initialize TTree
   m_tree_event = new TTree("event", "event");
   m_tree_event->Branch("max_voltage", &m_max_voltage, "max_voltage/D");
   m_tree_event->Branch("width", &m_width, "width/I");
   m_tree_event->Branch("charge", &m_charge, "charge/D");
   m_tree_event->Branch("trig_charge", &m_trig_charge, "trig_charge/I");
   m_tree_event->Branch("pass_width", &m_pass_width, "pass_width/I");
   m_tree_event->Branch("trig_level", &m_trig_level, "trig_level/I");
}

void single_channel_selector::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
}

Bool_t single_channel_selector::Process(Long64_t entry)
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
   // Check if size == 0;
   if ((*size) <= 0)
   {
      std::clog << "single_channel_selector::ERROR size of channel == 0; exit!" << std::endl;
      return kFALSE;
   }

   m_max_voltage = GetMinimumValue();
   m_width = GetWidth();
   m_charge = GetCharge();

   m_trig_charge = Pass_trigger_charge();
   m_pass_width = Pass_width();
   m_trig_level = Pass_trigger_level();

   m_tree_event->Fill();

   return kTRUE;
}

void single_channel_selector::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.
}

void single_channel_selector::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

   m_tree_event->Write();
}

Int_t single_channel_selector::Pass_width()
{
   if (m_width <= 10)
   {
      return 0;
   }
   else
   {
      return 1;
   }
}
Int_t single_channel_selector::Pass_trigger_charge()
{

   if (m_charge <= -4400)
   {
      return 0;
   }
   else
   {
      return 1;
   }
}

Int_t single_channel_selector::Pass_trigger_level()
{
   if (m_max_voltage <= -2.68)
   {
      return 0;
   }
   else
   {
      return 1;
   }
}

Double_t single_channel_selector::GetMinimumValue()
{

   Double_t minimum_value;
   minimum_value = voltage[0];
   //for (auto i = 999; i < (*size); i++)
   for (auto i = 899; i < 1200; i++)
   {
      if (voltage[i] < minimum_value)
      {
         minimum_value = voltage[i];
      }
   }

   return minimum_value;
}

Int_t single_channel_selector::GetWidth()
{
   Int_t width = 0;
   Double_t max_amplitude = m_baseline_voltage - m_max_voltage;
   for (auto i = 899; i < 1200; i++)
   {
      if ((m_baseline_voltage - voltage[i]) < (max_amplitude / (1.4142136)))
      {
         width = width + 1;
      }
   }

   return width;
}

Double_t single_channel_selector::GetCharge()
{
   Double_t charge = 0;
   for (auto i = 0; i < (*size); i++)
   {
      charge = charge + voltage[i];
   }

   return charge;
}
