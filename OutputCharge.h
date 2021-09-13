//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Sun Sep 12 21:29:49 2021 by ROOT version 6.24/00
// from TTree event/event
// found on file: channel2_trig_n3p00_cut_charge_n4400_level_n2p68_CH3.root
//////////////////////////////////////////////////////////

#ifndef OutputCharge_h
#define OutputCharge_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>

// Headers needed by this particular selector

class OutputCharge : public TSelector
{
public:
   TTreeReader fReader; //!the tree reader
   TTree *fChain = 0;   //!pointer to the analyzed TTree or TChain
   TFile *m_output_file;
   TH1F *ahisto;
   // Readers to access the data (delete the ones you do not need).
   TTreeReaderValue<Double_t> max_voltage = {fReader, "max_voltage"};
   TTreeReaderValue<Int_t> width = {fReader, "width"};
   TTreeReaderValue<Double_t> charge = {fReader, "charge"};
   TTreeReaderValue<Int_t> trig_charge = {fReader, "trig_charge"};
   TTreeReaderValue<Int_t> pass_width = {fReader, "pass_width"};
   TTreeReaderValue<Int_t> trig_level = {fReader, "trig_level"};

   OutputCharge(TTree * /*tree*/ = 0) {}
   virtual ~OutputCharge() {}
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

   ClassDef(OutputCharge, 0);
};

#endif

#ifdef OutputCharge_cxx
void OutputCharge::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the reader is initialized.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   fReader.SetTree(tree);
}

Bool_t OutputCharge::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

#endif // #ifdef OutputCharge_cxx
