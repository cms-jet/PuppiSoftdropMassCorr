# PUPPI Softdrop Mass Corrections
Scripts and weights for correcting PUPPI softdrop mass. Weights for CMSSW 80X are stored in the "weights/" folder of the master branch, while weights for CMSSW 76X can be found in the same folder of the branch "76X". For futher details, see presentation at https://indico.cern.ch/event/559594/contributions/2258188/attachments/1316911/1973452/puppiSoftdropJMScorr_2707.pdf.

## Get uncorrected PUPPI soft drop mass from MINIAOD:
```
TLorentzVector puppi_softdrop, puppi_softdrop_subjet;
        auto const & sdSubjetsPuppi = jet.subjets("SoftDropPuppi");
        for ( auto const & it : sdSubjetsPuppi ) {
          puppi_softdrop_subjet.SetPtEtaPhiM(it->correctedP4(0).pt(),it->correctedP4(0).eta(),it->correctedP4(0).phi(),it->correctedP4(0).mass());
          puppi_softdrop+=puppi_softdrop_subjet;
        }
```
## Get PUPPI soft drop mass correction:
```
float puppiCorr = getPUPPIweight( (data_.jetAK8_puppi_pt).at(j) , (data_.jetAK8_puppi_eta).at(j) );
float jetmass = (*data_.jetAK8_puppi_softdrop_massUnCorr)[j]*puppiCorr;

float ExoDiBosonAnalysis::getPUPPIweight(float puppipt, float puppieta ){

 TFile* file = TFile::Open( "weights/puppiJecCorr.root","READ");
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
