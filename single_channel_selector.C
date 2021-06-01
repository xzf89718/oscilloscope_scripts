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
#include <iostream>

void single_channel_selector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   auto output_filename=option;
   if(option.size() == 0){
      output_filename="default.root";
   }
   // Initialize output file
   m_output_file = TFile::Open(output_filename.c_str(), "RECREATE");
   // Initialize TTree
   m_tree_max_voltage = new TTree("max_voltage", "max_voltage");
   m_tree_max_voltage->Branch("max_voltage", &m_max_voltage, "max_voltage/D");
   m_tree_charge = new TTree("charge", "charge");
   m_tree_charge->Branch("charge", &m_charge, "charge/D");
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
   m_max_voltage=GetMinimumValue();
   m_charge=GetCharge();
   m_tree_max_voltage->Fill();
   m_tree_charge->Fill();

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

   m_tree_charge->Write();
   m_tree_max_voltage->Write();
}

Double_t single_channel_selector::GetMinimumValue()
{

   Double_t minimum_value;
   minimum_value = voltage[0];
   for (auto i = 0; i < (*size); i++)
   {
      if (voltage[i] < minimum_value)
      {
         minimum_value = voltage[i];
      }
   }

   return minimum_value;
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