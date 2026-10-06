from typing import Any, Callable



strint_to_bool: Callable[[str], bool] = lambda v: v == "1"
"""Converts a literal string of "0" or "1" to a boolean"""
str_to_strnone: Callable[[str], str|None] = lambda v: None if not v else v
"""Converts a string that can be empty to a string or none"""

def model_del_empty_str(model_data: dict[str, Any]) -> dict[str, Any]:
    return {k: None if v == "" else v for k,v in model_data.items()}