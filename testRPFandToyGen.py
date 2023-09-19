from TwoDAlphabet.twoDalphabet import MakeCard, TwoDAlphabet
from TwoDAlphabet.alphawrap import BinnedDistribution, ParametricFunction, SemiParametricFunction
import ROOT

# Load up a previous workspace with fits already performed
twoD = TwoDAlphabet('THfits_LP_CR','THfits_LP_CR/runConfig.json',findreplace={},loadPrevious=True)

# The new function saves the transfer function shapes (in the original input binning) to a
# new ROOT file, and returns the histograms themselves for use.
#rpf_dict = twoD.GetTransferFunctionShapes(binName='default',rpfOpts=_rpf_options)
rpf_data = ROOT.TFile.Open('THfits_LP_CR/RPF_data.root')
rpl = rpf_data.Get('b_2x1')

# Now we produce a pseudo-data toy in the SR.
# First, declare which regions we want to create a toy for. 
regions = ['SR_loose','SR_pass'] 
# Note that these regions may not be included in the TwoDAlphabet's configuration JSON, 
# but do exist in the input datasets as histograms. As such, we need to do a quick find-and-replace
findreplace = {'CR_loose':'SR_loose', 'CR_pass':'SR_pass'}
# We also need to tell the toy generation method which postfit transfer function to use to produce the QCD estimate 
# in all the non-fail regions. In this case, we are only fitting Loose -> Pass, so there should only be one function
rpfs = [rpl]
# Now we can pass this all to the toy generation method, which will output a root file containing the histograms for:
# 	- SR_loose (we want this to be blinded for now, since it's not entirely signal-free)
#	- SR_pass
twoD.MakePseudoData(regions, rpfs, findreplace, blindFail=True)

