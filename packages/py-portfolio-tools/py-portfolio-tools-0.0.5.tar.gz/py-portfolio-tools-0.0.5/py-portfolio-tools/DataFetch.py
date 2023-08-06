from .Utils import *
from .Logger import *
import yfinance as yf
import pandas as pd
import json

class DataFetch:
    """DataFetch is a class that handles fetching data from the internet and caching it locally."""

    def __init__(self, cachePath = GetDataPath(), logger = Logger("PPFT")) -> None:
        """Initializes the DataFetch class"""
        self._logger = logger
        self._cachePath = cachePath

    def GetStockInfo(self, tickerName, forceRedownload = False):
        """Gets stock info for a given ticker name"""
        cachedDataLocation = os.path.join(self._cachePath, f'cache/StockInfo/{tickerName}')
        VerifyPath(cachedDataLocation)
        cachedDataPath = os.path.join(cachedDataLocation, f'info.json')
        if PathExists(cachedDataPath) and not forceRedownload:
            self._logger.Log(f'Using cached data for {tickerName} [{cachedDataPath}]')                        
            with open(cachedDataPath, 'r') as f:
                return json.load(f)
        else:
            self._logger.Log(f'Failed to find cached data for {tickerName}')
            self._logger.Log(f'Fetching data for {tickerName} at [{cachedDataPath}]')
            ticker = yf.Ticker(tickerName)
            data = ticker.info
            with open(cachedDataPath, 'w') as f:
                json.dump(data, f)
            return data
        return None
    
    def GetStockHistory(self, tickerName, interval = '1d', start = None, end = None, forceRedownload = False, proxy = None):
        """Gets stock history for a given ticker name"""
        cachedDataLocation = os.path.join(self._cachePath, f'cache/StockInfo/{tickerName}')
        VerifyPath(cachedDataLocation)
        cachedDataPath = os.path.join(cachedDataLocation, f'history-{start}-{end}-{interval}.csv')
        if PathExists(cachedDataPath) and not forceRedownload:
            self._logger.Log(f'Using cached data for {tickerName} [{cachedDataPath}]')                        
            with open(cachedDataPath, 'r') as f:
                return pd.read_csv(f)                
        else:
            self._logger.Log(f'Failed to find cached data for {tickerName}')
            self._logger.Log(f'Fetching data for {tickerName} at [{cachedDataPath}]')
            ticker = yf.Ticker(tickerName)
            data = ticker.history(interval = interval, start = start, end = end, proxy = proxy)
            data.to_csv(cachedDataPath, encoding = 'utf-8')
            return data
        return None
        