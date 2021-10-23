
from typing import List
from appapy.data import naeb
    
def execute(args: List[str]):
    if args is None or len(args) == 0:
        raise ValueError(args)
    
    print('executing')
    arg0 = args[0]
    
    if arg0 == "naeb":
        naeb.process()
    else:
        raise ValueError(args)