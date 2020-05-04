# PUPPI Softdrop Mass Corrections

__THIS IS THE BRANCH FOR 102X (NOT YET APPROVED! CONTACT JMAR BEFORE USE!)__

## Introduction

This branch contains the weights needed to apply PUPPI softdrop mass corrections for 2017 and 2018 MC samples. Remember that the JMAR recommendation is __to apply these corrections to two prong fatjets with the mass close to the W boson__. These corrections are not recommended for top tagging or boosted objects with more than two prongs. 

The weights are stored under the [weights](weights/) folder of this branch. For other versions, please look at a different branch.



## Example on how to apply these corrections: 

```
float puppiCorr = getPUPPIweight( AK8jetPt , AK8jetEta );
float jetmass = AK8PUPPISoftdropUncorrectedMass*puppiCorr;

float ExoDiBosonAnalysis::getPUPPIweight(float puppipt, float puppieta ){

 TFile* file = TFile::Open( "weights/puppiCorr_2017.root","READ");
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
