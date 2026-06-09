from types import MappingProxyType
from typing import Any



def deep_freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({
            k: deep_freeze(v)
            for k,v in value.items()
        })
    
    elif isinstance(value, list):
        return tuple(
            deep_freeze(v)
            for v in value
        )
    
    elif isinstance(value, set):
        return frozenset(
            deep_freeze(v)
            for v in value
        )
    
    else:
        return value