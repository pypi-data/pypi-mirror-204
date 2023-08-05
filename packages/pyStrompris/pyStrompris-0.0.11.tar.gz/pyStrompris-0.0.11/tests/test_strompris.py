import unittest
from strompris import common
from strompris.const import SOURCE_HVAKOSTERSTROMMEN
from strompris.schemas import Pris
from strompris.strompris import Strompris
from MockPriceSource import MockPriceSource, sync
from strompris.common import Common
import pytest
from datetime import datetime, timedelta
import aiohttp
import asyncio
import json
import os
import pytest
from typing import Final, List, Optional, final
from strompris.schemas import Pris
from strompris.PriceSource import PriceSource, Hvakosterstrommen


class TestStrompris(unittest.IsolatedAsyncioTestCase, Strompris):
    source: MockPriceSource = MockPriceSource(1)
    priceSource: PriceSource = source
    
    
    async def async_get_price_for_record(self, id: int) -> List[Pris]:
        return await self.source.async_fetch_for_spesific_record(id)
    
    
    @pytest.mark.asyncio
    async def test_async_hasPriceJumpOrDrop(self):        
        record = await self.source.async_fetch_for_spesific_record(0)
        for item in record:
            print(item.__dict__)
        self._apply_tax(record)
        
#        tops = await self.async_get_extreme_price_increases(record)
#        bottoms = await self.async_get_extreme_price_reductions(record)
        print("Result")
#        print(tops)
#        print(bottoms)
        

    @pytest.mark.asyncio
    async def test_async_priceTodayLevel(self):
        common = Common()
        prices = await self.source.async_fetch_for_today()
        self._apply_tax(prices)
        for price in prices:
            level = common.getPriceLevel(price, prices)
            print(price.total, level)
        
    @pytest.mark.asyncio
    async def test_async_priceTomorrowLevel(self):
        common = Common()
        prices = await self.source.async_fetch_for_tomorrow()
        self._apply_tax(prices)
        for price in prices:
            level = common.getPriceLevel(price, prices)
            print(price.total, level)
        

    @pytest.mark.asyncio
    async def test_today_current_price_attrs(self):
        attr = await self.async_get_price_attrs()
        assert attr['start'] != None 
        

    @pytest.mark.asyncio
    async def test_async_priceBigChangesLevel(self):
        common = Common()
        prices = await self.source.async_fetch_for_spesific_record(0)
        self._apply_tax(prices)
                
        leveled = self.get_prices_with_level(prices)
        for price in leveled:
            print(price.total, price.level)

        grouped = self.get_price_level_grouped(leveled)
            
#        inc = await self.async_get_extreme_price_increases(prices)
#        assert len(inc) == 2
#        
#        drop = await self.async_get_extreme_price_reductions(prices)
#        assert len(drop) == 4
#        
#        for price in inc:
#            level = common.getPriceLevel(price, prices)
#            assert level == common.COST_LEVEL__VERY_EXPENSIVE
#        
#        for price in drop:
#            level = common.getPriceLevel(price, prices)
#            assert level == common.COST_LEVEL__VERY_CHEAP
            
    @pytest.mark.asyncio
    async def test_async_priceLevelOn(self, number: int = 0):
        common = Common()
        prices = await self.source.async_fetch_for_spesific_record(number)
        self._apply_tax(prices)
                
        for price in prices:
            level = common.getPriceLevel(price, prices)
            print(price.start.hour, price.total, level)
            
            
    @pytest.mark.asyncio
    async def test_async_priceTest4(self):
        common = Common()
        prices = await self.source.async_fetch_for_spesific_record(4)
        self._apply_tax(prices)
                
        for price in prices:
            level = common.getPriceLevel(price, prices)
            print(price.total, level)
            
#        inc = await self.async_get_extreme_price_increases(prices)
 #       assert len(inc) > 0
        
        
        
