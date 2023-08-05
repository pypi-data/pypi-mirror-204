# Strømpris


## Usage

Supported sources:
- Hvakosterstrommen

```python
from strompris.strompris import Strompris 
from strompris.const import SOURCE_HVAKOSTERSTROMMEN

strompris = Strompris(source=SOURCE_HVAKOSTERSTROMMEN, zone=1) # Can also be used with direct string # Zone 1-5

"""Returns pricing for today and tomorrow if available"""
priser = strompris.get_available_prices() 

"""Returns pricing for current hour using GMT+1|+2"""
now = strompris.get_current_price()

"""Returns pricing for current hour along with extra info:

total (kwh + tax)
min
max
avg
tax
price_level
"""
nowAttrs = strompris.getPriceAttrs(zone=1)


```


![hvakosterstrommen.no](./static-assets/hvakosterstrommen.png)