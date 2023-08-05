import unittest
from strompris import common
from strompris.schemas import Pris
from MockPriceSource import MockPriceSource, sync
from strompris.common import Common
from strompris.strompris import Strompris


class TestCommon(unittest.TestCase):
    common = Common()
    today: list[Pris] = []
    tomorrow: list[Pris] = []
    
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.today = MockPriceSource().fetch_for_today()
        self.tomorrow = MockPriceSource().fetch_for_tomorrow()
    
    def test_getMax(self):
        assert self.common.getMax(prices=self.today) == 0.711
    
    def test_getAverage(self):
        assert self.common.getAverage(prices=self.today) == 0.5008750000000001
    
    def test_getMin(self):
        assert self.common.getMin(prices=self.today) == 0.312
        
    def test_onlyExpensiveIsTrue(self):
        now = next(p for p in self.today if p.kwh == self.common.getMax(self.today))
        
        assert self.common.isVeryExpensive(now, self.today) is True
        assert self.common.isExpensive(now, self.today) is True
        self.assertFalse(self.common.isCheap(now, self.today), "Price {kwhCost} is identified as Expensive, and threshold is {threshold}".format(kwhCost=now.kwh, threshold=self.common._isExpensiveThreadhold(self.today)))
        self.assertFalse(self.common.isVeryCheap(now, self.today), "Price {kwhCost} is identified as Expensive, and threshold is {threshold}".format(kwhCost=now.kwh, threshold=self.common._isExpensiveThreadhold(self.today)))
        
    def test_onlyCheapIsTrue(self):
        now = next(p for p in self.today if p.kwh == self.common.getMin(self.today))
        
        assert self.common.isVeryExpensive(now, self.today) is False
        assert self.common.isExpensive(now, self.today) is False
        self.assertTrue(self.common.isCheap(now, self.today), "Price {kwhCost} is not identified as Cheap, and threshold is {threshold}".format(kwhCost=now.kwh, threshold=self.common._isCheapThreshold(self.today)))
        self.assertTrue(self.common.isVeryCheap(now, self.today), "Price {kwhCost} is not identified as Very Cheap, and threshold is {threshold}".format(kwhCost=now.kwh, threshold=self.common._isCheapThreshold(self.today)))
        
    def test_findOnlyCheap(self):
        cheap = list(filter(lambda p: p.start.hour >= 12 and p.start.hour < 16, self.today))
        for price in cheap:
            assert self.common.isCheap(price, self.today) is True
    
    def test_pricesAreOnlyAverage(self):        
        average = list(filter(lambda p: p.start.hour <= 6, self.today))
        avg_2 = list(filter(lambda p: p.start.hour >= 19 and p.start.hour <= 21, self.today))
        average.extend(avg_2)
        for price in average:
            self.assertFalse(self.common.isCheap(price, self.today), "Price {kwhCost} is identified as Cheap @ {hour}, and threshold is {threshold}".format(hour=price.start.hour, kwhCost=price.kwh, threshold=self.common._isCheapThreshold(self.today)))
            self.assertFalse(self.common.isExpensive(price, self.today), "Price {kwhCost} is identified as Expensive".format(kwhCost=price.kwh))
            
    def test_pricesAreOnlyExpensive(self):
        expensive: list[Pris] = []
        exp_1 = list(filter(lambda p: p.start.hour >= 7 and p.start.hour <= 10, self.today))
        exp_2 = list(filter(lambda p: p.start.hour >= 22, self.today))
        expensive.extend(exp_1)
        expensive.extend(exp_2)
        
        for price in expensive:
            self.assertFalse(self.common.isCheap(price, self.today), "Price {kwhCost} is identified as Cheap @ {hour}, and threshold is {threshold}".format(hour=price.start.hour, kwhCost=price.kwh, threshold=self.common._isCheapThreshold(self.today)))
            self.assertTrue(self.common.isExpensive(price, self.today), "Price {kwhCost} is not identified as Expensive, and is {threshold}".format(kwhCost=price.kwh, threshold=self.common._isCheapThreshold(self.today)))
            
            
    def test_defaultsToAverage(self):
        average = list(filter(lambda p: p.start.hour <= 6, self.today))
        avg_2 = list(filter(lambda p: p.start.hour >= 19 and p.start.hour <= 21, self.today))
        average.extend(avg_2)
        self.assertFalse(self.common.isSpreadOk(self.today), "Price spread for passed prices does not qualify for defaulting to Average on {kwhCost}".format(kwhCost=self.common.getSpread(average)))
        

        
    def test_onlyVeryCheapIsTrue(self):
        now = next(p for p in self.tomorrow if p.kwh == self.common.getMin(self.tomorrow))
        
        assert self.common.isVeryExpensive(now, self.tomorrow) is False
        assert self.common.isExpensive(now, self.tomorrow) is False
        self.assertTrue(self.common.isCheap(now, self.tomorrow), "Price {kwhCost} is not identified as Cheap, and threshold is {threshold}".format(kwhCost=now.kwh, threshold=self.common._isCheapThreshold(self.today)))
        self.assertTrue(self.common.isVeryCheap(now, self.tomorrow), "Price {kwhCost} is not identified as Very Cheap, and threshold is {threshold}".format(kwhCost=now.kwh, threshold=self.common._isCheapThreshold(self.today)))
        
    def test_tomorrowHasAtleastOneVeryCheap(self):
        attrs = []
        for price in self.tomorrow:
            attr = self.common.get_price_attrs(price, self.tomorrow)
            print(attr["price_level"])
            attrs.append(attr)
        
        veryCheap = list(filter(lambda a: a["price_level"] == self.common.COST_LEVEL__VERY_CHEAP, attrs))
        self.assertTrue(len(veryCheap) != 0, "There is no entries that are very cheap..")
        print(veryCheap)