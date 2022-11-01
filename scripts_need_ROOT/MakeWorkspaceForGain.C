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

int MakeWorkspaceForGain()
{
    RooWorkspace worksapceTwoPeak("worksapceTwoPeak");
    RooWorkspace workspaceThreePeak("workspaceThreePeak");
    RooWorkspace workspaceFourPeak("workspaceFourPeak");
    RooWorkspace workspaceFivePeak("workspaceFivePeak");
    RooWorkspace workspaceSixPeak("workspaceSixPeak");


    // build three gaussian to fit the data
    RooRealVar voltage0("voltage0", "Any unit", -5500., -4000.);
    RooRealVar voltage1("voltage1", "Any unit", -5500., -4000.);
    RooRealVar voltage2("voltage2", "Any unit", -5500., -4000.);
    RooRealVar voltage3("voltage3", "Any unit", -5500., -4000.);
    RooRealVar voltage4("voltage4", "Any unit", -5500., -4000.);


    // Use gaussian as approximation of poisson
    RooRealVar mean1("mean1", "Any unit", -4900., -5500., -4800.);
    RooRealVar mean2("mean2", "Any unit", -4900., -5500., -4800.);
    RooRealVar mean3("mean3", "Any unit", -4900., -5500., -4800.);
    RooRealVar mean4("mean4", "Any unit", -4900., -5500., -4800.);
    RooRealVar mean5("mean5", "Any unit", -4900., -5500., -4800.);
    RooRealVar mean6("mean6", "Any unit", -4900., -5500., -4800.);


    // Use gaussian as approximation of poisson
    RooRealVar var1("var1", "var1", 10., 1.0, 1000.);
    RooRealVar var2("var2", "var2", 10., 1.0, 1000.);
    RooRealVar var3("var3", "var3", 10., 1.0, 1000.);
    RooRealVar var4("var4", "var4", 10., 1.0, 1000.);
    RooRealVar var5("var5", "var5", 10., 1.0, 1000.);
    RooRealVar var6("var6", "var6", 10., 1.0, 1000.);

    // Build gaussian
    RooGaussian gaus1TwoPeak("gaus1TwoPeak", "gaus1TwoPeak", voltage0, mean1, var1);
    RooGaussian gaus2TwoPeak("gaus2TwoPeak", "gaus2TwoPeak", voltage0, mean2, var2);

    RooGaussian gaus1ThreePeak("gaus1ThreePeak", "gaus1ThreePeak", voltage1, mean1, var1);
    RooGaussian gaus2ThreePeak("gaus2ThreePeak", "gaus2ThreePeak", voltage1, mean2, var2);
    RooGaussian gaus3ThreePeak("gaus3ThreePeak", "gaus3ThreePeak", voltage1, mean3, var3);

    RooGaussian gaus1FourPeak("gaus1FourPeak", "gaus1FourPeak", voltage2, mean1, var1);
    RooGaussian gaus2FourPeak("gaus2FourPeak", "gaus2FourPeak", voltage2, mean2, var2);
    RooGaussian gaus3FourPeak("gaus3FourPeak", "gaus3FourPeak", voltage2, mean3, var3);
    RooGaussian gaus4FourPeak("gaus4FourPeak", "gaus4FourPeak", voltage2, mean4, var4);

    RooGaussian gaus1FivePeak("gaus1FivePeak", "gaus1FivePeak", voltage3, mean1, var1);
    RooGaussian gaus2FivePeak("gaus2FivePeak", "gaus2FivePeak", voltage3, mean2, var2);
    RooGaussian gaus3FivePeak("gaus3FivePeak", "gaus3FivePeak", voltage3, mean3, var3);
    RooGaussian gaus4FivePeak("gaus4FivePeak", "gaus4FivePeak", voltage3, mean4, var4);
    RooGaussian gaus5FivePeak("gaus5FivePeak", "gaus5FivePeak", voltage3, mean5, var5);

    RooGaussian gaus1SixPeak("gaus1SixPeak", "gaus1SixPeak", voltage4, mean1, var1);
    RooGaussian gaus2SixPeak("gaus2SixPeak", "gaus2SixPeak", voltage4, mean2, var2);
    RooGaussian gaus3SixPeak("gaus3SixPeak", "gaus3SixPeak", voltage4, mean3, var3);
    RooGaussian gaus4SixPeak("gaus4SixPeak", "gaus4SixPeak", voltage4, mean4, var4);
    RooGaussian gaus5SixPeak("gaus5SixPeak", "gaus5SixPeak", voltage4, mean5, var5);
    RooGaussian gaus6SixPeak("gaus6SixPeak", "gaus6SixPeak", voltage4, mean6, var6);

        // Fraction of different gaussian
    RooRealVar n1("n1", "#Number of peak 1", 0.1, 0., 1.);
    RooRealVar n2("n2", "#Number of peak 2", 0.1, 0., 1.);
    RooRealVar n3("n3", "#Number of peak 3", 0.1, 0., 1.);
    RooRealVar n4("n4", "#Number of peak 4", 0.1, 0., 1.);
    RooRealVar n5("n5", "#Number of peak 5", 0.1, 0., 1.);
    RooRealVar n6("n6", "#Number of peak 6", 0.1, 0., 1.);
    // Build combined distribution PDF
    RooAddPdf twoPeakGaus("twoPeakGaus", "gaus1+gaus2", RooArgList(gaus1TwoPeak, gaus2TwoPeak), RooArgList(n1));
    RooAddPdf threePeakGaus("threePeakGaus", "gaus1+gaus2+gaus3", RooArgList(gaus1ThreePeak, gaus2ThreePeak, gaus3ThreePeak), RooArgList(n1, n2));
    RooAddPdf fourPeakGaus("fourPeakGaus", "gaus1+gaus2+gaus3+gaus4", RooArgList(gaus1FourPeak, gaus2FourPeak, gaus3FourPeak, gaus4FourPeak), RooArgList(n1, n2, n3));
    RooAddPdf fivePeakGaus("fivePeakGaus", "gaus1+gaus2+gaus3+gaus4+gaus5", RooArgList(gaus1FivePeak, gaus2FivePeak, gaus3FivePeak, gaus4FivePeak, gaus5FivePeak), RooArgList(n1, n2, n3, n4));
    RooAddPdf sixPeakGaus("sixPeakGaus", "gaus1+gaus2+gaus3+gaus4+gaus5+gaus6", RooArgList(gaus1SixPeak, gaus2SixPeak, gaus3SixPeak, gaus4SixPeak, gaus5SixPeak, gaus6SixPeak), RooArgList(n1, n2, n3, n4, n5));


    worksapceTwoPeak.import(twoPeakGaus);
    workspaceThreePeak.import(threePeakGaus);
    workspaceFourPeak.import(fourPeakGaus);
    workspaceFivePeak.import(fivePeakGaus);
    workspaceSixPeak.import(sixPeakGaus);

    // Generate toy model
    // for (auto i = 0; i < 100; i++)
    // {
    //     RooDataSet *dataThreePeak = threePeakGaus.generate(voltage1, 10000, Name((std::string("toydataThreePeak") + std::to_string(i)).c_str()));
    //     RooDataSet *dataFourPeak = fourPeakGaus.generate(voltage2, 10000, Name((std::string("toydataFourPeak") + std::to_string(i)).c_str()));
    //     RooDataSet *dataFivePeak = fivePeakGaus.generate(voltage3, 10000, Name((std::string("toydataFivePeak") + std::to_string(i)).c_str()));
    //     RooDataSet *dataSixPeak = sixPeakGaus.generate(voltage4, 10000, Name((std::string("toydataSixPeak") + std::to_string(i)).c_str()));

    //     workspaceThreePeak.import(*dataThreePeak);
    //     workspaceFourPeak.import(*dataFourPeak);
    //     workspaceFivePeak.import(*dataFivePeak);
    //     workspaceSixPeak.import(*dataSixPeak);

    // }
    // auto *toydataThreePeak = workspaceThreePeak.data("toydataThreePeak100");
    // threePeakGaus.fitTo(*toydataThreePeak);
    // auto *toydataFourPeak = workspaceFourPeak.data("toydataFourPeak100");
    // fourPeakGaus.fitTo(*toydataFourPeak);
    // auto *toydataFivePeak = workspaceFivePeak.data("toydataFivePeak100");
    // fivePeakGaus.fitTo(*toydataFivePeak);
    // auto *toydataSixPeak = workspaceSixPeak.data("toydataSixPeak100");
    // sixPeakGaus.fitTo(*toydataSixPeak);

    workspaceThreePeak.writeToFile("gainFitWorkspace.root", true);
    worksapceTwoPeak.writeToFile("gainFitWorkspace.root", false);
    workspaceFourPeak.writeToFile("gainFitWorkspace.root", false);
    workspaceFivePeak.writeToFile("gainFitWorkspace.root", false);
    workspaceSixPeak.writeToFile("gainFitWorkspace.root", false);
    return 0;
}
