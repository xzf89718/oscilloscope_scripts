#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooPoisson.h"
#include "RooConstVar.h"
#include "RooChebychev.h"
#include "RooFormulaVar.h"

#include "RooAddPdf.h"
#include "RooProdPdf.h"
#include "RooWorkspace.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TFile.h"
#include "TH1.h"
#include <vector>
using namespace RooFit;

// Two peak and three peak no shift model is valid for this experiment, please use it to obtain Gain.
// Shift model is not available now!
int UseWorkspaceForFit(TString input_file = "gainFitWorkspace.root")
{

    auto f1 = TFile::Open(input_file, "read");
    auto f2 = TFile::Open("output_charge.root", "READ");
    // charge, include baseline
    auto h1 = (TH1F *)f2->Get("ahisto");
    // charge, deduct baseline
    auto h1_shift = (TH1F*)f2->Get("ahisto_shift");

    // Get all workspace
    auto wTwo = (RooWorkspace *)f1->Get("worksapceTwoPeak");
    auto wThree = (RooWorkspace *)f1->Get("workspaceThreePeak");
    auto wFour = (RooWorkspace *)f1->Get("workspaceFourPeak");
    auto wFive = (RooWorkspace *)f1->Get("workspaceFivePeak");
    auto wSix = (RooWorkspace *)f1->Get("workspaceSixPeak");

    // // three peak
    // auto threePeakGaus = wThree->pdf("threePeakGaus");
    // auto voltage1 = wThree->var("voltage1");
    // // auto mean1 = wThree->var("mean1");
    // // auto mean2 = wThree->var("mean2");
    // // auto mean3 = wThree->var("mean3");
    // auto data1 = wThree->data("toydataThreePeak1");

    // auto c1 = new TCanvas();
    // auto frame_voltage1 = voltage1->frame();
    // data1->plotOn(frame_voltage1);
    // threePeakGaus->fitTo(*data1);
    // threePeakGaus->plotOn(frame_voltage1);
    // frame_voltage1->Draw();
    // gPad->Update();

    // // four peak
    // auto fourPeakGaus = wFour->pdf("fourPeakGaus");
    // auto voltage2 = wFour->var("voltage2");
    // // auto mean1 = wThree->var("mean1");
    // // auto mean2 = wThree->var("mean2");
    // // auto mean3 = wThree->var("mean3");
    // // auto mean4 = wThree->var("mean4");
    // auto data2 = wFour->data("toydataFourPeak1");
    // gPad->Update();

    // auto c2 = new TCanvas();
    // auto frame_voltage2 = voltage2->frame();
    // data2->plotOn(frame_voltage2);
    // fourPeakGaus->fitTo(*data2);
    // fourPeakGaus->plotOn(frame_voltage2);
    // frame_voltage2->Draw();
    // gPad->Update();

    // // five peak
    // auto fivePeakGaus = wFive->pdf("fivePeakGaus");
    // auto voltage3 = wFive->var("voltage3");
    // // auto mean1 = wThree->var("mean1");
    // // auto mean2 = wThree->var("mean2");
    // // auto mean3 = wThree->var("mean3");
    // // auto mean4 = wThree->var("mean4");
    // // auto mean5 = wThree->var("mean5");
    // auto data3 = wFive->data("toydataFivePeak1");

    // auto c3 = new TCanvas();
    // auto frame_voltage3 = voltage3->frame();
    // data3->plotOn(frame_voltage3);
    // fivePeakGaus->fitTo(*data3);
    // fivePeakGaus->plotOn(frame_voltage3);
    // frame_voltage3->Draw();
    // gPad->Update();

    // // six peak
    // auto sixPeakGaus = wSix->pdf("sixPeakGaus");
    // auto voltage4 = wSix->var("voltage4");
    // // auto mean1 = wSix->var("mean1");
    // // auto mean2 = wSix->var("mean2");
    // // auto mean3 = wSix->var("mean3");
    // // auto mean4 = wSix->var("mean4");
    // // auto mean5 = wSix->var("mean5");
    // // auto mean6 = wSix->var("mean6");
    // auto data4 = wSix->data("toydataSixPeak1");

    // auto c4 = new TCanvas();
    // auto frame_voltage4 = voltage4->frame();
    // data4->plotOn(frame_voltage4);
    // sixPeakGaus->fitTo(*data4);
    // sixPeakGaus->plotOn(frame_voltage4);
    // frame_voltage4->Draw();
    // gPad->Update();

    // two peak
    auto twoPeakGaus = wTwo->pdf("twoPeakGaus");
    auto voltage0= wTwo->var("voltage0");
    voltage0->setRange(-5200., -4700.);
    auto mean0_1 = wTwo->var("mean1");
    // mean0_1->setRange(-4860., -4850.);
    mean0_1->setVal(-5120.);
    auto mean0_2 = wTwo->var("mean2");
    // mean0_2->setRange(-5160., -5120.);
    mean0_2->setVal(-5140.);
    RooDataHist data0("data0", "data0", *voltage0, h1);
    auto c12 = new TCanvas();
    auto frame_voltage0= voltage0->frame();
    data0.plotOn(frame_voltage0);
    twoPeakGaus->chi2FitTo(data0,PrintEvalErrors(10));
    twoPeakGaus->plotOn(frame_voltage0);
    frame_voltage0->Draw();
    gPad->Update();


    // // three peak
    // auto threePeakGaus = wThree->pdf("threePeakGaus");
    // auto voltage1= wThree->var("voltage1");
    // voltage1->setRange(-5200., -4700.);
    // auto mean1_1 = wThree->var("mean1");
    // // mean1_1->setRange(-5120., -5100.);
    // mean1_1->setVal(-5120.);
    // auto mean1_2 = wThree->var("mean2");
    // // mean1_2->setRange(-5160., -5120.);
    // mean1_2->setVal(-5130.); 
    // auto mean1_3 = wThree->var("mean3");
    // // mean1_3->setRange(-5200., -5100.);
    // // mean1_3->setVal(-5140.);
    // // auto gaus1 = wThree->pdf("gaus1ThreePeak");
    // // auto n1 = wThree->var("n1");
    // // auto gaus2 = wThree->pdf("gaus2ThreePeak");
    // // auto n2 = wThree->var("n2");
    // // auto gaus3 = wThree->pdf("gaus3ThreePeak");
    // // auto n3 = wThree->var("n3");
    // RooDataHist data1("data1", "data1", *voltage1, h1);
    // auto c13 = new TCanvas();
    // auto frame_voltage1= voltage1->frame();
    // data1.plotOn(frame_voltage1);
    // threePeakGaus->fitTo(data1,PrintEvalErrors(10));
    // threePeakGaus->plotOn(frame_voltage1);
    // threePeakGaus->plotOn(frame_voltage1, Components("gaus1ThreePeak"), LineColor(kRed), LineStyle(kDashed));
    // threePeakGaus->plotOn(frame_voltage1, Components("gaus2ThreePeak"), LineColor(kBlue), LineStyle(kDashed));
    // threePeakGaus->plotOn(frame_voltage1, Components("gaus3ThreePeak"), LineColor(kGreen), LineStyle(kDashed));
    // frame_voltage1->Draw();
    // gPad->Update();

    // three peak deduct baseline
    auto threePeakGaus = wThree->pdf("threePeakGaus");
    auto voltage1= wThree->var("voltage1");
    voltage1->setRange(-500., 100.);
    auto mean1_1 = wThree->var("mean1");
    mean1_1->setRange(-100., 0.);
    mean1_1->setVal(-10.);
    auto mean1_2 = wThree->var("mean2");
    mean1_2->setRange(-100., 0.);
    mean1_2->setVal(-10.); 
    auto mean1_3 = wThree->var("mean3");
    mean1_3->setRange(-100., -0.);
    mean1_3->setVal(-10.);
    auto n3 = wThree->var("n3");
    RooDataHist data1("data1", "data1", *voltage1, h1_shift);
    auto c13 = new TCanvas();
    auto frame_voltage1= voltage1->frame();
    data1.plotOn(frame_voltage1);
    threePeakGaus->fitTo(data1,PrintEvalErrors(10));
    threePeakGaus->plotOn(frame_voltage1);
    threePeakGaus->plotOn(frame_voltage1, Components("gaus1ThreePeak"), LineColor(kRed), LineStyle(kDashed));
    threePeakGaus->plotOn(frame_voltage1, Components("gaus2ThreePeak"), LineColor(kBlue), LineStyle(kDashed));
    threePeakGaus->plotOn(frame_voltage1, Components("gaus3ThreePeak"), LineColor(kGreen), LineStyle(kDashed));
    frame_voltage1->Draw();
    gPad->Update();

    return 0;
}
