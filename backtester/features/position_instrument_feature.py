from backtester.features.feature import Feature


class PositionInstrumentFeature(Feature):

   '''
   Computing for Instrument. By default defers to computeForLookbackData
   '''

   @classmethod
   def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
       instrumentsDict = instrumentManager.getAllInstrumentsByInstrumentId()
       if len(instrumentsDict) == 0:
           raise ValueError('instrumentDict is empty')
           return None
       positionDict = {}
       for instrumentId in instrumentsDict:
           positionDict[instrumentId] = instrumentManager.getInstrument(instrumentId).getCurrentPosition()
       return positionDict

