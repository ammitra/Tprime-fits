from TwoDAlphabet.twoDalphabet import *

def _generate_constraints(nparams):
    out = {}
    for i in range(nparams):
        if i == 0:
            out[i] = {"MIN":-50,"MAX":50}
        else:
            out[i] = {"MIN":-50,"MAX":50}
    return out

_rpf_options = {
    '0x0': {
        'form': '(@0)',
        'constraints': _generate_constraints(1)
    },
    '1x0': {
        'form': '(@0+@1*x)',
        'constraints': _generate_constraints(2)
    },
    '0x1': {
        'form': '(@0+@1*y)',
        'constraints': _generate_constraints(2)
    },
    '1x1': {
        'form': '(@0+@1*x)*(@2+@3*y)',
        'constraints': _generate_constraints(3)
    },
    '2x1': {
        'form': '(@0+@1*x+@2*x**2)*(@3+@4*y)',
        'constraints': _generate_constraints(4)
    },
    '2x2': {
        'form': '(@0+@1*x+@2*x**2)*(@3+@4*y*@5*y**2)',
        'constraints': _generate_constraints(4)
    }
}

# Load up a previous workspace with fits already performed 
twoD = TwoDAlphabet('THfits_LP_SR','THfits_LP_SR/runConfig.json',findreplace={},loadPrevious=True)

# The new function saves the transfer function shapes (in the original input binning) to a 
# new ROOT file, and returns the histogram itself for use. 
out = twoD.GetTransferFunctionShapes(binName='default',rpfOpts=_rpf_options)

