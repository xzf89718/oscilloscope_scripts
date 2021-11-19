//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Nov 19 16:32:10 2021 by ROOT version 6.24/06
// from TTree ntuple/ntuple for MUX64 test
// found on file: data_rootformat/B0data.root
//////////////////////////////////////////////////////////

#ifndef MUX64_TEST_Selector_h
#define MUX64_TEST_Selector_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>

// Headers needed by this particular selector
#include <vector>
using std::vector;

typedef TTreeReaderArray<double> &doubleReader;

class OnstateResistanceDumper
{
public:
   // Default Construct Function
   OnstateResistanceDumper(const int measuretimes, const double load, const doubleReader Voltage_in, const doubleReader Current_in, const doubleReader Voltage_load, const doubleReader Current_power);

   Bool_t Dump();
   // GetFunction
   vector<double> GetDumpedVoltageIn() { return m_dumped_Voltage_in; };
   vector<double> GetDumpedOnResistance() { return m_dumped_On_resistance; };
   vector<double> GetDumpedOnResistanceError() { return m_dumped_On_resistance_error; };

private:
   int m_measuretimes;
   double m_load;

   doubleReader m_Voltage_in;
   doubleReader m_Current_in;
   doubleReader m_Voltage_load;
   doubleReader m_Current_power;

   // Save the output
   vector<double> m_dumped_Voltage_in;
   vector<double> m_dumped_On_resistance;
   vector<double> m_dumped_On_resistance_error;
};

class MUX64_TEST_Selector : public TSelector
{
public:
   // My analysis histogram
   TFile* output_file;
   TTree* goodchannels;
   TTree* badchannels;
   double max_resistance;
   double max_voltagein;
   double min_resistance;
   double min_voltagein;
   Char_t nametag_to_write[20];
   Int_t channel_to_write;

   TTreeReader fReader; //!the tree reader
   TTree *fChain = 0;   //!pointer to the analyzed TTree or TChain

   // Readers to access the data (delete the ones you do not need).
   TTreeReaderValue<Int_t> measuretimes = {fReader, "measuretimes"};
   TTreeReaderArray<Char_t> nametag = {fReader, "nametag"};
   TTreeReaderValue<Int_t> channel = {fReader, "channel"};
   TTreeReaderValue<Double_t> temperature = {fReader, "temperature"};
   TTreeReaderValue<Double_t> load = {fReader, "load"};
   TTreeReaderArray<double> Voltage_in = {fReader, "Voltage_in"};
   TTreeReaderArray<double> Current_in = {fReader, "Current_in"};
   TTreeReaderArray<double> Voltage_load = {fReader, "Voltage_load"};
   TTreeReaderArray<double> Current_power = {fReader, "Current_power"};

   MUX64_TEST_Selector(TTree * /*tree*/ = 0) {}
   virtual ~MUX64_TEST_Selector() {}
   virtual Int_t Version() const { return 2; }
   virtual void Begin(TTree *tree);
   virtual void SlaveBegin(TTree *tree);
   virtual void Init(TTree *tree);
   virtual Bool_t Notify();
   virtual Bool_t Process(Long64_t entry);
   virtual Int_t GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
   virtual void SetOption(const char *option) { fOption = option; }
   virtual void SetObject(TObject *obj) { fObject = obj; }
   virtual void SetInputList(TList *input) { fInput = input; }
   virtual TList *GetOutputList() const { return fOutput; }
   virtual void SlaveTerminate();
   virtual void Terminate();

   ClassDef(MUX64_TEST_Selector, 0);
};

#endif

#ifdef MUX64_TEST_Selector_cxx
void MUX64_TEST_Selector::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the reader is initialized.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   fReader.SetTree(tree);
}

Bool_t MUX64_TEST_Selector::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

#endif // #ifdef MUX64_TEST_Selector_cxx
