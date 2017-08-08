# PUPPI Softdrop Mass Corrections
Scripts and weights for correcting PUPPI softdrop mass. Weights for CMSSW 80X are stored in the "weights/" folder of the master branch, while weights for CMSSW 76X can be found in the same folder of the branch "76X". For futher details, see presentation at https://indico.cern.ch/event/559594/contributions/2258188/attachments/1316911/1973452/puppiSoftdropJMScorr_2707.pdf.

## Get uncorrected PUPPI soft drop mass from MINIAOD:
When running on MINIAOD, the uncorrected PUPPI softdrop mass can be obtained in the following way:
```
TLorentzVector puppi_softdrop, puppi_softdrop_subjet;
        auto const & sdSubjetsPuppi = jet.subjets("SoftDropPuppi");
        for ( auto const & it : sdSubjetsPuppi ) {
          puppi_softdrop_subjet.SetPtEtaPhiM(it->correctedP4(0).pt(),it->correctedP4(0).eta(),it->correctedP4(0).phi(),it->correctedP4(0).mass());
          puppi_softdrop+=puppi_softdrop_subjet;
        }
```

## Get PUPPI soft drop mass correction:
To compute the weights, the AK8 jet pt and eta must be passed, where the jet pT should be corrected with the newest JEC corrections available for MC(data). For the AK8 jet pt and eta, either CHS AK8 jets or PUPPI AK8 jets with full JEC applied can be used (but not the PUPPI softdrop AK8 jet pt and eta, unless they are shown to have the same JES as the ungroomed jets). In the example below, these are called "AK8jetPt" and "AK8jetEta" respectively. The returned weight is then applied to the uncorrected PUPPI softdrop mass, which can be obtained following the example above ("Get uncorrected PUPPI soft drop mass from MINIAOD").
```
float puppiCorr = getPUPPIweight( AK8jetPt , AK8jetEta );
float jetmass = AK8PUPPISoftdropUncorrectedMass*puppiCorr;

float ExoDiBosonAnalysis::getPUPPIweight(float puppipt, float puppieta ){

 TFile* file = TFile::Open( "weights/puppiCorr.root","READ");
  puppisd_corrGEN      = (TF1*)file->Get("puppiJECcorr_gen");
  puppisd_corrRECO_cen = (TF1*)file->Get("puppiJECcorr_reco_0eta1v3");
  puppisd_corrRECO_for = (TF1*)file->Get("puppiJECcorr_reco_1v3eta2v5");


  float genCorr  = 1.;
  float recoCorr = 1.;
  float totalWeight = 1.;
        
  genCorr =  puppisd_corrGEN->Eval( puppipt );
  if( fabs(puppieta)  <= 1.3 ){
    recoCorr = puppisd_corrRECO_cen->Eval( puppipt );
  }
  else{
    recoCorr = puppisd_corrRECO_for->Eval( puppipt );
  }
  
  totalWeight = genCorr * recoCorr;

  return totalWeight;
}
```
