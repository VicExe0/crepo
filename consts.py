from typing import Optional, Any

class Array:
    def __init__( self, values: list[Any], func: Optional[type] = None ) -> None:
        self.values = list(map(func, values)) if func else values

    def __getitem__( self, index: int ) -> Any:
        if index < len(self.values):
            return self.values[index]
        
        return self.values[-1]
    
    def __str__( self ):
        return str(self.values)

MONEY_MULTIPLIERS = Array([
    3.57142851821014,
    4.76190457268368,
    4.74639982908994,
    7.07604922227163,
    7.00606421609719,
    9.20059248925003,
    8.99406905420288,
    8.70545410147724,
    8.39388691548115,
    8.21523722771264,
    8.16998770743610
])

MONSTER_LEVELS = Array([
    [( 1, 0, 1 )] * 2  +
    [( 1, 1, 1 )] * 3  +
    [( 2, 2, 2 )] * 3  +
    [( 2, 3, 2 )]      +
    [( 2, 3, 3 )] * 10 +
    [( 3, 4, 4 )]       
][0])

EXTRACTION_AMOUNT = Array([
    [( 1 )]     +
    [( 2 )] * 2 +
    [( 3 )] * 2 +
    [( 4 )] * 9 +
    [( 5 )]
][0])

ORB_VALUE = [
    ( 2000, 3000 ),
    ( 3500, 4500 ),
    ( 5500, 7500 )
]

IDLE_TIME = Array([
    ( 240, 360 ),
    ( 214, 321 ),
    ( 134, 202 ),
    ( 78,  117 ),
    ( 54,  81  ),
    ( 48,  72  ),
    ( 47,  70  ),
    ( 42,  63  ),
    ( 34,  52  ),
    ( 22,  33  ),
    ( 0,   0   )
])