import FWCore.ParameterSet.Config as cms

import os



##
## Process definition
##
process = cms.Process("TrackerTreeGeneration")



##
## MessageLogger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('TrackerTreeGenerator')
process.MessageLogger.cerr.INFO.limit = 0
process.MessageLogger.cerr.default.limit = -1
process.MessageLogger.cerr.TrackerTreeGenerator = cms.untracked.PSet(limit = cms.untracked.int32(-1))



##
## Process options
##
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )



##
## Input source
##
process.source = cms.Source("EmptySource")



##
## Number of events
##
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )



##
## Geometry
##
#process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")



##
## Conditions
##
# use always ideal conditions to get no influence from Alignment on absolute Positions, Orientations...
# so it is clear that when choosing special regions in e.g. globalPhi, Modules of the same Rod are contained in the same region
# --- this is now improved, it is always taken from ideal geometry independent of the GlobalTag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'DESIGN42_V11::All'
process.GlobalTag.globaltag = 'DESIGN53_V9::All'



##
## Analyzer
##
process.load("Alignment.TrackerTreeGenerator.TrackerTreeGenerator_cfi")



##
## Output File Configuration
##
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(os.environ['CMSSW_BASE'] + '/src/Alignment/TrackerTreeGenerator/hists/TrackerTree.root')
)



##
## Path
##
process.p = cms.Path(process.TrackerTreeGenerator)







