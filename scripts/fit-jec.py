import time
import CMS_lumi, tdrstyle
from ROOT import *
from array import *
import math
import numpy as np
from optparse import OptionParser

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = ""
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod=4

parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('-r','--reco', action='store_true', dest='calculateRecoJEC', default=False, help='calculate reco JEC')

(options, args) = parser.parse_args()

if options.noX: 
  gROOT.SetBatch(True)

gStyle.SetOptFit(0)

def getCanvas():
  c = TCanvas("c","c",800,800)
  c.GetWindowHeight()
  c.GetWindowWidth()
  c.SetTitle("")
  return c
  
def get_palette(mode):
 palette = {}
 palette['gv'] = [] 
 colors = ['#40004b','#762a83','#9970ab','#de77ae','#a6dba0','#5aae61','#1b7837','#00441b','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#762a83','#de77ae','#a6dba0','#92c5de','#4393c3','#2166ac','#053061']
 colors = ['#FF420E','#80BD9E','#a6dba0','#92c5de','#4393c3','#2166ac','#053061','#40004b','#762a83','#9970ab','#de77ae']
 for c in colors:
  palette['gv'].append(c)
 return palette[mode]
 
palette = get_palette('gv')
col = TColor()

filetmp = TFile.Open("input/genCorr.root","READ")   
gC_forCorr = filetmp.Get("gC_forCorr")
gF_forCorr = filetmp.Get("gF_forCorr")

if options.calculateRecoJEC: 
  filetmp = TFile.Open("input/recoCorr.root","READ")   
  gC_forCorr = filetmp.Get("gC_forCorr")
  gF_forCorr = filetmp.Get("gF_forCorr")
  
canv = getCanvas()
canv.cd()
canv.SetName("fitGEN")
vFrame = canv.DrawFrame(200,0.95,3100,1.1)
vFrame.SetYTitle("m_{PDG} / m_{gen}")
if options.calculateRecoJEC: 
  canv.SetName("fitRECO")
  vFrame = canv.DrawFrame(200,1.0,3100,1.4)
  vFrame.SetYTitle("m_{gen} / m_{reco}")


vFrame.SetXTitle("p_{T} (GeV)")
vFrame.GetXaxis().SetTitleSize(0.06)
vFrame.GetXaxis().SetTitleOffset(0.95)
vFrame.GetXaxis().SetLabelSize(0.05)
vFrame.GetYaxis().SetTitleSize(0.06)
vFrame.GetYaxis().SetTitleOffset(1.2)
vFrame.GetYaxis().SetLabelSize(0.05)
vFrame.GetXaxis().SetNdivisions(809)
vFrame.GetYaxis().SetNdivisions(707)
gC_forCorr.SetMarkerSize(1.6)
gF_forCorr.SetMarkerSize(1.6)
gC_forCorr.SetMarkerStyle(20)
gF_forCorr.SetMarkerStyle(20)
gC_forCorr.SetMarkerColor(col.GetColor(palette[0]))
gF_forCorr.SetMarkerColor(col.GetColor(palette[1]))
gC_forCorr.SetLineColor(col.GetColor(palette[0]))
gF_forCorr.SetLineColor(col.GetColor(palette[1]))
l = TLegend(0.60461809,0.7620725,0.7559296,0.9009845)
l.SetTextSize(0.035)
l.SetLineColor(0)
l.SetShadowColor(0)
l.SetLineStyle(1)
l.SetLineWidth(1)
l.SetFillColor(0)
l.SetFillStyle(0)
l.SetMargin(0.35)

fitmin = TMath.MinElement(gC_forCorr.GetN(),gC_forCorr.GetX())
fitmin = 200.
fitmax = TMath.MaxElement(gC_forCorr.GetN(),gC_forCorr.GetX())
print "Fitting range: [%.2f,%.2f] "%(fitmin,fitmax)

if not options.calculateRecoJEC: 
  l.AddEntry(gC_forCorr, "Gen correction","p")
  g = TF1("puppiJECcorr_gen","[0]+[1]*pow(x*[2],-[3])",fitmin,fitmax)
  g.SetParameter(0,  0.97)
  g.SetParameter(1, -3.51252e+00)
  # g.SetParameter(2,  2.76144e-02)
  g.SetParameter(2,  0.04)
  g.SetParLimits(2,  0.06,0.08)
  g.SetParameter(3,  2.27721e+00)
  # g.SetParameter(4, 1.04)
  # g = TF1("gJEC","pol4",fitmin,fitmax) # "W" Set all weights to 1;ignore error bars "R" Use the Range specified in the function range  "U" Use a User specified fitting algorithm (via SetFCN)  "F" If fitting a polN, switch to minuit fitter
  
  #Fit
  gC_forCorr.Fit(g, "FRU")
  gC_forCorr.Fit(g, "FRU")
  gC_forCorr.Fit(g, "FRU")
  gC_forCorr.Draw("PEsame")
  
  #Write to file
  jecCorr_gen = gC_forCorr.GetFunction("puppiJECcorr_gen")
  filename = "weights/puppiCorr"
  f = TFile("%s.root"%filename,  "UPDATE")
  print "Writing to file " ,f.GetName()
  jecCorr_gen.Write("",TObject.kOverwrite)
  canv.Write("",TObject.kOverwrite)
  f.Close()  
  
elif options.calculateRecoJEC:
  l.AddEntry(gF_forCorr, "Reco corr. |#eta| > 1.3","p")
  l.AddEntry(gC_forCorr, "Reco corr. |#eta| #leq 1.3","p")

  g = TF1("puppiJECcorr_reco_0eta1v3","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)",fitmin,fitmax)
  # g = TF1("puppiJECcorr_reco_0eta1v3","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)",fitmin,fitmax)
  
  # g = TF1("gJEC","pol4",fitmin,fitmax)
  # g.SetParameter(0,      1.21228)
 #  g.SetParameter(1, -0.000559701)
 #  g.SetParameter(2,  8.96666e-07)
 #  g.SetParameter(3, -5.44342e-10)
 #  g.SetParameter(4,   1.1131e-13)
 #  g.SetParameter(5, -1.95118e-17)
  
  g.SetParameter(0, 9.95307e-01)
  g.SetParameter(1, 1.98033e-04)
  g.SetParameter(2,-1.42701e-07)
  g.SetParameter(3, 4.20355e-11)
  g.SetParameter(4,-4.37768e-15)

#
#
#
#
#   g.SetParameter(5, -1.64570e-16)
#   g.SetParameter(6,  -1.55572e-17)

  
  print "Fitting for central region" 
  for i in range(0,10):
    gC_forCorr.Fit(g, "EX0FRU")
 
  gC_forCorr.Draw("PEsame") 
  
  print "" ; print "" ; print "" ;
  # sC = TSpline3("SPLINE_puppiJECcorr_reco_0eta1v3",gC_forCorr,"",fitmin,fitmax)
  # sC.SetLineColor(kBlue)
  # s.Draw("same")
  # gC_forCorr.Draw("PEsame")
  
  # g2 = TF1("gJEC2","pol3",fitmin,fitmax)
  g2 = TF1("puppiJECcorr_reco_1v3eta2v5","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)",fitmin,fitmax)
  # g2 = TF1("puppiJECcorr_reco_1v3eta2v5","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)",fitmin,fitmax)
  # g2.SetParameter(0,  1.40318e+00)
  # g2.SetParameter(1, -1.22826e-03)
  # g2.SetParameter(2,  2.16362e-06)
  # g2.SetParameter(3, -1.66125e-09)
  # g2.SetParameter(4,  4.81044e-13)
  # g2.SetParameter(5, -2.33647e-13)
  # g2.SetParameter(6, -2.41196e-17)
  g2.SetParameter(0, 1.10752e+00)
  g2.SetParameter(1,-1.86182e-05)
  g2.SetParameter(2, 9.31589e-08)
  g2.SetParameter(3,-5.17814e-11)
  g2.SetParameter(4, 8.12939e-15)

  print "Fitting for forward region" 
  for i in range(0,10):
    gF_forCorr.Fit(g2, "EX0FRU")


  gF_forCorr.Draw("PEsame")


  # sF = TSpline3("SPLINE_puppiJECcorr_reco_1v3eta2v5",gF_forCorr,"",fitmin,fitmax)
  # sF.SetLineColor(kBlue)
  # s2.Draw("same")
  # gF_forCorr.Draw("PEsame")
  jecCorr_reco_central = gC_forCorr.GetFunction("puppiJECcorr_reco_0eta1v3")
  jecCorr_reco_forward = gF_forCorr.GetFunction("puppiJECcorr_reco_1v3eta2v5")

  filename = "weights/puppiCorr"
  f = TFile("%s.root"%filename,  "UPDATE")
  print "Writing to file " ,f.GetName()
  jecCorr_reco_central.Write("",TObject.kOverwrite)
  jecCorr_reco_forward.Write("",TObject.kOverwrite)
  # sC.Write("",TObject.kOverwrite)
  # sF.Write("",TObject.kOverwrite)
  canv.Write("",TObject.kOverwrite)
  f.Close()


 
l.Draw("same")
CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
canv.Update()
postfix = "gen"
if options.calculateRecoJEC: postfix = "reco"
canvname = "JMC_fit_%s.pdf"%(postfix)
canv.SaveAs(canvname,"pdf")
canv.SaveAs(canvname.replace("pdf","root"),"pdf")
time.sleep(20)


