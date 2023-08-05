from datetime import datetime
import json
from os import stat
from typing import List

LEVEL__VERY_EXPENSIVE  = "VERY_EXPENSIVE"
LEVEL__EXPENSIVE       = "EXPENSIVE"
LEVEL__AVERAGE         = "AVERAGE"
LEVEL__CHEAP           = "CHEAP"
LEVEL__VERY_CHEAP      = "VERY_CHEAP"

class Periode():
    start_tid: datetime
    slutt_tid: datetime
    
    def __init__(self, start: datetime, slutt: datetime) -> None:
        self.start_tid = start
        self.slutt_tid = slutt


class Pris(object):
    start: datetime = None
    slutt: datetime = None
    NOK_kwh: float = 0
    EUR_kwh: float = 0
    kwh: float = 0 # Defaults to NOK
    exr: float = 0 # Exchange Rate
    tax: float = 0.0
    total: float = 0.0
    
    def __init__(self, periode: Periode, data: dict) -> None:
        self.start = periode.start_tid
        self.slutt = periode.slutt_tid
        self.NOK_kwh = data['NOK_per_kWh']
        self.EUR_kwh = data['EUR_per_kWh']
        self.kwh = round(self.NOK_kwh, 3)
        self.total = self.kwh
        self.exr = data['EXR']
    
    def __dict__(self):
        return {
            "start": self.start,
            "slutt": self.slutt,
            "NOK_kwh": self.NOK_kwh,
            "EUR_kwh": self.EUR_kwh,
            "kwh": self.kwh,
            "exr": self.exr,
            "tax": self.tax,
            "total": self.total
        }
        
    def __repr__(self):
        return json.dumps(self.__dict__(), indent=4, default=str)

    def __iter__(self):
        yield "start", self.start,
        yield "slutt", self.slutt,
        yield "NOK_kwh", self.NOK_kwh,
        yield "EUR_kwh", self.EUR_kwh,
        yield "kwh", self.kwh,
        yield "exr", self.exr,
        yield "tax", self.tax
        yield "total", self.total
        
        
class PriceLevel(Pris):

    level: str = None
    def __init__(self) -> None:
        super(Pris, self).__init__()
        

class PriceGroups():
    
    group: str = None
    prices: List[PriceLevel] = []
    
    def __init__(self, prices: List[PriceLevel], group: str) -> None:
        self.prices = prices
        self.group = group
        