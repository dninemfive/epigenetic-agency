from typing import Any

def ask_for_input(resources: dict[str, Any], failMsg: str) -> Any:
    key: str = None
    while key not in resources.keys():
        key = input()
        if key in resources.keys(): break
        print(failMsg, key, ". Please select one of", list_str(resources.keys()))
    result: Any = resources[key]
    print("You have selected", key)
    return result

def list_str(items: enumerate) -> str:
    result: str = ""
    first: bool = True
    for item in items:
        if first: 
            result = str(item)
        else:
            result = str(result) + ", " + str(item)
        first = False
    return "[" + result + "]"

def weighted_avg(a: float, b: float, ratio: float):
    assert ratio >= 0 and ratio <= 1
    return (a * ratio) + (b * (1 - ratio))