//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Nov 19 16:32:20 2021 by ROOT version 6.24/06
// from TTree ntuple/ntuple for MUX64 test
// found on file: data_rootformat/B0data.root
//////////////////////////////////////////////////////////

#ifndef MUX64_TEST_h
#define MUX64_TEST_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"

class MUX64_TEST {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           measuretimes;
   Char_t          nametag[241];
   Int_t           channel;
   Double_t        temperature;
   Double_t        load;
   vector<double>  *Voltage_in;
   vector<double>  *Current_in;
   vector<double>  *Voltage_load;
   vector<double>  *Current_power;

   // List of branches
   TBranch        *b_measuretimes;   //!
   TBranch        *b_nametag;   //!
   TBranch        *b_channel;   //!
   TBranch        *b_temperature;   //!
   TBranch        *b_load;   //!
   TBranch        *b_Voltage_in;   //!
   TBranch        *b_Current_in;   //!
   TBranch        *b_Voltage_load;   //!
   TBranch        *b_Current_power;   //!

   MUX64_TEST(TTree *tree=0);
   virtual ~MUX64_TEST();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef MUX64_TEST_cxx
MUX64_TEST::MUX64_TEST(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("data_rootformat/B0data.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("data_rootformat/B0data.root");
      }
      f->GetObject("ntuple",tree);

   }
   Init(tree);
}

MUX64_TEST::~MUX64_TEST()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t MUX64_TEST::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t MUX64_TEST::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void MUX64_TEST::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   Voltage_in = 0;
   Current_in = 0;
   Voltage_load = 0;
   Current_power = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("measuretimes", &measuretimes, &b_measuretimes);
   fChain->SetBranchAddress("nametag", nametag, &b_nametag);
   fChain->SetBranchAddress("channel", &channel, &b_channel);
   fChain->SetBranchAddress("temperature", &temperature, &b_temperature);
   fChain->SetBranchAddress("load", &load, &b_load);
   fChain->SetBranchAddress("Voltage_in", &Voltage_in, &b_Voltage_in);
   fChain->SetBranchAddress("Current_in", &Current_in, &b_Current_in);
   fChain->SetBranchAddress("Voltage_load", &Voltage_load, &b_Voltage_load);
   fChain->SetBranchAddress("Current_power", &Current_power, &b_Current_power);
   Notify();
}

Bool_t MUX64_TEST::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void MUX64_TEST::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t MUX64_TEST::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef MUX64_TEST_cxx
