import FWCore.ParameterSet.Config as cms




## Trigger for MC
import HLTrigger.HLTfilters.hltHighLevel_cfi
TriggerFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    #HLTPaths = ['HLT_Mu9', 'HLT_Mu15_v*'],
    #HLTPaths = ['HLT_IsoMu17_v*'],
     HLTPaths = ['HLT_IsoMu24_*'],
    throw = False,
)



## SEQUENCE
TriggerSelectionSequence = cms.Sequence(
    TriggerFilter
)





