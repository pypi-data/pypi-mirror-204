import math
import random

ANUKE_EPSILON = 1e-6
LONG_MAX = 0x7fffffffffffffff
arithmetic_operators = {}


def register_operator(name):
    def decorator(function):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        arithmetic_operators[name] = function
        return wrapper
    return decorator


arithmetic_operators["add"] = lambda a, b : a + b
arithmetic_operators["sub"] = lambda a, b : a - b
arithmetic_operators["mul"] = lambda a, b : a * b
arithmetic_operators["mod"] = lambda a, b : a % b
arithmetic_operators["pow"] = lambda a, b : math.pow(a, b)

@register_operator("div")
def mlog_division(a, b):
    if b != 0:
        return a / b
    return None

@register_operator("idiv")
def mlog_int_division(a, b):
    if b != 0:
        return a // b
    return None

# TODO: arithmetic only?
@register_operator("equal")
def equal(a: float, b: float):
    return 0.0 if abs(a-b) >= ANUKE_EPSILON else 1.0

@register_operator("notEqual")
def not_equal(a: float, b: float):
    return 0.0 if abs(a-b) < ANUKE_EPSILON else 1.0


arithmetic_operators["lessThan"] = lambda a, b : a < b
arithmetic_operators["lessThanEq"] = lambda a, b : a <= b
arithmetic_operators["greaterThan"] = lambda a, b : a > b
arithmetic_operators["greaterThanEq"] = lambda a, b : a >= b
arithmetic_operators["strictEqual"] = lambda a, b : a == b
# For jumps
arithmetic_operators["always"] = lambda a, b: True

arithmetic_operators["land"] = lambda a, b : a != 0 and b != 0

arithmetic_operators["min"] = lambda a, b: min(a, b)
arithmetic_operators["max"] = lambda a, b: max(a, b)
arithmetic_operators["abs"] = lambda a, b: abs(a)
arithmetic_operators["ceil"] = lambda a, b: math.ceil(a)
arithmetic_operators["floor"] = lambda a, b: math.floor(a)
arithmetic_operators["log"] = lambda a, b: math.log(a)
arithmetic_operators["log10"] = lambda a, b: math.log10(a)
arithmetic_operators["sqrt"] = lambda a, b: math.sqrt(a)
arithmetic_operators["rand"] = lambda a, b: random.random() * a

# Anuke vector: (x, y)
arithmetic_operators["angle"] = lambda a, b: math.degrees(math.atan2(b, a))
arithmetic_operators["len"] = lambda a, b: math.hypot(a, b)

# Anuke: I use degree measures :P
arithmetic_operators["sin"] = lambda a, b: math.sin(math.radians(a))
arithmetic_operators["cos"] = lambda a, b: math.cos(math.radians(a))
arithmetic_operators["tan"] = lambda a, b: math.tan(math.radians(a))
arithmetic_operators["asin"] = lambda a, b: math.degrees(math.asin(a))
arithmetic_operators["acos"] = lambda a, b: math.degrees(math.acos(a))
arithmetic_operators["atan"] = lambda a, b: math.degrees(math.atan(a))

# Bitwise operations
arithmetic_operators["and"] = lambda a, b : (int(a) & int(b)) & LONG_MAX
arithmetic_operators["or"] = lambda a, b : (int(a) | int(b)) & LONG_MAX
arithmetic_operators["xor"] = lambda a, b : (int(a) ^ int(b)) & LONG_MAX
arithmetic_operators["not"] = lambda a, b : int(a) ^ LONG_MAX

# sign-filling or sign-keeping ?
arithmetic_operators["shl"] = lambda a, b : (int(a) << int(b)) & LONG_MAX
arithmetic_operators["shr"] = lambda a, b : (int(a) >> int(b)) & LONG_MAX
