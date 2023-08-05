
from datetime import datetime
from typing import Any, Final, List, Optional, final
from .schemas import *
from .common import *
from .PriceSource import *
from .const import *

class Strompris(Common):
    
    priceSource: PriceSource
    
    def __init__(self, source: str, zone: int) -> None:
        if (source is SOURCE_HVAKOSTERSTROMMEN):
            self.priceSource = Hvakosterstrommen(price_zone=zone)
        else:
            raise Exception("Could not find source:",source)
    
    @final
    def showPriceZones(self) -> None:
        print("NO1", "Øst-Norge")
        print("NO2", "Sør-Norge")
        print("NO3", "Midt-Norge")
        print("NO4", "Nord-Norge")
        print("NO5", "Vest-Norge")
        
    def getTaxPercentage(self) -> float:
        if (self.priceSource._price_zone != 4):
            return 25
        else:
            return 0
        
    def _apply_tax(self, prices:list[Pris]) -> None:
        """Applies tax to items in list."""    
        if (self.priceSource._price_zone != 4):
            """Price Zone NO4 is not subjected to Electricity Tax as of now"""
            for price in prices:
                price.tax = self.getTax(price.kwh) 
                price.total = price.kwh + price.tax
        
    async def async_get_prices_for_today(self) -> list[Pris]:
        today = await self.priceSource.async_fetch_for_today()
        if (today is None):
            return []              
        self._apply_tax(today)
        return today 
    
    async def async_get_prices_for_tomorrow(self) -> list[Pris]:
        try:
            tomorrow = await self.priceSource.async_fetch_for_tomorrow()
            if (tomorrow is None):
                return []
            self._apply_tax(tomorrow)
            return tomorrow   
        except PriceNotAvailable:
            print("Price data is not available for tomorrow")
        return []
        
    async def async_get_available_prices(self) -> list[Pris]:    
        """Fetches prices for today + tomorrow (if available)

        Returns:
            list[Prising]: Prices
        """
        today = await self.async_get_prices_for_today()
        tomorrow = await self.async_get_prices_for_tomorrow()
        return (today + tomorrow)
        
    def get_prices_for_today(self) -> list[Pris]:
        return self.sync(self.async_get_prices_for_today())
    
    def get_prices_for_tomorrow(self) -> list[Pris]:
        return self.sync(self.async_get_prices_for_tomorrow())
    
    def get_available_prices(self) -> list[Pris]:    
        today = self.get_prices_for_today()
        tomorrow = self.get_prices_for_tomorrow()
        return (today + tomorrow)
    
    async def async_get_current_price(self) -> Optional[Pris]:
        if (not self.priceSource._price_today or len(self.priceSource._price_today) == 0):
            await self.async_get_prices_for_today()
        return next((x for x in self.priceSource._price_today if x.start.hour == getNorwayTime().hour), None)
        
    def get_current_price(self) -> Optional[Pris]:
        return self.sync(self.async_get_current_price())
                
    async def async_get_price_attrs(self, price: Pris = None, prices: List[Pris] = None) -> dict[str, Any]:
        if (price is None):
            price = await self.async_get_current_price()
        if (prices is None or len(prices) == 0):
            prices = self.priceSource._price_today
        
        common = Common()
        max = common.getMax(self.priceSource._price_today)
        avg = common.getAverage(self.priceSource._price_today)
        min =  common.getMin(self.priceSource._price_today)
        return {
            "start": price.start.isoformat(),
            "end": price.slutt.isoformat(),
            "kwh": price.kwh,
            "tax": price.tax,
            "total": price.total,
            "max": max + common.getTax(max, self.getTaxPercentage()),
            "avg": avg + common.getTax(avg, self.getTaxPercentage()),
            "min": min + common.getTax(min, self.getTaxPercentage()),
            "price_level": common.getPriceLevel(price, self.priceSource._price_today)
        }
     
    async def async_get_price_tomorrow_attrs(self) -> dict[str, Any]:
        common = Common()
        max = common.getMax(self.priceSource._price_tomorrow)
        avg = common.getAverage(self.priceSource._price_tomorrow)
        min = common.getMin(self.priceSource._price_tomorrow)
        return {
            "max": max + common.getTax(max, self.getTaxPercentage()),
            "avg": avg + common.getTax(avg, self.getTaxPercentage()),
            "min": min + common.getTax(min, self.getTaxPercentage())
        }
    
    def get_current_price_attrs(self) -> dict[str, Any]:
        return self.sync(self.async_get_price_attrs())
    
    def get_price_attrs(self, price: Pris, prices: List[Pris]) -> dict[str, Any]:
        return self.sync(self.async_get_price_attrs(price, prices))
    
    
    def __get_avg(self, prices: List[Pris]) -> float:
        common = Common()
        avg = common.getAverage(prices)
        #avg = avg + common.getTax(avg, self.getTaxPercentage())
        return avg
        
    def get_prices_with_level(self, prices: List[Pris]) -> List[PriceLevel]:  
        """
        """  
        _prices = prices.copy()
        instanced: List[PriceLevel] = []
        c = Common()
        for price in _prices:
            pl: PriceLevel = price
            pl.__class__ = PriceLevel
           # pl.__dict__.update(price.__dict__)
            pl.level = c.getPriceLevel(price, _prices)
            instanced.append(pl)
        return instanced
        
    def __price_is_cheap(self, price: PriceLevel) -> bool:
        return price.level == LEVEL__CHEAP or price.level == LEVEL__VERY_CHEAP
    
    def __price_is_expensive(self, price: PriceLevel) -> bool:
        return price.level == LEVEL__EXPENSIVE or price.level == LEVEL__VERY_EXPENSIVE
        
    def get_price_level_grouped(self, prices: List[PriceLevel]) -> List[PriceGroups]:
        """
        """
        result: List[PriceGroups] = []
        
        ig: List[PriceLevel] = []
        for i, price in enumerate(prices):
            if (price.level == LEVEL__AVERAGE and len(ig) == 0):
                continue
            if (any(c.level == LEVEL__VERY_CHEAP or c.level == LEVEL__CHEAP for c in ig)):
                """List is of cheap"""
                if (self.__price_is_cheap(price)):
                    ig.append(price)
                    continue
                else:
                    """If next item is not of cheap, then store ig as a group"""
                    if (len(ig) > 1):
                        result.append(PriceGroups(ig, LEVEL__CHEAP))
                        ig = []
                    else:
                        """If item group is smaller or equal to 1 then it will be skipped"""
                        ig = []
            
            elif (any(c.level == LEVEL__EXPENSIVE or c.level == LEVEL__VERY_EXPENSIVE for c in ig)):
                """List is of expensive"""
                if (self.__price_is_expensive(price)):
                    ig.append(price)
                    continue
                else:
                    """"""
                    if (price.level == LEVEL__AVERAGE and len(prices)-1 > i+1):
                        """If there is a next item 
                        and it is of expensive or very expensive then add average to expensicve"""
                        ni = prices[i+1]
                        
                        if (ni != None and self.__price_is_expensive(ni)):
                            """Since next item is of expensive, do continue"""
                            ig.append(price)
                            continue 

                    if (len(ig) > 1):
                        result.append(PriceGroups(ig, LEVEL__EXPENSIVE))
                        ig = []
                    else:
                        """If item group is smaller or equal to 1 then it will be skipped"""
                        ig = []
            
            
            if (price.level != LEVEL__AVERAGE and len(ig) == 0):
                ig.append(price)
        
        
        return result
                
    