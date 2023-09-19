from TwoDAlphabet import plot
from TwoDAlphabet.twoDalphabet import MakeCard, TwoDAlphabet
from TwoDAlphabet.alphawrap import BinnedDistribution, ParametricFunction
from TwoDAlphabet.helpers import make_env_tarball, cd, execute_cmd
import ROOT

'''
Script designed to debug CR fits by fitting RRatio on top of data-nominalMC RPL
'''

def _select_signal(row, args):
    signame = args[0]
    poly_order = args[1]
    if row.process_type == 'SIGNAL':
        if signame in row.process:
            return True
        else:
            return False
    elif 'Multijet' in row.process:
        if row.process == 'Multijet_'+poly_order:
            return True
        elif row.process == 'Multijet':
            return True
        else:
            return False
    else:
        return True

# try out a few RRatios
_rratio_options = {
    '0x0': {
        'form': '(@0)',
        'constraints': {"MIN":-500,"MAX":500}
    },
    '1x1': {
        'form': '(@0+@1*x)*(@2+@3*y)',
        'constraints': {"MIN":-500,"MAX":500}
    },
    '2x1': {
        'form': '(@0+@1*x+@2*x**2)*(@3+@4*y)',
        'constraints': {"MIN":-500,"MAX":500}
    }
}

# Construct a workspace for the fits
twoD = TwoDAlphabet('THfits_RRatio_CR','LP.json',loadPrevious=False)
qcd_hists = twoD.InitQCDHists() # get the data-nominalMC histos for each region
CR_l = qcd_hists['CR_loose']
CR_p = qcd_hists['CR_pass']

# Now, re-bin them with the binning used in the fits
binning, _ = twoD.GetBinningFor('CR_loose')
qcd_l = BinnedDistribution('Multijet_CR_loose', CR_l, binning, constant=True)
qcd_p = BinnedDistribution('Multijet_CR_pass', CR_p, binning, constant=True)

# Make a new BinnedDistribution object of their quotient - this is the pass-to-loose ratio
mc_rpl = qcd_p.Divide('Multijet_CR_RPL', qcd_l)
# we can also quickly check that these distributions actually make sense...
h_mcrpl, _ = mc_rpl.PlotDistribution()
h_qcdl, _ = qcd_l.PlotDistribution() # should be the same plot as CR_l!
h_qcdp, _ = qcd_p.PlotDistribution() # should be the same plot as CR_p!
debug = ROOT.TFile.Open('debug_mc_rpl.root','RECREATE')
debug.cd()
CR_l.Write()
CR_p.Write()
h_mcrpl.Write()
h_qcdl.Write()
h_qcdp.Write()
debug.Close()

twoD.AddAlphaObj('Multijet','CR_loose',qcd_l,title='Multijet')
qcd_intermediate = qcd_l.Multiply('Multijet_LooseTimesRPL',mc_rpl)
for rratio, options in _rratio_options.items():
    qcd_rratio = ParametricFunction('CR_RRatio'+'_'+rratio, binning, options['form'], constraints=options['constraints'])
    qcd_pass = qcd_intermediate.Multiply('Multijet_CR_pass_'+rratio, qcd_rratio)
    twoD.AddAlphaObj('Multijet_'+rratio,'CR_pass',qcd_pass,title='Multijet')
twoD.Save()

# now fit these
for rratio in _rratio_options.keys():
    subset = twoD.ledger.select(_select_signal, 'TprimeB-1800-125', rratio)
    twoD.MakeCard(subset, 'TprimeB-1800-125-{}_area'.format(rratio))
    twoD.MLfit('TprimeB-1800-125-{}_area'.format(rratio),rMin=-1,rMax=5,verbosity=2,defMinStrat=1,extra='--robustFit 1')
    twoD.StdPlots('TprimeB-1800-125-{}_area'.format(rratio),subset)

# otherwise there will be a (harmless) segfault due to some weird garbage collection in 2DAlphabet's RooDataHists. Need to fix.. 
del twoD
