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
#include <TH2.h>
#include <TStyle.h>

#include <iostream>

using std::cout;
using std::endl;

void MUX64_TEST_Selector::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
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
}

OnstateResistanceDumper::OnstateResistanceDumper(const int measuretimes, const double load, doubleReader Voltage_in, doubleReader Current_in, doubleReader Voltage_load, doubleReader Current_power) : m_measuretimes(measuretimes), m_load(load), m_Voltage_in(Voltage_in), m_Current_in(Current_in), m_Voltage_load(Voltage_load), m_Current_in(Current_in), m_Current_power(Current_power)
{
   // Do some checks on size of inputs
   if (m_Voltage_in.GetSize() != m_Current_in.GetSize() || m_Voltage_in.GetSize() != m_Voltage_load.GetSize() || m_Voltage_load.GetSize())
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
   double dumped_voltage, dumped_resistance, dumped_resistance_error = 0;
   for (size_t i = 0; i < (m_Voltage_in.GetSize() / m_measuretimes); i++)
   {  
      m_dumped_Voltage_in.at(i) = m_Voltage_in.At(i);
      for (size_t j = 0; j < m_measuretimes; j++)
      {
         
      }
   }
   return true;
}