from typing import Any
import math

def ask_for_input(resources: dict[str, Any], failMsg: str) -> Any:
    key: str = None
    while key not in resources.keys():
        key = input()
        if key in resources.keys(): break
        print(failMsg, key, ". Please select one of", list_str(resources.keys()))
    result: Any = resources[key]
    print("You have selected", key)
    return result

def list_str(items: enumerate, print_type: bool = False, print_brackets: bool = False) -> str:
    result: str = ""
    first: bool = True
    def type_and_str(item):
        result = type(item).__name__ if print_type else ""
        result += " " + str(item)
        return result
    for item in items:
        if first: 
            result = type_and_str(item)
        else:
            result = str(result) + ", " + type_and_str(item)
        first = False
    return "[" + result + "]" if print_brackets else result

def weighted_avg(a: float, b: float, ratio: float) -> float:
    assert ratio >= 0 and ratio <= 1
    return (a * ratio) + (b * (1 - ratio))

def clamp(val: float, min_val: float = 0, max_val: float = 1) -> float:
    if min_val is not None and val < min_val: 
        return min_val
    if max_val is not None and val > max_val:
        return max_val
    return val

def sigmoid(x: float, x_0: float = 0., L: float = 1., k: float = 1.) -> float:
    """
    Plugs val into a sigmoid curve to clamp the values in the range (0, L).
    Technically, this generalization is called the logistic function, apparently. 
    https://en.wikipedia.org/wiki/Logistic_function
    To visualize: https://www.desmos.com/calculator/bpbdhepeyo
    """
    return L / (1 + math.e ** -(k * (x - x_0)))

def avg(a: float, b: float) -> float:
    return weighted_avg(a, b, 0.5)