#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
import registerPrep

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

fileType = 'ls3'

stSetup = config.stSetup
app = config.apps['makeLS3']

realFt1File = fileNames.fileName('extendedFT1', dlId, runId)
stagedFt1File = staged.stageIn(realFt1File)
realFt2File = fileNames.fileName('ft2', dlId, runId)
stagedFt2File = staged.stageIn(realFt2File)

realLs3File = fileNames.fileName(fileType, dlId, runId, next=True)
stagedLs3File = staged.stageOut(realLs3File)

workDir = os.path.dirname(stagedLs3File)

version = fileNames.version(realLs3File)

instDir = config.ST
glastExt = config.glastExt

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s 
source %(stSetup)s
%(app)s evfile=%(stagedFt1File)s scfile=%(stagedFt2File)s outfile=%(stagedLs3File)s dcostheta=0.025 binsz=1 file_version=%(version)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, realLs3File)

sys.exit(status)
