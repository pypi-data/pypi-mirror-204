import unittest
from strompris import common
from strompris.schemas import Pris
from MockPriceSource import sync
from strompris.common import Common
from strompris.strompris import Hvakosterstrommen


class TestCommon(unittest.TestCase):
    common = Common()
    today: list[Pris] = []
    tomorrow: list[Pris] = []
    
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        priceSource = Hvakosterstrommen(1)
        self.today = priceSource.async_fetch_for_today()
        self.tomorrow = priceSource.async_fetch_for_tomorrow()

