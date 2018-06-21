import pandas as pd
from backtester.constants import *
from backtester.logger import *

class FeatureSelectionManager(object):
    """
    """
    def __init__(self, systemParams):
        self.systemParams = systemParams
        self.__instrumentData = None
        self.__targetVariables = None
        self.__selectedFeatures = {}

    def getFeatureDf(self, featureKey):
        return self.__instrumentData[featureKey]

    def getTargetVariableDf(self, targetVariableKey):
        return self.__targetVariables[targetVariableKey]

    def getAllSelectedFeaturesByKey(self, targetVariableKey):
        return self.__selectedFeatures[targetVariableKey]

    def getAllSelectedFeatures(self):
        return self.__selectedFeatures

    def getKeysFromData(self, data):
        if isinstance(data, dict):
            return data.keys()
        elif isinstance(data, pd.DataFrame):
            return data.columns.tolist()
        else:
            raise ValueError

    def pruneFeatures(self, instrumentData, targetVariables, featureSelectionConfigs=None, aggregationMethod='intersect'):
        if featureSelectionConfigs is None:
            featureSelectionConfigs = self.systemParams.getFeatureSelectionConfigsForInstrumentType(INSTRUMENT_TYPE_STOCK)

        featureKeys = self.getKeysFromData(instrumentData)
        targetVariableKeys = self.getKeysFromData(targetVariables)
        self.__instrumentData = instrumentData
        self.__targetVariables = targetVariables
        self.__selectedFeatures = {key : [] for key in targetVariableKeys}

        for targetVariableKey in targetVariableKeys:
            for featureSelectionConfig in featureSelectionConfigs:
                featureSelectionKey = featureSelectionConfig.getFeatureKey()
                featureSelectionParams = featureSelectionConfig.getFeatureParams()
                featureSelectionId = featureSelectionConfig.getFeatureId()
                featureSelectionCls = featureSelectionConfig.getClassForFeatureId(featureSelectionId)
                selectedFeatures = featureSelectionCls.extractImportantFeatures(targetVariableKey, featureKeys,
                                                                                  featureSelectionParams, self)
                if self.__selectedFeatures[targetVariableKey] == []:
                    self.__selectedFeatures[targetVariableKey] = selectedFeatures
                elif aggregationMethod == 'union':
                    self.__selectedFeatures[targetVariableKey] = list(set(selectedFeatures).union(self.__selectedFeatures[targetVariableKey]))
                elif aggregationMethod == 'intersect':
                        self.__selectedFeatures[targetVariableKey] = list(set(selectedFeatures).intersection(self.__selectedFeatures[targetVariableKey]))
                else:
                    raise ValueError
