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

def weighted_avg(a: float, b: float, ratio: float):
    assert ratio >= 0 and ratio <= 1
    return (a * ratio) + (b * (1 - ratio))