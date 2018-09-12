from backtester.features.feature import Feature
import numpy as np
import math

class CapitalFeature(Feature):

    '''
    Computing for Instrument. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        positionData = instrumentLookbackData.getFeatureDf('position')
        priceData = instrumentLookbackData.getFeatureDf(featureParams['price'])
        positionData = positionData.replace([np.nan, np.inf, -np.inf], 0)
        priceData = priceData.replace([np.nan, np.inf, -np.inf], 0)
        try:
                 currentPosition = positionData.iloc[-1]
                 currentPrice = priceData.iloc[-1]
                 zeroSeries = currentPosition * 0
                 if (updateNum == 1):
                     previousPosition = zeroSeries
                     previousPrice = zeroSeries
                 else:
                     previousPosition = positionData.iloc[-2]
                     previousPrice = priceData.iloc[-2]
                 currentFees = instrumentLookbackData.getFeatureDf(featureParams['fees']).iloc[-1]
                 currentFees = currentFees.replace([np.nan, np.inf, -np.inf], 0)
                 if 'capitalReqPercent' in featureParams:
                     capitalReqPercent = featureParams['capitalReqPercent']
                 else:
                     capitalReqPercent = 1
                 changeInCapital = capitalReqPercent * (np.abs(currentPosition) * currentPrice - np.abs(previousPosition) * previousPrice) \
                     + currentFees
                 return changeInCapital
        except IndexError:
                raise IndexError('Empty DataFrame')



    '''
    Computing for Market. By default defers to computeForLookbackData
    '''
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        changeInCapital = 0
        capitalDict = instrumentManager.getDataDf()[featureKey]
        capitalDict = capitalDict.replace([np.nan, np.inf, -np.inf], 0.0)
        if len(capitalDict) <= 1:
                return featureParams['initial_capital']
        capital = capitalDict.values[-2]
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        changeInCapital = instrumentLookbackData.getFeatureDf(featureKey).iloc[-1].sum()
        if np.isnan(changeInCapital) or np.isinf(changeInCapital):
                changeInCapital=0.0
        return float(capital) - float(changeInCapital)
        
