"""@brief Register output data with the data server.
@author W. Focke <focke@slac.stanford.edu>
"""
# This script is automagically pasted into the XML at install time

from java.util import HashMap

def getVar(fileType, name):
    mangledName = '_'.join([nameManglingPrefix, fileType, name])
    value = parentPI.getVariable(mangledName)
    return value

currentStream = pipeline.getCurrentStream()

parentPI = currentStream.getProcessInstance(parentProcess)

runNumber = int(RUNID[1:])

dsName = RUNID
fileFormat = getVar(fileType, 'format')
dcType = getVar(fileType, 'dcType')
dcGroup = getVar(fileType, 'group')
site = getVar(fileType, 'site')
fileName = getVar(fileType, 'fileName')
version = getVar(fileType, 'ver')

fcPi = currentStream.getProcessInstance(timeProcess)
lessBrokenTStart = fcPi.getVariable('tStart')
lessBrokenTStop = fcPi.getVariable('tStop')
mootAlias = fcPi.getVariable('mootAlias')
mootKey = fcPi.getVariable('mootKey')

attributes = HashMap()
attributes.put('sCreator', creator)
attributes.put('sDataSource', DATASOURCE)
attributes.put('nDownlink', DOWNLINK_ID)
attributes.put('sIntent', mootAlias)
attributes.put('nMetStart', lessBrokenTStart)
attributes.put('nMetStop', lessBrokenTStop)
attributes.put('nMootKey', mootKey)
attributes.put('nRun', runNumber)

mdRepr = getVar(fileType, 'metadata')
if mdRepr:
    metadata = eval(mdRepr)
    for key, value in metadata.items(): attributes.put(key, value)

print attributes

dsNew = datacatalog.newDataset(dsName, fileFormat, dcType, dataCatDir, dcGroup, site, fileName)
dsNew.setVersionID(version)
ds = datacatalog.registerDataset(dsNew, attributes);
