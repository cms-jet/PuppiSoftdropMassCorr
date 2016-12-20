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
 colors = ['#762a83','#de77ae','#a6dba0','#92c5de','#4393c3','#2166ac','#053061','#40004b','#762a83','#9970ab','#de77ae']
 colors = ['#FF420E','#80BD9E','#a6dba0','#92c5de','#4393c3','#2166ac','#053061','#40004b','#762a83','#9970ab','#de77ae''#40004b','#762a83','#9970ab']

 for c in colors:
  palette['gv'].append(c)
 
 return palette[mode]
 
palette = get_palette('gv')
col = TColor()

#masses = [1000,1200,1400,1600,1800,2000,2500,3000,4000,4500]  
#masses = [600,800,1000,1200,1400,1800,2000,2500,3000,3500,4000,4500] #Ops!! 400 masspoint is named for convenience and is actually SM WW, not signal sample!
#masses = [600,1000,1200,1400,1800,2000,3000,3500,4000,4500]
masses = [600,1000,1200,2000,2500,3000] # BulkWW
masses = [600,1000,1200,2000,2500,3000,3500] # WprimeWZ
masses = [600,1000,1200,1400,1800,2000,3000,3500,4000,4500] #ZprimeWW
if options.fitGenMass:
  masses = [400,600,800,1000,1200,1400,1800,2500,3000,4000,4500]
  masses = [600,1000,1200,1400,1800,2000,3000,3500,4000,4500]
  masses = [600,1000,1200,2000,2500,3000]
  masses = [600,1000,1200,1400,1800,2000,3000,3500,4000,4500]
  #masses = [600,800,1800,2000,2500,3500,4500] #Wprime
  
hCentral = 'gen_SoftdropMass_eta1v3'
hForward = 'gen_SoftdropMass_etaUP1v3'

if options.doMassShiftFit:
  hCentral = 'massShift_softdrop_eta1v3'
  hForward = 'massShift_softdrop_etaUP1v3'
  
if options.doPruning:
  hCentral = 'massShift_pruning_eta1v3'
  hForward = 'massShift_pruning_etaUP1v3'
  options.doMassShiftFit = True
  

if options.fitGenMass:
  hCentral = 'GenAK8SoftdropMass_eta1v3'
  hForward = 'GenAK8SoftdropMass_etaUP1v3'
  if options.doPruning:
    hCentral = 'GenAK8PrunedMass_eta1v3'
    hForward = 'GenAK8PrunedMass_etaUP1v3'
    options.doMassShiftFit = False

      
  
lineStyle = [1,1,1,1,3,3,3,3]


signals = ["BulkWW","BulkZZ","ZprimeWW","WprimeWZ"]
signals = [ "ZprimeWW"]
ptsCEN = []

for signal in signals:
 
  filelist = []
  histosCEN = []
  histosFOR = []
  fits = []
  
  l = TLegend(0.7650754,0.7564767,0.8065327,0.876943)
  if options.fitGenMass or options.doMassShiftFit: l = TLegend(0.7650754,0.7564767,0.8065327,0.876943)
  l.SetTextSize(0.035)
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
  
  # if options.fitGenMass:
  #   meansCentral.append(82.20)
  #   meanErrCentral.append(0.06)
  #   ptsCEN.append(200)
  #   ptErrCEN.append(0.73)
    
  
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
    histtmpC.SetName("Central%i"%masspoints[i])
    # histtmp.Scale(1./histtmp.Integral())
    maxbin=0
    maxcontent=0
    startbin = 60.
    if options.doMassShiftFit: startbin = -0.4
    for b in range(histtmpC.GetXaxis().GetNbins()):
      if histtmpC.GetXaxis().GetBinCenter(b+1) > startbin and histtmpC.GetBinContent(b+1)>maxcontent:
        maxbin = b
        maxcontent = histtmpC.GetBinContent(b+1)   
    tmpmean = histtmpC.GetXaxis().GetBinCenter(maxbin)  
    tmpwidth = 15.
    if options.doMassShiftFit: tmpwidth = 0.8    
    if options.fitGenMass: tmpwidth = 7.0    
    g1 = TF1("g1CEN%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpC.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    if options.fitGenMass and masspoints[i] >= 3000:
      tmpwidth = tmpwidth*1.5
    g1 = TF1("g1CEN%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpC.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    if options.fitGenMass and masspoints[i] >= 3000:
      tmpwidth = tmpwidth*1.5
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
    # histtmp.Scale(1./histtmp.Integral())
    maxbin=0
    maxcontent=0
    startbin = 60.
    if options.doMassShiftFit: startbin = -0.4
    for b in range(histtmpF.GetXaxis().GetNbins()):
      if histtmpF.GetXaxis().GetBinCenter(b+1)>startbin and histtmpF.GetBinContent(b+1)>maxcontent:
        maxbin = b
        maxcontent = histtmpF.GetBinContent(b+1)
    tmpmean = histtmpF.GetXaxis().GetBinCenter(maxbin)
    tmpwidth = 15.
    if options.doMassShiftFit: tmpwidth = 0.8    
    if options.fitGenMass: tmpwidth = 7.0    
    g1 = TF1("g1FOR%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpF.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    if options.fitGenMass and masspoints[i] >= 3000:
      tmpwidth = tmpwidth*1.5
    g1 = TF1("g1FOR%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpF.Fit(g1, "SR")
    tmpmean = g1.GetParameter(1)
    tmpwidth = g1.GetParameter(2)
    if options.fitGenMass and masspoints[i] >= 3000:
      tmpwidth = tmpwidth*1.5
    if options.doMassShiftFit and masspoints[i] >= 4000:
      tmpwidth = tmpwidth*1.5
    
    g1 = TF1("g1FOR%i"%masspoints[i],"gaus", tmpmean-tmpwidth,tmpmean+tmpwidth)
    histtmpF.Fit(g1, "SR");
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
    
  
  postfix = "_recoMass"
  if options.doMassShiftFit: postfix = "_masshift"
  if options.fitGenMass: postfix = "_genMass"
  filename = "AllFits%s"%postfix
  f = TFile("%s.root"%filename,  "RECREATE")
  print "Writing to file " ,f.GetName()
  
  l1= TLegend(0.7650754,0.5564767,0.8065327,0.876943)
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
    if histosCEN[j].Integral()>0:
        histosCEN[j].Scale(1./histosCEN[j].Integral())
    if histosFOR[j].Integral()>0:
        histosFOR[j].Scale(1./histosFOR[j].Integral())
    histosCEN[j].SetLineColor(col.GetColor(palette[j]))
    histosCEN[j].SetLineWidth(2)
    histosCEN[j].Rebin(1) 
    histosFOR[j].SetLineColor(col.GetColor(palette[j]))
    histosFOR[j].SetLineWidth(2)
    histosFOR[j].Rebin(1)
    l1.AddEntry(histosCEN[j], "M = %i"%masspoints[j],"l")
    
  f.Close()  

      
  canv = getCanvas()
  canv.cd()
  yTitle = "Arbitrary scale"
   
  canv = getCanvas()
  canv.cd()
  setmax = histosCEN[0].GetMaximum()*2.0
  fxmin = 20.
  fxmax = 140.
  fymin = 0.000005
  fymax = setmax
  if options.doMassShiftFit:
      fxmin = -1.
      fxmax =1.
  vFrame = canv.DrawFrame(fxmin,fymin,fxmax,fymax)  
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
  for h in histosCEN: 
    h.Draw("HISTsame")
  l1.Draw("same")
  li = get_line(80.4,80.4,0.,0.13,1)
  li.Draw("same")
  
  canvname = "RecoPuppiSoftdropMass"
  if options.doMassShiftFit: canvname = "MassShift"
  if options.doPruning: canvname = "recoPrunedMass"
  if options.fitGenMass: canvname = "GenSoftdropMass"
  canv.Print(canvname+"_CEN.pdf")
  
  fxmin = 40.
  fxmax = 120.
  fymin = 0.000005
  fymax = setmax
  if options.doMassShiftFit:
      fxmin = -1.
      fxmax =1.
  
  canv = getCanvas()
  canv.cd()
  setmax = histosFOR[0].GetMaximum()*2.0
  vFrame = canv.DrawFrame(fxmin,fymin,fxmax,fymax)  
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
  canv.Print(canvname+"_FOR.pdf")
  time.sleep(10)
  del canv
  
  
  
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
  # if not options.fitGenMass and not options.doMassShiftFit:
 #    canv.Divide(1,2,0,0,0)
 #    canv.cd(1)
 #    p11_1 = canv.GetPad(1)
 #    p11_1.SetPad(0.01,0.20,0.99,0.98)
 #    p11_1.SetRightMargin(0.05)
 #    p11_1.SetTopMargin(0.05)
 #    p11_1.SetFillColor(0)
 #    p11_1.SetBorderMode(0)
 #    p11_1.SetFrameFillStyle(0)
 #    p11_1.SetFrameBorderMode(0)
  vFrame = canv.DrawFrame(200,65.,2200,85.)
  if signal.find("WprimeWZ")!=-1:
      vFrame = canv.DrawFrame(200,75.,2200,95.)
  vFrame.SetYTitle("<m>_{m_{reco}} (GeV)")
  if options.fitGenMass:
    vFrame = canv.DrawFrame(200,70.,2200,90.)
    if signal.find("WprimeWZ")!=-1:
      vFrame = canv.DrawFrame(200,75.,2200,95.)
    vFrame.SetYTitle("<m>_{m_{gen}} (GeV)")
  if options.doMassShiftFit:
    vFrame = canv.DrawFrame(200,-0.3,2200,0.1)
    vFrame.SetYTitle("(m_{reco} - m_{gen})/m_{reco}")
  vFrame.SetXTitle("p_{T} (GeV)")
  vFrame.GetXaxis().SetTitleSize(0.06)
  vFrame.GetXaxis().SetTitleOffset(0.95)
  vFrame.GetXaxis().SetLabelSize(0.05)
  vFrame.GetYaxis().SetTitleSize(0.06)
  vFrame.GetYaxis().SetTitleOffset(1.2)
  vFrame.GetYaxis().SetLabelSize(0.05)
  vFrame.GetXaxis().SetNdivisions(809)
  vFrame.GetYaxis().SetNdivisions(908)
  if options.doMassShiftFit:vFrame.GetYaxis().SetNdivisions(707)
  gCEN.SetMarkerSize(1.6)
  gFOR.SetMarkerSize(1.6)
  gCEN.SetMarkerStyle(20)
  gFOR.SetMarkerStyle(20)
  gCEN.SetMarkerColor(col.GetColor(palette[0]))
  gFOR.SetMarkerColor(col.GetColor(palette[1]))
  filetmp = TFile.Open(prefix+"/ExoDiBosonAnalysis.BulkWW_13TeV_2000GeV.VV.root","READ")
  histtmpCEN = TProfile(filetmp.Get("gen_chsJEC_eta1v3"))
  histtmpFOR = TProfile(filetmp.Get("gen_chsJEC_etaUP1v3"))
  histtmpCEN.SetMarkerSize(1.6)
  histtmpFOR.SetMarkerSize(1.6)
  histtmpCEN.SetMarkerStyle(20)
  histtmpFOR.SetMarkerStyle(20)
  histtmpCEN.SetMarkerColor(col.GetColor(palette[0]))
  histtmpFOR.SetMarkerColor(col.GetColor(palette[1]))
  histtmpCEN.Draw("same")
  histtmpCEN.SetMaximum(80.)
  histtmpCEN.SetMinimum(65.)
  if options.doMassShiftFit:
    histtmpCEN.SetMaximum(1.)
    histtmpCEN.SetMinimum(-1.)
     
  histtmpFOR.Draw("same")
  gCEN.Draw("PLsame")
  gFOR.Draw("PLsame")
  l.AddEntry(gCEN, "|#eta|<1.3","p")
  l.AddEntry(gFOR, "|#eta|>1.3","p")
  
  addInfo = TPaveText(0.571608,0.5103627,0.7336683,0.7189119,"NDC")
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
  if not options.fitGenMass:
    if signal.find("BulkWW") != -1: addInfo.AddText("Bulk G #rightarrow WW")
    elif signal.find("BulkZZ") != -1: addInfo.AddText("Bulk G #rightarrow ZZ")
    elif signal.find("WprimeWZ") != -1: addInfo.AddText("W'#rightarrow WZ")
    elif signal.find("ZprimeWW") != -1: addInfo.AddText("Z' #rightarrow WW")     
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.040)
  addInfo.SetTextAlign(12)
  addInfo.AddText("AK, R= 0.8")
  addInfo.AddText("Uncorrected")
  addInfo.AddText("p_{T} > 200 GeV, |#eta| < 2.5")
  
  
  l.Draw("same")
  addInfo.Draw("same")
  # if not options.fitGenMass and not options.doMassShiftFit: CMS_lumi.CMS_lumi(p11_1, iPeriod, iPos)
  # else: CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
  CMS_lumi.CMS_lumi(canv, iPeriod, iPos)
  canv.Update()
  
  # if not options.fitGenMass and not options.doMassShiftFit:
  #   canv.cd(2)
  #   p11_2 = canv.GetPad(2)
  #   p11_2.SetPad(0.01,0.02,0.99,0.27)
  #   p11_2.SetBottomMargin(0.35)
  #   p11_2.SetRightMargin(0.05)
  #   p11_2.SetGridx()
  #   p11_2.SetGridy()
  #   vFrame2 = p11_2.DrawFrame(p11_1.GetUxmin(),1.04, p11_1.GetUxmax(), 1.09)
  #   vFrame2.SetXTitle("p_{T} (GeV)")
  #   vFrame2.SetYTitle("CHS L2L3")
  #   vFrame2.GetXaxis().SetTitleSize(0.06)
  #   vFrame2.GetYaxis().SetTitleSize(0.15)
  #   vFrame2.GetYaxis().SetTitleOffset(0.40)
  #   vFrame2.GetYaxis().SetLabelSize(0.09)
  #   vFrame2.GetXaxis().SetTitleSize(0.15)
  #   # vFrame2.GetXaxis().SetTitleOffset(0.90)
  #   vFrame2.GetXaxis().SetLabelSize(0.12)
  #   vFrame2.GetXaxis().SetNdivisions(809)
  #   vFrame2.GetYaxis().SetNdivisions(403)
  
  
  
  histtmpCEN.Draw("same")
  histtmpFOR.Draw("same")
  canv.Update()
  canvname = "RecoPuppiSoftdropMass_vspt.pdf"
  if options.doMassShiftFit: canvname = "MassShift_vspt.pdf"
  if options.doPruning: canvname = "recoPrunedMass_vspt.pdf"
  if options.fitGenMass: canvname = "GenSoftdropMass_vspt.pdf"
  canv.SaveAs(canvname,"pdf")
  canv.SaveAs(canvname.replace("pdf","root"),"pdf")
  
  
  if options.fitGenMass or options.doMassShiftFit:
    # vyCEN.append(vyCEN[0])
    # errCEN.append(errCEN[0])
    # vyFOR.append(vyFOR[0])
    # errFOR.append(errFOR[0])
    # vxCEN.append(200.)
    # vxErrCEN.append(vxErrCEN[0])
    # vxFOR.append(200.)
    # vxErrFOR.append(vxErrFOR[0])
    
    vyCEN.append(vyCEN[-1])
    errCEN.append(errCEN[-1])  
    vyCEN.append(vyCEN[-1])
    errCEN.append(errCEN[-1])
    vyCEN.append(vyCEN[-1])
    errCEN.append(errCEN[-1])
    
    vyFOR.append(vyFOR[-1])
    errFOR.append(errFOR[-1])
    vyFOR.append(vyFOR[-1])
    errFOR.append(errFOR[-1])
    vyFOR.append(vyFOR[-1])
    errFOR.append(errFOR[-1])
    vyFOR.append(vyFOR[-1])
    errFOR.append(errFOR[-1])
   
    
    vxCEN.append(2500.)
    vxErrCEN.append(vxErrCEN[-1])
    vxCEN.append(3000.)
    vxErrCEN.append(vxErrCEN[-1])
    vxCEN.append(3200.)
    vxErrCEN.append(vxErrCEN[-1])
    
    vxFOR.append(1500.)
    vxErrFOR.append(vxErrFOR[-1])
    vxFOR.append(2000.)
    vxErrFOR.append(vxErrFOR[-1])
    vxFOR.append(3000.)
    vxErrFOR.append(vxErrFOR[-1])
    vxFOR.append(3200.)
    vxErrFOR.append(vxErrFOR[-1])
    
    nvyCEN  = np.array(vyCEN)
    nerrCEN = np.array(errCEN)
    if options.fitGenMass:
      nvyCEN = 80.4/nvyCEN
      # nerrCEN = nerrCEN/80.4
      nerrCEN = nvyCEN*0.005 #Try 0.5% error on all points
      # nerrCEN[0] = nvyCEN[0]*0.1
    elif options.doMassShiftFit:
      nvyCEN  = -1*(nvyCEN - 1)
      # nerrCEN = nerrCEN
      nerrCEN = nvyCEN*0.005 #Try 0.5% error on all points
      # nerrCEN[0] = nvyCEN[0]*0.1
    nnvyCEN = array("f",nvyCEN)
    nnerrCEN = array("f",nerrCEN)
    
    nvyFOR  = np.array(vyFOR)
    nerrFOR = np.array(errFOR)
    if options.fitGenMass:
      nvyFOR = 80.4/nvyFOR
      # nerrFOR = nerrFOR/80.4
      nerrFOR = nvyFOR*0.005 #Try 0.5% error on all points
      # nerrFOR[0] = nvyFOR[0]*0.1
    elif options.doMassShiftFit:
      nvyFOR  = -1*(nvyFOR-1)
      nerrFOR = nvyFOR*0.005 #Try 0.5% error on all points
      # nerrFOR[0] = nvyFOR[0]*0.1
    nnvyFOR = array("f",nvyFOR)
    nnerrFOR = array("f",nerrFOR)

    gC_forCorr = TGraphErrors(len(vxCEN),vxCEN,nnvyCEN,vxErrCEN,nnerrCEN)
    gC_forCorr.SetName("gC_forCorr")
    gF_forCorr = TGraphErrors(len(vxFOR),vxFOR,nnvyFOR,vxErrFOR,nnerrFOR)
    gF_forCorr.SetName("gF_forCorr")
    
    filename = "input/genCorr"
    if options.doMassShiftFit: filename = "input/recoCorr"
    f = TFile("%s.root"%filename,  "RECREATE")
    gC_forCorr.Write()
    gF_forCorr.Write()
    f.Close()
  time.sleep(15)
  del canv
