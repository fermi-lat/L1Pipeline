"""@brief Conventions for naming files.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

import config
import procDirs

headFields = 3

def baseHead(inFile):
    """@brief DEPRECATED

    Parses out the portion of a filename that does not depend on
    the file type.
    """

    inDir, inName = os.path.split(inFile)

    cut = inName.rindex('.')
    inBase = inName[:cut]
    allFields = inBase.split('_')

    goodFields = allFields[:headFields]
    head = '_'.join(goodFields)

    return head

def join(parts, ext):
    return '_'.join(parts) + '.' + ext


def setup(dlId, runId=None, chunkId=None, crumbId=None):
    """@brief Setup data directory names.

    @arg dlId The dowlink ID.

    @arg [runId] The run ID.

    @arg [chunkId] The chunk ID.

    @arg [crumbId] The crumb ID.

    @return A dictionary containing the names of various data files.
    
    """
    runHead = runId

    dirs = procDirs.setup(dlId, runId, chunkId, crumbId)
    files = {}
    files['run'] = {}

    files['dirs'] = 'dirs'

    files['downlink'] = {}
    files['downlink']['runList'] = os.path.join(dirs['downlink'], 'runList')

    if chunkId is not None:
        files['chunk'] = _setupChunk(dirs, chunkId, runHead)
        if crumbId is not None:
            files['crumb'] = _setupCrumb(dirs, crumbId, chunkHead)
            pass
        pass


    files['run']['digi'] = os.path.join(dirs['run'], \
                                      join(runHead, 'digi.root'))
    files['run']['digiMon'] = os.path.join(dirs['run'], \
                                      join(runHead, 'digiHist.root'))
    
    files['run']['recon'] = os.path.join(dirs['run'], \
                                       join(runHead, 'recon.root'))
    files['run']['merit'] = os.path.join(dirs['run'], \
                                       join(crumbHead, 'merit.root'))
    files['run']['cal'] = os.path.join(dirs['run'], \
                                       join(crumbHead, 'cal.root'))
    
    files['run']['reconMon'] = os.path.join(dirs['run'], \
                                      join(runHead, 'reconHist.root'))

    files['run']['svac'] = os.path.join(dirs['run'], \
                                      join(runHead, 'svac.root'))
    
    
    return files


def _setupChunk(dirs, chunkId, runHead):
    files = {}
    chunkHead = join(runHead, chunkId)
    files['digiChunk'] = os.path.join(dirs['chunk'], \
                                      join(chunkHead, 'digi.root'))
    files['digiMonChunk'] = os.path.join(dirs['chunk'], \
                                      join(chunkHead, 'digiHist.root'))
    
    files['reconChunk'] = os.path.join(dirs['chunk'], \
                                       join(chunkHead, 'recon.root'))
    files['meritChunk'] = os.path.join(dirs['chunk'], \
                                       join(crumbHead, 'merit.root'))
    files['calChunk'] = os.path.join(dirs['chunk'], \
                                       join(crumbHead, 'cal.root'))
    
    files['reconMonChunk'] = os.path.join(dirs['chunk'], \
                                      join(chunkHead, 'reconHist.root'))

    files['svacChunk'] = os.path.join(dirs['chunk'], \
                                      join(chunkHead, 'svac.root'))

    return files


def _setupCrumb(dirs, crumbId, chunkHead):
    files = {}
    crumbHead = join(chunkHead, crumbId)
    files['reconCrumb'] = os.path.join(dirs['crumb'], \
                                       join(crumbHead, 'recon.root'))
    files['meritCrumb'] = os.path.join(dirs['crumb'], \
                                       join(crumbHead, 'merit.root'))
    files['calCrumb'] = os.path.join(dirs['crumb'], \
                                       join(crumbHead, 'cal.root'))
    return files
