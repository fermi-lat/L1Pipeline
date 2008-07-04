#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Delete no-longer-needed directories and their contents.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import fileNames
import runner

status = 0

dlRawDir = os.environ['DOWNLINK_RAWDIR']
head, dlId = os.path.split(dlRawDir)
if not dlId: head, dlId = os.path.split(head)

runId = os.environ.get('RUNID')
if runId is not None:
    # runStatus = os.environ['RUNSTATUS']

    chunkId = os.environ.get('CHUNK_ID')
    if chunkId is not None:
        level = 'chunk'
    else:
        level = 'run'
        dlId = '*'
        pass

    # check if mergeStuff has supressed cleanup due to missing files
    runDir = fileNames.fileName(None, dlId, runId)
    lfBase = 'dontCleanUp'
    cleanupLock = os.path.join(runDir, lfBase)
    if os.path.exists(cleanupLock):
        print >> sys.stderr, '''Cleanup is supressed by %s''' % cleanupLock
        sys.exit(1)
        pass
    
else:
    level = 'downlink'

    # print >> sys.stderr, 'Not doing cleanup.'
    # sys.exit(0)
    
    chunkId = None
    pass

# This is harmful; the runStatus the halfPipe gave us is not reliable
# due to concurrency issues.
#
# # This decision should be made at a higher level.
# if level == 'run' and runStatus not in ['COMPLETE', 'INCOMPLETE']:
#     print >> sys.stderr, 'Run %s has status %s, not deleting chunks.' \
#           % (runId, runStatus)
#     sys.exit(0)
#     pass

goners = fileNames.findPieces(None, dlId, runId, chunkId)

if level == 'downlink':
    if config.saveDl:
        dlStorage = config.dlStorage
        cmd = 'mv %(dlRawDir)s %(dlStorage)s' % locals()
        status |= runner.run(cmd)
    else:
        goners.append(dlRawDir)
        pass
    pass
elif level == 'run':
    goners.append(fileNames.tokenDir(head, runId))
    pass

totG = len(goners)
for ig, goner in enumerate(goners):
    if config.doCleanup:
        print >> sys.stderr, "Deleting %s. (%d/%d)" % (goner, ig+1, totG)
        cmd = 'rm -rf %(goner)s' % locals()
        status |= runner.run(cmd)
        print >> sys.stderr, '%s has left the building.' % goner
    else:
        print >> sys.stderr, "NOT Deleting %s." % goner
        pass
    continue

sys.exit(status)
