#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
xrdcp root://cmseos.fnal.gov//store/user/ammitra/CMSSW_10_6_14_env.tgz env_tarball.tgz
export SCRAM_ARCH=slc7_amd64_gcc700
scramv1 project CMSSW CMSSW_10_6_14
tar -xzf env_tarball.tgz
rm env_tarball.tgz

mkdir tardir; cp THfits_LP_CR_TprimeB-1800-125-0x1_area_gof_toys_input.tgz tardir/; cd tardir
tar -xzvf THfits_LP_CR_TprimeB-1800-125-0x1_area_gof_toys_input.tgz
rm THfits_LP_CR_TprimeB-1800-125-0x1_area_gof_toys_input.tgz
cp -r * ../CMSSW_10_6_14/src/
cd ../
cd CMSSW_10_6_14/src/; eval `scramv1 runtime -sh`
cd THfits_LP_CR/TprimeB-1800-125-0x1_area
echo $*
$*
cd $CMSSW_BASE/src/

tar -czvf THfits_LP_CR_TprimeB-1800-125-0x1_area_gof_toys_output_${CONDOR_ID}.tgz THfits_LP_CR/TprimeB-1800-125-0x1_area/higgsCombine_gof_toys.GoodnessOfFit.mH120.*.root
cp THfits_LP_CR_TprimeB-1800-125-0x1_area_gof_toys_output_${CONDOR_ID}.tgz $CMSSW_BASE/../
