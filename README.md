# Installation
Ensure that you have SSH keys installed
```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_xyz
```
Setup CMSSW
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_14
cd CMSSW_10_6_14/src
cmsenv
```
Setup 2DAlphabet
```
cd ~/public/CMSDAS2023/CMSSW_10_6_14/src/
git clone --branch binningFloatFix https://github.com/ammitra/2DAlphabet.git
git clone --branch 102x https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
curl -s https://raw.githubusercontent.com/lcorcodilos/CombineHarvester/master/CombineTools/scripts/sparse-checkout-ssh.sh | bash
scram b clean; scram b -j 8
cmsenv
```
Virtual env
```
python -m virtualenv twoD-env
source twoD-env/bin/activate
cd 2DAlphabet
python setup.py develop
```
Test that everything works
```
python
>>> import ROOT
>>> r = ROOT.RooParametricHist()
```
Then clone this repository to the `CMSSW_10_6_14/src/` directory. 

# Contents of this repository
* `rootfiles/` - contains the templates for ttbar, V+jets, and 1 signal mass point, both per-year and combined for Run2. The script to combine templates for Run2 is `rootfiles/combine_run2.py`
* `LP.json`, `LP.py` - scripts for generating the control region fits, whose results are in `THfits_LP_CR/`
* `SR.json`, `SR.py` - scripts for generating the (toy) signal region fits. Results stored in `THfits_LP_SR/`
* `testRPFandToyGen.py` - script to generate a pseudo-data toy of the SR using the transfer functions derived in the control region. One can either run the RPF plotting command in line 10, or run it separately, open the ROOT file containing the RPFs, and select the desired RPF manually. This script will produce a file `PseudoDataToy.root`, which will have to be referenced in the JSON file for any fits using the toy. 
* `test_rpf_plotting.py` - script to generate the postfit transfer function shapes for both b-only and s+b fits. It will produce a file `RPF_data.root` in the base directory of the 2DAlphabet workspace of the fit you selected in the script. 
* `perYear/` contains the scripts to run fits using the per-year templates instead of the combined run2 templates. 

