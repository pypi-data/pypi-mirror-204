from enum import Enum
class SLType(Enum):
    fixed = 'fixed'
    price_action = 'priceaction'
    indicator = 'indicator'
    

class RiskAppetite (Enum):
    safe = 'safe'
    extra_safe = 'extra_safe'
    medium = 'medium'
    medium_opportunistic = 'medium_opportunistic'
    aggressive = 'aggressive'
    very_aggressive = 'very_aggressive'
