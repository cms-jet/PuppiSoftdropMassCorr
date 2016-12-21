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
parser.add_option('-m','--mshift', action='store_true', dest='doMassShiftFit', default=False, help='Fit (reco-gen)/reco instead of pruned mass!')
parser.add_option('-p','--pruning', action='store_true', dest='doPruning', default=False, help='Fit pruned mass')
parser.add_option('--fitGen', action='store_true', dest='fitGenMass', default=False, help='Fit gen mass')

(options, args) = parser.parse_args()

if options.noX: gROOT.SetBatch(True)

#prefix = '/mnt/t3nfs01/data01/shome/thaarres/EXOVVAnalysisRunII/AnalysisOutput/80X/'
prefix = '/mnt/t3nfs01/data01/shome/dschafer/AnalysisOutput/80X/SignalMC/Summer16/'
gStyle.SetOptFit(1)

def get_line(xmin,xmax,ymin,ymax,style):
   line = TLine(xmin,ymin,xmax,ymax)
   line.SetLineColor(kRed)
   line.SetLineStyle(style)
   line.SetLineWidth(2)
   return line
   
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
 colors = ['#762a83','#de77ae','#a6dba0','#92c5de','#4393c3','#2166ac','#053061','#5aae61','#1b7837','#00441b']
 colors = ['#FF420E','#80BD9E','#a6dba0','#92c5de','#4393c3','#2166ac','#053061','#40004b','#762a83','#9970ab','#de77ae']

 for c in colors:
  palette['gv'].append(c)
 
 return palette[mode]
 
palette = get_palette('gv')
col = TColor()

masses = [1000,1200,1400,1600,1800,2000,2500,3000,4000,4500]  
masses = [600,1000,1200,1400,1800,2000,3000,3500,4000,4500] #Zprime #Ops!! 400 masspoint is named for convenience and is actually SM WW, not signal sample!
masses = [600,1000,1200,2000,2500,3000] #BulkGrav
#masses = [600,800,1800,2000,2500,3500,4500] #Wprime

hCentral = 'gen_SoftdropMass_eta1v3_NEWCORR'
hForward = 'gen_SoftdropMass_etaUP1v3_NEWCORR'

if options.fitGenMass:
    hCentral = 'GenAK8SoftdropMass_eta1v3_CORR'
    hForward = 'GenAK8SoftdropMass_etaUP1v3_CORR'

lineStyle = [1,1,1,1,3,3,3,3]


signals = ["BulkWW","BulkZZ","ZprimeWW","WprimeWZ"]
signals = ["BulkWW"]
#signals = ["WprimeWZ"]
ptsCEN = []

for signal in signals:
 
  filelist = []
  histosCEN = []
  histosFOR = []

  l = TLegend(0.7781766,0.7480056,0.9217516,0.9186611)
  l.SetTextSize(0.04106571)
  l.SetLineColor(0)
  l.SetShadowColor(0)
  l.SetLineStyle(1)
  l.SetLineWidth(1)
  l.SetFillColor(0)
  l.SetFillStyle(0)
  l.SetMargin(0.35)
  
  meansCentral = []
  meanErrCentral = []
  sigmasCentral = []
  sigErrCentral = []
  ptsCEN = []
  ptErrCEN = []
  meansForward = []
  meanErrForward = []
  sigmasForward = []
  sigErrForward = []
  ptsFOR = []
  ptErrFOR = []
  masspoints = []
  
  
  for m in masses:
    filename = prefix + 'ExoDiBosonAnalysis.' + signal + '_13TeV_' + "%s"%m + 'GeV.VV.root'
    filetmp = TFile.Open(filename,"READ")
    filetmp.SetName(filename)
    print "opening " ,filename
    filelist.append(filetmp)
    masspoints.append(m)
  
  i = -1  
  for filetmp in filelist:
    i += 1
    #Central
    histtmpC = TH1F(filetmp.Get(hCentral))
    histtmpC.SetName("Central_%i"%masspoints[i])
    maxbin=0
    maxcontent=0
    startbin = 60.
    for b in range(histtmpC.GetXaxis().GetNbins()):
      if histtmpC.GetXaxis().GetBinCenter(b+1) > startbin and histtmpC.GetBinContent(b+1)>maxcontent:
        maxbin = b
        maxcontent = histtmpC.GetBinContent(b+1)   
    tmpmean = histtmpC.GetXaxis().GetBinCenter(maxbin)   
    g1 = TF1("g1CEN%i"%m,"gaus",tmpmean-11.,tmpmean+15.)
    histtmpC.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    g1 = TF1("g1CEN%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpC.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    g1 = TF1("g1CEN%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpC.Fit(g1, "SR")
    print ""
    histosCEN.append(histtmpC)
    mean    = g1.GetParameter(1)
    meanerr = g1.GetParError(1)
    meansCentral.append(mean)
    meanErrCentral.append(meanerr)
  
    #Forward
    histtmpF = TH1F(filetmp.Get(hForward))
    histtmpF.SetName("Forward%i"%masspoints[i])
    maxbin=0
    maxcontent=0
    startbin = 70.
    for b in range(histtmpF.GetXaxis().GetNbins()):
      if histtmpF.GetXaxis().GetBinCenter(b+1)>startbin and histtmpF.GetBinContent(b+1)>maxcontent:
        maxbin = b
        maxcontent = histtmpF.GetBinContent(b+1)
    tmpmean = histtmpF.GetXaxis().GetBinCenter(maxbin)
    g1 = TF1("g1FOR%i"%m,"gaus", tmpmean-11.,tmpmean+15.)
    histtmpF.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    g1 = TF1("g1FOR%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpC.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    g1 = TF1("g1FOR%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpC.Fit(g1, "SR")
    print ""
    histosFOR.append(histtmpF)
    mean    = g1.GetParameter(1)
    meanerr = g1.GetParError(1)
    meansForward.append(mean)
    meanErrForward.append(meanerr)
 
    ptsCEN.append(TH1F(filetmp.Get("gen_pt_eta1v3")).GetMean())
    ptErrCEN.append(TH1F(filetmp.Get("gen_pt_eta1v3")).GetMeanError())
   
    ptsFOR.append(TH1F(filetmp.Get("gen_pt_etaUP1v3")).GetMean())
    ptErrFOR.append(TH1F(filetmp.Get("gen_pt_etaUP1v3")).GetMeanError())
  
  
  filename = "allmassfits"
  f = TFile("%s.root"%filename,  "RECREATE")
  print "Writing to file " ,f.GetName()
  
  l1= TLegend(0.6861809,0.6520725,0.7859296,0.9209845)
  l1.SetTextSize(0.035)
  l1.SetLineColor(0)
  l1.SetShadowColor(0)
  l1.SetLineStyle(1)
  l1.SetLineWidth(1)
  l1.SetFillColor(0)
  l1.SetFillStyle(0)
  l1.SetMargin(0.35)

  for j in xrange(0,len(histosCEN)):
    histosCEN[j].Write() 
    histosFOR[j].Write()
    histosCEN[j].Scale(1./histosCEN[j].Integral())
    histosFOR[j].Scale(1./histosFOR[j].Integral())
    histosCEN[j].SetLineColor(col.GetColor(palette[j]))
    histosCEN[j].SetLineWidth(2)
    histosCEN[j].Rebin(4) 
    histosFOR[j].SetLineColor(col.GetColor(palette[j]))
    histosFOR[j].SetLineWidth(2)
    histosFOR[j].Rebin(4)
    l1.AddEntry(histosCEN[j], "M = %i"%masspoints[j],"l")
    
  f.Close()  
  # fits = []
  # for j in xrange(0,len(histosCEN)):
  #   fittmp = TGraph(histosCEN[j])
  #   fits.append(fittmp)
  #   fittmp = TGraph(histosFOR[j])
  #   fits.append(fittmp)
    
  canv = getCanvas()
  canv.cd()
  yTitle = "Arbitrary scale"
   
  canv = getCanvas()
  canv.cd()
  setmax = histosCEN[0].GetMaximum()*2.0
  vFrame = canv.DrawFrame(40.,0.000005,120.,setmax)  
  vFrame.SetXTitle("PUPPI softdrop mass")
  vFrame.SetYTitle(yTitle)
  vFrame.GetXaxis().SetTitleSize(0.06)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.05)
  vFrame.GetYaxis().SetTitleSize(0.06)
  #vFrame.GetYaxis().SetTitleOffset(1.0)
  vFrame.GetYaxis().SetLabelSize(0.05)
  vFrame.GetXaxis().SetNdivisions(408)
  vFrame.GetYaxis().SetNdivisions(404)
  for h in histosCEN: h.Draw("HISTsame")
  l1.Draw("same")
  li = get_line(80.4,80.4,0.,0.13,1)
  li.Draw("same")
  canv.Print("Closure_massfits_CEN.pdf")
  
  canv = getCanvas()
  canv.cd()
  setmax = histosFOR[0].GetMaximum()*2.0
  vFrame = canv.DrawFrame(40.,0.000005,120.,setmax)  
  vFrame.SetXTitle("PUPPI softdrop mass")
  vFrame.SetYTitle(yTitle)
  vFrame.GetXaxis().SetTitleSize(0.06)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.05)
  vFrame.GetYaxis().SetTitleSize(0.06)
  #vFrame.GetYaxis().SetTitleOffset(1.0)
  vFrame.GetYaxis().SetLabelSize(0.05)
  vFrame.GetXaxis().SetNdivisions(408)
  vFrame.GetYaxis().SetNdivisions(404)
  for h in histosFOR: h.Draw("HISTsame")
  l1.Draw("same")
  li.Draw("same")
  canv.Print("JEC_closure_massfits_FOR.pdf")
  
  
  print signal
  for i in range(0,len(masspoints)):
    print "Central:  Mass = %i  GeV pT = %.2f +/- %.2f GeV" %(masspoints[i], ptsCEN[i],  ptErrCEN[i] )
    print "Central:  Softdrop mass = %.2f +/- %.2f GeV" %(meansCentral[i], meanErrCentral[i] )
    print ""
    print "Forward:  Mass = %i  GeV pT = %.2f +/- %.2f GeV" %(masspoints[i], ptsFOR[i],  ptErrFOR[i] )
    print "Forward:  Softdrop mass = %.2f +/- %.2f GeV" %(meansForward[i], meanErrForward[i] )
    print "";print ""
  
  
  vxCEN = array("f",ptsCEN)
  vxErrCEN = array("f",ptErrCEN)
  vxFOR = array("f",ptsFOR)
  vxErrFOR = array("f",ptErrFOR)
  vyCEN = array("f",meansCentral)
  errCEN = array("f",meanErrCentral)
  vyFOR = array("f",meansForward)
  errFOR = array("f",meanErrForward)
  # gCEN = TGraphAsymmErrors(len(vxCEN),vxCEN,vyCEN,vxErrCEN,errCEN)
  # gFOR = TGraphAsymmErrors(len(vxFOR),vxFOR,vyFOR,vxErrFOR,errFOR)

  gCEN = TGraphErrors(len(vxCEN),vxCEN,vyCEN,vxErrCEN,errCEN)
  gFOR = TGraphErrors(len(vxFOR),vxFOR,vyFOR,vxErrFOR,errFOR)

  canv = getCanvas()
  canv.cd()
  canv.Divide(1,2,0,0,0)
  canv.cd(1)
  p11_1 = canv.GetPad(1)
  p11_1.SetPad(0.01,0.35,0.99,0.98)
  p11_1.SetRightMargin(0.05)
  p11_1.SetTopMargin(0.05)
  p11_1.SetFillColor(0)
  p11_1.SetBorderMode(0)
  p11_1.SetFrameFillStyle(0)
  p11_1.SetFrameBorderMode(0)
  vFrame = canv.DrawFrame(200,75.,2200,85.)
  if signal.find("WprimeWZ")!=-1:
      vFrame = canv.DrawFrame(200,85.,2200,95.)
  vFrame.SetYTitle("<m>_{m_{reco}} (GeV)")
  vFrame.SetXTitle("p_{T} (GeV)")
  vFrame.GetXaxis().SetTitleSize(0.08)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.08)
  vFrame.GetYaxis().SetTitleSize(0.08)
  vFrame.GetYaxis().SetTitleOffset(0.8)
  vFrame.GetYaxis().SetLabelSize(0.05)
  vFrame.GetXaxis().SetNdivisions(809)
  vFrame.GetYaxis().SetNdivisions(908)
  
  gCEN.SetMarkerSize(1.6)
  gFOR.SetMarkerSize(1.6)
  gCEN.SetMarkerStyle(20)
  gFOR.SetMarkerStyle(20)
  gCEN.SetMarkerColor(col.GetColor(palette[0]))
  gFOR.SetMarkerColor(col.GetColor(palette[1]))
  gCEN.SetLineColor(col.GetColor(palette[0]))
  gFOR.SetLineColor(col.GetColor(palette[1]))

  gCEN.Draw("PLsame")
  gFOR.Draw("PLsame")
  l.AddEntry(gCEN, "|#eta|<1.3","p")
  l.AddEntry(gFOR, "|#eta|>1.3","p")
  
  addInfo = TPaveText(0.6101938,0.05099104,0.7781766,0.2956658,"NDC")
  if options.fitGenMass or options.doMassShiftFit: addInfo = TPaveText(0.1959799,0.1632124,0.3580402,0.3717617,"NDC")
  if not options.fitGenMass:
    if options.doPruning: 
       addInfo.AddText("Pruned mass")
    else:
       addInfo.AddText("PUPPI softdrop mass")  
  else:    
    if options.doPruning:  
       addInfo.AddText("Gen pruned mass") 
    else:
       addInfo.AddText("Gen softdrop mass")
  if signal.find("BulkWW") != -1: addInfo.AddText("Bulk G #rightarrow WW")
  elif signal.find("BulkZZ") != -1: addInfo.AddText("Bulk G #rightarrow ZZ")
  elif signal.find("WprimeWZ") != -1: addInfo.AddText("W'#rightarrow WZ")
  elif signal.find("ZprimeWW") != -1: addInfo.AddText("Z' #rightarrow WW")     
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.045)
  addInfo.SetTextAlign(12)
  addInfo.AddText("AK, R= 0.8")
  addInfo.AddText("Mass correction applied")
  addInfo.AddText("p_{T} > 200 GeV, |#eta| < 2.5")
  addInfo.Draw("same")
  l.Draw("same")
  CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
 
  canv.Update()
  canv.cd(2)
  
  filetmp = TFile.Open("/mnt/t3nfs01/data01/shome/dschafer/PuppiSoftdropMassCorr/weights/puppiCorr.root","READ")
  histtmpCEN = TF1(filetmp.Get("puppiJECcorr_reco_0eta1v3"))
  histtmpFOR = TF1(filetmp.Get("puppiJECcorr_reco_1v3eta2v5"))
  histtmpGEN = TF1(filetmp.Get("puppiJECcorr_gen"))
  
  histtmpCEN.SetLineColor(col.GetColor(palette[0]))
  histtmpFOR.SetLineColor(col.GetColor(palette[1]))
  
  p11_2 = canv.GetPad(2)
  p11_2.SetPad(0.01,0.02,0.99,0.35)
  p11_2.SetBottomMargin(0.35)
  p11_2.SetRightMargin(0.05)
  # p11_2.SetGridx()
  # p11_2.SetGridy()
  vFrame2 = p11_2.DrawFrame(p11_1.GetUxmin(),0.92, p11_1.GetUxmax(), 1.43)
  vFrame2.SetXTitle("<p_{T}> (GeV)")
  vFrame2.SetYTitle("Weight")
  vFrame2.GetXaxis().SetTitleSize(0.09)
  vFrame2.GetYaxis().SetTitleSize(0.15)
  vFrame2.GetYaxis().SetTitleOffset(0.40)
  vFrame2.GetYaxis().SetLabelSize(0.09)
  vFrame2.GetXaxis().SetTitleSize(0.15)
  vFrame2.GetYaxis().CenterTitle()
  vFrame2.GetXaxis().SetLabelSize(0.12)
  vFrame2.GetXaxis().SetNdivisions(809)
  vFrame2.GetYaxis().SetNdivisions(403)
  histtmpCEN.Draw("same")
  histtmpFOR.Draw("same")
  histtmpGEN.Draw("same")
  histtmpCEN.SetLineStyle(1)
  histtmpFOR.SetLineStyle(2)
  histtmpGEN.SetLineStyle(3)
  
  
  l2= TLegend(0.2067862,0.6705882,0.3668374,0.9529412)
  l2.SetTextSize(0.090925)
  l2.SetLineColor(0)
  l2.SetShadowColor(0)
  l2.SetLineStyle(1)
  l2.SetLineWidth(2)
  l2.SetFillColor(0)
  l2.SetFillStyle(0)
  l2.SetMargin(0.35)
  l2.AddEntry(histtmpFOR, "Reco weight (|#eta|>1.3)","l")
  l2.AddEntry(histtmpCEN, "Reco weight (|#eta|#leq1.3)","l")
  l2.AddEntry(histtmpGEN, "Gen weight","l")
  

  l2.Draw("same")
  
  
  
  canv.Update()
  canvname = "ClosureTest_RecoMass.pdf"
  canv.SaveAs(canvname,"pdf")
  canv.SaveAs(canvname.replace("pdf","root"),"pdf")
  
  #============ plot generated puppi+softdrop mass with correction ===============================
  
  yTitle = "Arbitrary scale"
   
  canv4 = getCanvas()
  canv4.cd()
  
  
  histosGenCorr   =[]
  
  for filetmp in filelist:
      histosGenCorr.append(filetmp.Get("GenAK8SoftdropMass_CORR"))
  
  setmax = histosGenCorr[0].GetMaximum()*2.0
  vFrame = canv4.DrawFrame(40.,0.000005,120.,setmax)  
  vFrame.SetXTitle("PUPPI softdrop mass")
  vFrame.SetYTitle(yTitle)
  vFrame.GetXaxis().SetTitleSize(0.06)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.05)
  vFrame.GetYaxis().SetTitleSize(0.06)
  #vFrame.GetYaxis().SetTitleOffset(1.0)
  vFrame.GetYaxis().SetLabelSize(0.05)
  vFrame.GetXaxis().SetNdivisions(408)
  vFrame.GetYaxis().SetNdivisions(404)
  j=0
  for h in histosGenCorr:
      h.Draw("HISTsame")
      #h.Scale(1./h.Integral())
      h.SetLineColor(col.GetColor(palette[j]))
      h.SetLineWidth(2)
      j+=1
  l1.Draw("same")
  li = get_line(80.4,80.4,0.,0.13,1)
  li.Draw("same")
  canv4.Print("Closure_puppiSoftdropgenCorr.pdf")
  
  
  
  
  
    
  time.sleep(10)
