import os

import FWCore.ParameterSet.Config as cms




##
## Setup command line options
##
import FWCore.ParameterSet.VarParsing as VarParsing
import sys
options = VarParsing.VarParsing ('standard')
options.register('sample', 'data1', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "Input sample")
options.register('fileNumber', 1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Input file number")
options.register('iterNumber', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Iteration number")
options.register('lastIter', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Last iteration")
options.register('alignRcd','design', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "AlignmentRcd")



# get and parse the command line arguments
if( hasattr(sys, "argv") ):
    for args in sys.argv :
        arg = args.split(',')
        for val in arg:
            val = val.split('=')
            if(len(val)==2):
                setattr(options,val[0], val[1])

print "Input sample: ", options.sample
print "Input file number", options.fileNumber
print "Iteration number: ", options.iterNumber
print "Last iteration: ", options.lastIter
print "AlignmentRcd: ", options.alignRcd



##
## Process definition
##
process = cms.Process("ApeEstimator")



##
## Message Logger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('SectorBuilder')
process.MessageLogger.categories.append('ResidualErrorBinning')
process.MessageLogger.categories.append('HitSelector')
process.MessageLogger.categories.append('CalculateAPE')
process.MessageLogger.categories.append('ApeEstimator')
#process.MessageLogger.categories.append('TrackRefitter')
process.MessageLogger.categories.append('AlignmentTrackSelector')
process.MessageLogger.cerr.INFO.limit = 0
process.MessageLogger.cerr.default.limit = -1
process.MessageLogger.cerr.SectorBuilder = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.HitSelector = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.CalculateAPE = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.ApeEstimator = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.AlignmentTrackSelector = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 ## really show only every 1000th



##
## Process options
##
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)



##
## Input sample definition
##
isData1 = isData2 = False
isData = False
isQcd = isWlnu = isZmumu = isZtautau = isZmumu10 = isZmumu20 = False
isMc = False
isParticleGunMuon = isParticleGunPion = False
isParticleGun = False
if options.sample == 'data1':
    isData1 = True
    isData = True
elif options.sample == 'data2':
    isData2 = True
    isData = True
elif options.sample == 'data3':
    isData3 = True
    isData = True
elif options.sample == 'data4':
    isData4 = True
    isData = True
elif options.sample == 'qcd':
    isQcd = True
    isMc = True
elif options.sample == 'wlnu':
    isWlnu = True
    isMc = True
elif options.sample == 'zmumu':
    isZmumu = True
    isMc = True
elif options.sample == 'ztautau':
    isZtautau = True
    isMc = True
elif options.sample == 'zmumu10':
    isZmumu10 = True
    isMc = True
elif options.sample == 'zmumu20':
    isZmumu20 = True
    isMc = True
else:
    print 'ERROR --- incorrect data sammple: ', options.sample
    exit(8888)



##
## Input Files
##
readFiles = cms.untracked.vstring()
process.source = cms.Source ("PoolSource",
    fileNames = readFiles
)
readFiles.extend( [
    'file:reco.root',
] )



##
## Number of Events (should be after input file)
##
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
if isQcd:
  #if options.fileNumber==1: process.maxEvents.input = 496645   # 588022 events
  if options.fileNumber==1: process.maxEvents.input = 550000   # 588022 events   # scale up to match observation
elif isWlnu:
  if options.fileNumber==1: process.maxEvents.input =    91613 # 958439 events
  elif options.fileNumber==2: process.maxEvents.input =  91613 # 958759 events
  elif options.fileNumber==3: process.maxEvents.input =  91613 # 959034 events
  elif options.fileNumber==4: process.maxEvents.input =  91613 # 960240 events
  elif options.fileNumber==5: process.maxEvents.input =  91613 # 960338 events
  elif options.fileNumber==6: process.maxEvents.input =  91613 # 961001 events
  elif options.fileNumber==7: process.maxEvents.input =  91613 # 959984 events
  elif options.fileNumber==8: process.maxEvents.input =  91612 # 959096 events
  elif options.fileNumber==9: process.maxEvents.input =  91612 # 961693 events
  elif options.fileNumber==10: process.maxEvents.input = 91612 # 960902 events
  elif options.fileNumber==11: process.maxEvents.input = 91612 # 959644 events
  elif options.fileNumber==12: process.maxEvents.input = 91612 # 960541 events
  elif options.fileNumber==13: process.maxEvents.input = 91612 # 979030 events
  elif options.fileNumber==14: process.maxEvents.input = 91612 # 958643 events
  elif options.fileNumber==15: process.maxEvents.input = 91612 # 822995 events
elif isZmumu10:
  if options.fileNumber==1: process.maxEvents.input = 10121    # 114536 events
elif isZmumu20:
  if options.fileNumber==1: process.maxEvents.input =     9490 # 692756 events
  elif options.fileNumber==2: process.maxEvents.input =   9490 # 697785 events
  elif options.fileNumber==3: process.maxEvents.input =   9490 # 696344 events
  elif options.fileNumber==4: process.maxEvents.input =   9490 # 696398 events
  elif options.fileNumber==5: process.maxEvents.input =   9490 # 694961 events
  elif options.fileNumber==6: process.maxEvents.input =   9490 # 695541 events
  elif options.fileNumber==7: process.maxEvents.input =   9490 # 693676 events
  elif options.fileNumber==8: process.maxEvents.input =   9490 # 652365 events
  elif options.fileNumber==9: process.maxEvents.input =   9490 # 695692 events
  elif options.fileNumber==10: process.maxEvents.input =  9490 # 695065 events
  elif options.fileNumber==11: process.maxEvents.input =  9490 # 696383 events
  elif options.fileNumber==12: process.maxEvents.input =  9490 # 696564 events
  elif options.fileNumber==13: process.maxEvents.input =  9490 # 695379 events
  elif options.fileNumber==14: process.maxEvents.input =  9490 # 692976 events
  elif options.fileNumber==15: process.maxEvents.input =  9490 # 682748 events
  elif options.fileNumber==16: process.maxEvents.input =  9490 # 697161 events
  elif options.fileNumber==17: process.maxEvents.input =  9490 # 695905 events
  elif options.fileNumber==18: process.maxEvents.input =  9490 # 696553 events
  elif options.fileNumber==19: process.maxEvents.input =  9489 # 698772 events
  elif options.fileNumber==20: process.maxEvents.input =  9489 # 696231 events
  elif options.fileNumber==21: process.maxEvents.input =  9489 # 372419 events
elif isData1:
  if options.fileNumber==1: process.maxEvents.input = 1   # 894724 events
  elif options.fileNumber==2: process.maxEvents.input = 1 # 895421 events
  elif options.fileNumber==3: process.maxEvents.input = 1 # 207016 events
elif isData2:
  if options.fileNumber==1: process.maxEvents.input =    254095 # 1101299 events
  elif options.fileNumber==2: process.maxEvents.input =  254095 # 947505 events
  elif options.fileNumber==3: process.maxEvents.input =  254095 # 1087702 events
  elif options.fileNumber==4: process.maxEvents.input =  254095 # 919027 events
  elif options.fileNumber==5: process.maxEvents.input =  254095 # 1064381 events
  elif options.fileNumber==6: process.maxEvents.input =  254095 # 896920 events
  elif options.fileNumber==7: process.maxEvents.input =  254094 # 952183 events
  elif options.fileNumber==8: process.maxEvents.input =  254094 # 986213 events
  elif options.fileNumber==9: process.maxEvents.input =  254094 # 893426 events
  elif options.fileNumber==10: process.maxEvents.input = 254094 # 542679 events


##
## Check run and event numbers for Dublicates --- only for real data
##
#process.source.duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
#process.source.duplicateCheckMode = cms.untracked.string("checkEachFile")
process.source.duplicateCheckMode = cms.untracked.string("checkEachRealDataFile")
#process.source.duplicateCheckMode = cms.untracked.string("checkAllFilesOpened")   # default value



##
## Whole Refitter Sequence
##
process.load("ApeEstimator.ApeEstimator.TrackRefitter_38T_cff")
if isParticleGun:
    process.GlobalTag.globaltag = 'DESIGN42_V12::All'
elif isMc:
    #process.GlobalTag.globaltag = 'DESIGN42_V12::All'
    #process.GlobalTag.globaltag = 'START42_V12::All'
    #process.GlobalTag.globaltag = 'MC_42_V12::All'
    process.GlobalTag.globaltag = 'DESIGN53_V9::All'

    if options.alignRcd=='useStartGlobalTagForAllConditions':
        #process.GlobalTag.globaltag = 'START42_V12::All'
        process.GlobalTag.globaltag = 'DESIGN53_V9::All'
elif isData:
    #process.GlobalTag.globaltag = 'GR_R_42_V21::All'
    process.GlobalTag.globaltag = 'FT_R_53_V18::All'
## --- Further information (Monte Carlo and Data) ---
#process.TTRHBuilderGeometricAndTemplate.StripCPE = 'StripCPEfromTrackAngle'
#process.TTRHBuilderGeometricAndTemplate.PixelCPE = 'PixelCPEGeneric'
process.FittingSmootherRKP5.EstimateCut = 25.
process.FittingSmootherRKP5.RejectTracks = True
process.FittingSmootherRKP5.LogPixelProbabilityCut = -14.
#process.HighPuritySelector.src = 'generalTracks'
process.HighPuritySelector.src = 'MuSkim'



##
## New pixel templates
##
process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(
        record = cms.string("SiPixelTemplateDBObjectRcd"),
        tag = cms.string("SiPixelTemplateDBObject_38T_v3_mc"),
        connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PIXEL"),
    )
)



##
## Alignment and APE
##
import CalibTracker.Configuration.Common.PoolDBESSource_cfi
## Choose Alignment (w/o touching APE)
if options.alignRcd=='design':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_31X_FROM21X',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerIdealGeometry210_mc'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
elif options.alignRcd == 'misalTob20':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/misalignments/AlignmentsTob20.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
elif options.alignRcd == 'idealAligned':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/idealAlignedGeometry/alignments_MP.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('Alignments'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
elif options.alignRcd == 'GR10_v6':
  # Recent geometry
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_31X_ALIGNMENT',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerAlignment_GR10_v6_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus5':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_5.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus10':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_10.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus15':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_15.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus20':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_20.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'globalTag':
  pass
elif options.alignRcd == 'useStartGlobalTagForAllConditions':
  pass
elif options.alignRcd == '':
  pass
else:
  print 'ERROR --- incorrect alignment: ', options.alignRcd
  exit(8888)

## APE
if options.iterNumber==0:
    process.myTrackerAlignmentErr = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
      connect = 'frontier://FrontierProd/CMS_COND_31X_FROM21X',
      toGet = [
        cms.PSet(
          record = cms.string('TrackerAlignmentErrorRcd'),
          tag = cms.string('TrackerIdealGeometryErrors210_mc'),
        ),
      ],
    )
    process.es_prefer_trackerAlignmentErr = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentErr")
else:
    process.myTrackerAlignmentErr = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
      connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/ApeEstimator/ApeEstimator/hists/apeObjects/apeIter'+str(options.iterNumber-1)+'.db',
      toGet = [
        cms.PSet(
          record = cms.string('TrackerAlignmentErrorRcd'),
          tag = cms.string('AlignmentErrors'),
        ),
      ],
    )
    process.es_prefer_trackerAlignmentErr = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentErr")



##
## Beamspot (Use correct Beamspot for simulated Vertex smearing of ParticleGun)
##
if isParticleGun:
    process.load("ApeEstimator.ApeEstimator.BeamspotForParticleGun_cff")



##
## ApeEstimator
##
from ApeEstimator.ApeEstimator.ApeEstimator_cff import *
process.ApeEstimator1 = ApeEstimator.clone(
    tjTkAssociationMapTag = "TrackRefitterHighPurityForApeEstimator",
    analyzerMode = False,
)

process.ApeEstimator2 = ApeAnalyzer.clone()
process.ApeEstimator3 = process.ApeEstimator2.clone(
    zoomHists = False,
)

process.ApeEstimatorSequence = cms.Sequence(process.ApeEstimator1)
if options.iterNumber==0:
  process.ApeEstimatorSequence *= process.ApeEstimator2
  process.ApeEstimatorSequence *= process.ApeEstimator3
elif options.lastIter == True:
  process.ApeEstimatorSequence *= process.ApeEstimator2



##
## Output File Configuration
##
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/workingArea/'+options.sample+str(options.fileNumber)+'.root'),
    closeFileFast = cms.untracked.bool(True)
)



##
## Path
##
process.p = cms.Path(
    #process.TriggerSelectionSequence*
    process.RefitterHighPuritySequence*
    process.ApeEstimatorSequence
)



