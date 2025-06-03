from enum import Enum, auto

class NodeType(str, Enum):
    """Node types enumeration"""
    SIMPLE = "simple"
    FIXED = "fixed"
    HINGE = "hinge"
    ELASTIC = "elastic"

class ForceType(str, Enum):
    """Force types enumeration"""
    POINT = "point"
    RECTANGLE = "rectangle"
    TRIANGLE = "triangle"
    CIRCULAR = "circular"

class Plane(str, Enum):
    """Plane types enumeration"""
    XY = "xy"
    YZ = "yz"
    ZX = "zx"