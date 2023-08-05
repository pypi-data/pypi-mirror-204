import asyncio
from datetime import datetime
from typing import Any, List, Optional
import pytz
from .schemas import *

def getNorwayTime() -> datetime:
    return datetime.now(pytz.timezone('Europe/Oslo'))

class Common():
    
    COST_LEVEL__VERY_EXPENSIVE  = "VERY_EXPENSIVE"
    COST_LEVEL__EXPENSIVE       = "EXPENSIVE"
    COST_LEVEL__AVERAGE         = "AVERAGE"
    COST_LEVEL__CHEAP           = "CHEAP"
    COST_LEVEL__VERY_CHEAP      = "VERY_CHEAP"
    
    
    def __init__(self) -> None:
        pass
        
    def sync(self, func):
        return asyncio.get_event_loop().run_until_complete(func)
        
    def getTax(self, price: float, taxPercentage: float = 25) -> float:
        """Calculates Tax of price

        Args:
            price (float): Electricty price
            taxPercentage (float, optional): Electricity tax, Defaults to 25 as Norwegian tax bracket is 25% for electricity. Defaults to 25.

        Returns:
            float: Tax
        """
        if (taxPercentage == 0 or price is None):
            return 0
        tax = (price * (taxPercentage / 100))
        return tax
                
    def getAverage(self, prices: list[Pris]) -> Optional[float]:
        """Returns average of prices list

        Args:
            prices (list[Prising]): List of prices

        Returns:
            float: Average price
        """
        if (len(prices) == 0):
            return None
        summed = sum(p.total for p in prices)
        return summed / len(prices)
    
    def getMax(self, prices: list[Pris]) -> Optional[float]:
        """Returns max of prices list

        Args:
            prices (list[Prising]): List of prices

        Returns:
            float: Max price
        """
        if (len(prices) == 0):
            return None
        return max(p.total for p in prices)
    
    def getMin(self, prices: list[Pris]) -> Optional[float]:
        """Returns min of prices list

        Args:
            prices (list[Prising]): List of prices

        Returns:
            float: Min price
        """
        if (len(prices) == 0):
            return None
        return min(p.total for p in prices)
    
    def getSpread(self, prices: list[Pris]) -> float:
        return abs(self.getMax(prices=prices) - self.getMin(prices=prices))
    
    def isSpreadOk(self, prices: list[Pris]) -> bool:
        if self.getSpread(prices=prices) >= 0.5:
            return True
        return False
    
    def isVeryExpensive(self, now: Pris, prices: list[Pris]) -> bool:
        return now.total > 0.9 * self.getMax(prices=prices)
    
    def isExpensive(self, now: Pris, prices: list[Pris]) -> bool:
        return now.total > 0.75 * self.getMax(prices=prices)
    
    def _isExpensiveThreadhold(self, prices: list[Pris]) -> bool:
        return 0.75 * self.getMax(prices=prices)
    
    def _isCheapThreshold(self, prices: list[Pris]) -> bool:
        return 1.6 * self.getMin(prices=prices)
    
    def isAverage(self, now: Pris, prices: List[Pris]) -> bool:
        avg = self.getAverage(prices)
        return avg * 0.9 <= now.total <= avg * 1.1
    
    
    def isCheap(self, now: Pris, prices: list[Pris]) -> bool:
        return now.total < 1.45 * self.getMin(prices=prices)
    
    def isVeryCheap(self, now: Pris, prices: list[Pris]) -> bool:
        return now.total < 1.2 * self.getMin(prices=prices)
    
    def getPriceLevel(self, now: Pris, prices: list[Pris]) -> str:
        if self.isSpreadOk(prices=prices) == False or self.isAverage(now = now, prices=prices):
            return self.COST_LEVEL__AVERAGE
        
        if self.isVeryExpensive(now = now, prices = prices):
            return self.COST_LEVEL__VERY_EXPENSIVE
        
        if self.isExpensive(now = now, prices = prices):
            return self.COST_LEVEL__EXPENSIVE
        
        if self.isVeryCheap(now = now, prices = prices):
            return self.COST_LEVEL__VERY_CHEAP
        
        if self.isCheap(now = now, prices = prices):
            return self.COST_LEVEL__CHEAP
        
        
        return self.COST_LEVEL__AVERAGE
    
    def get_price_attrs(self, price: Pris, prices: list[Pris]) -> dict[str, Any]:
        return {
            "start": price.start.isoformat(),
            "end": price.slutt.isoformat(),
            "kwh": price.kwh,
            "tax": price.tax,
            "total": price.total,
            "max": self.getMax(prices),
            "avg": self.getAverage(prices),
            "min": self.getMin(prices),
            "price_level": self.getPriceLevel(price, prices)
        }
        