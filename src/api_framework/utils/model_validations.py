from typing import Any



def strint_to_bool(value: str) -> bool: return value == "1"

def model_del_empty_str(model_data: dict[str, Any]) -> dict[str, Any]:
    return {k: None if v == "" else v for k,v in model_data.items()}