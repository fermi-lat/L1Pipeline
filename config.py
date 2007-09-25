#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

mode = False
if not mode:
    try:
        mode = os.environ['PIPELINE_MODE']
    except KeyError:
        print >> sys.stderr, 'PIPELINE_MODE not set.'
        pass
    pass
if not mode:
    try:
        pfa = os.environ['PIPELINE_FROMADDRESS']
        mode = pfa.split('@')[0].split('-')[1]
    except KeyError:
        print >> sys.stderr, 'PIPELINE_FROMADDRESS not set.'
        pass
    pass
if not mode:
    mode = 'dev'
    pass
mode = mode.lower()
if mode in ['prod']:
    testMode = False
else:
    testMode = True
    pass
print >> sys.stderr, "Test mode: %s" % testMode

L1Version = "1.18"
installRoot = "/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/SC/L1Pipeline"
L1ProcROOT = os.path.join(installRoot, L1Version)
L1Xml = os.path.join(L1ProcROOT, 'xml')

LATCalibRoot = '/afs/slac/g/glast/ground/releases/calibrations/'
L1Cmt = os.path.join(installRoot, 'builds')

L1Disk = '/nfs/farm/g/glast/u40/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

if testMode: L1Dir = os.path.join(L1Dir, 'test')

afsStage = "/afs/slac/g/glast/ground/PipelineStaging"

#maxCrumbSize = 48000 # SVAC pipeline uses this
#maxCrumbSize = 250   # tiny
#maxCrumbSize = 6353   # ~.5Hr on tori (muons).  Also about half of (old) medium q limit
maxCrumbSize = 17000   # ~.5Hr on cob (skymodel).
minCrumbCpuf = 7

glastRoot = '/afs/slac.stanford.edu/g/glast'
groundRoot = os.path.join(glastRoot, 'ground')
glastSetup = os.path.join(groundRoot, 'scripts', 'group.sh')
#
cmtConfig = 'rh9_gcc32opt'
installArea = os.path.join(L1Cmt, 'InstallArea', cmtConfig)
installBin = os.path.join(installArea, 'bin')
#
glastExt = os.path.join(groundRoot, 'GLAST_EXT', cmtConfig)
#
releaseDir = os.path.join(groundRoot, 'releases', 'volume07')
glastVersion = 'v12r5'
releaseName = 'GlastRelease'
gleamPackage = 'Gleam'
#
glastName = '-'.join((releaseName, glastVersion))
glastLocation = os.path.join(releaseDir, glastName)
gleam = os.path.join(glastLocation, 'bin', gleamPackage)
cmtScript = os.path.join(glastLocation, releaseName, glastVersion, 'cmt',
                         'setup.sh') # do we need this?
#
digiOptions = os.path.join(L1ProcROOT, 'digi.jobOpt')
reconOptions = os.path.join(L1ProcROOT, 'recon.jobOpt')

rootSys = os.path.join(glastExt, 'ROOT/v5.14.00g/root')
haddRootSys = rootSys
hadd = os.path.join(glastExt, haddRootSys, 'bin', 'hadd')


isoc = '/afs/slac/g/glast/isoc/flightOps'
isocPlatform = os.popen(os.path.join(isoc, 'isoc-platform')).readline().strip()
isocBin = os.path.join(isoc, isocPlatform, 'ISOC_PROD/bin')

ST="/nfs/farm/g/glast/u30/builds/rh9_gcc32opt/ScienceTools/ScienceTools-v9r2"
PFILES="."
stBinDir = os.path.join(ST, 'bin')

cmtPath = ':'.join((L1Cmt, glastLocation, glastExt, ST))
os.environ['CMTPATH'] = cmtPath

packages = {
    'configData': {
        'repository': '',
        'version': 'v0r2p6',
        },
    'Common': {
        'repository': 'dataMonitoring',
        'version': 'v2r1p0',
        },
    'FastMon': {
        'repository': 'dataMonitoring',
        'version': 'v2r1p1',
        },
    'Monitor': {
        'repository': 'svac',
        'version': 'dp20070728',
        },
    'TestReport': {
        'repository': 'svac',
        'version': 'v3r7p4',
        },
    'EngineeringModelRoot': {
        'repository': 'svac',
        'version': 'v3r1p2',
        },
    'pipelineDatasets': {
        'repository': 'users/richard',
        'version': 'v0r4',
        },
    'ft2Util': {
        'repository': '',
        'version': 'v1r1p6',
        },
    }

# fill in standard values for standard packages
for packName in packages:
    package = packages[packName]
    packages[packName]['root'] = os.path.join(L1Cmt, packName, package['version'])
    package['bin'] = os.path.join(package['root'], cmtConfig)
    package['cmtDir'] = os.path.join(package['root'], 'cmt')
    package['setup'] = os.path.join(package['cmtDir'], 'setup.sh')
    package['checkOutName'] = os.path.join(package['repository'], packName)
    continue

# add nonstandard package info
packages['Common']['python'] = os.path.join(packages['Common']['root'], 'python')

packages['EngineeringModelRoot']['app'] = os.path.join(packages['EngineeringModelRoot']['bin'], 'RunRootAnalyzer.exe')

packages['ft2Util']['app'] = os.path.join(packages['ft2Util']['bin'], 'makeFT2Entries.exe')

packages['FastMon']['app'] = os.path.join(packages['FastMon']['root'],
                                          'python', 'pDataProcessor.py')
packages['FastMon']['env'] = {
    'XML_CONFIG_DIR': os.path.join(packages['FastMon']['root'], 'xml'),
    }
packages['FastMon']['extraSetup'] = 'eval `/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/isoc isoc_env --add-env=flightops --add-env=root`'

packages['Monitor']['app'] = os.path.join(packages['Monitor']['bin'],
                                          'runStrip_t.exe')
packages['Monitor']['configDir'] = os.path.join(packages['Monitor']['root'],
                                                'src')
packages['Monitor']['trendMerge'] = os.path.join(packages['Monitor']['bin'],
                                                 'treemerge.exe')

packages['TestReport']['app'] = os.path.join(packages['TestReport']['bin'],
                                             'TestReport.exe')
packages['TestReport']['mergeApp'] = os.path.join(packages['TestReport']['bin'],
                                                  'MergeHistFiles.exe')


apps = {
    'digi': gleam,
    'digiMon': packages['TestReport']['app'],
    'digiEor': packages['Monitor']['app'],
    'fastMon': packages['FastMon']['app'],
    'makeFT2': packages['ft2Util']['app'],
    'makeFT1': os.path.join(stBinDir, 'makeFT1'),
    'recon': gleam,
    'reconMon': packages['TestReport']['app'],
    'reportMerge': packages['TestReport']['mergeApp'],
    'svacTuple': packages['EngineeringModelRoot']['app'],
    'trendMerge': packages['Monitor']['trendMerge']
    }

monitorOptions = {
    'digiEor': os.path.join(packages['Monitor']['configDir'],
                            'monconfig_digi_v24_histos.xml'),
    'digiTrend': os.path.join(packages['Monitor']['configDir'],
                              'monconfig_digi_v24_trending.xml'),
    'reconEor': os.path.join(packages['Monitor']['configDir'],
                             'monconfig_recon_v2_histos.xml'),
    'reconTrend': os.path.join(packages['Monitor']['configDir'],
                               'monconfig_recon_v2_trending.xml'),
    }

monitorOutFiles = {
    'fastMon': 'FASTMON',
    'digiEor': 'DIGIHIST',
    'digiTrend': 'tripe',
    'reconEor': 'RECONHIST',
    'reconTrend': 'tripe',
    }

mergeConfigs = {
    'digiEor': os.path.join(packages['Monitor']['configDir'],
                            'MergeHistos_e2e_digi.txt'),
    'digiMon': os.path.join(L1ProcROOT, 'merge_digi.txt'),
    'fastMon': os.path.join(L1ProcROOT, 'fast_mon_config.txt'),
    'reconEor': os.path.join(packages['Monitor']['configDir'],
                             'MergeHistos_e2e_recon.txt'),
    'reconMon': os.path.join(L1ProcROOT, 'merge_recon.txt'),
    }

tdBin = 15

ingestor = {
    'digiTrend': '/afs/slac.stanford.edu/g/glast/ground/bin/ingestDigiTrending',
    'reconTrend': '/afs/slac.stanford.edu/g/glast/ground/bin/ingestRecoTrending',
    }

joiner = '*'

rootPath = os.path.join(rootSys, 'lib')
#xercesPath = ':'.join([glastExt, 'xerces/2.7.0/lib'])
#mysqlPath = ':'.join([glastExt, 'MYSQL/4.1.18/lib/mysql'])
clhepPath = os.path.join(glastExt, 'CLHEP/1.9.2.2/lib')
cppunitPath = os.path.join(glastExt, 'cppunit/1.10.2/lib')

libraryPath = ':'.join((os.path.join(L1Cmt, 'lib'), \
                        os.path.join(glastLocation, 'lib'), \
                        rootPath, clhepPath, cppunitPath))
#                        rootPath, xercesPath, mysqlPath))

#gplPath = '/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/GPLtools/prod/python'
GPL2 = '/nfs/slac/g/svac/focke/builds/GPLtools/dev'
gplPath = os.path.join(GPL2, 'python')

pythonPath = ':'.join([L1ProcROOT, rootPath, gplPath,
                       packages['Common']['python']])

# LSF stuff
# allocationGroup = 'glastdata' # don't use this anymore, policies have changed
# allocationGroup="%(allocationGroup)s" # ripped from XML template
#
quickQueue = 'express'
reconQueue = 'medium'
#standardQueue = 'glastdataq'
standardQueue = 'long'
slowQueue = 'xlong'
#
reconMergeScratch = " -R &quot;select[scratch&gt;70]&quot; "
reconCrumbCpuf = " -R &quot;select[cpuf&gt;%s]&quot; " % minCrumbCpuf

if __name__ == "__main__":
    print L1Dir
    print reconApp
    
