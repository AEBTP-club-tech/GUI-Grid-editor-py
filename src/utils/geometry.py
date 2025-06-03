import math

def calculate_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def find_intersection_point(line1, line2):
    """Find intersection point between two lines
    
    Args:
        line1: Tuple (x1, y1, x2, y2) representing first line
        line2: Tuple (x1, y1, x2, y2) representing second line
        
    Returns:
        Tuple (x, y) of intersection point, or None if lines are parallel
    """
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    
    # Calculate the denominator
    denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    
    # If denominator is zero, lines are parallel
    if denominator == 0:
        return None
    
    # Calculate the numerators
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator
    
    # If both ua and ub are between 0 and 1, the intersection is within both line segments
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return (x, y)
    
    return None

def point_line_distance(point, line):
    """Calculate the distance from a point to a line
    
    Args:
        point: Tuple (x, y) representing the point
        line: Tuple (x1, y1, x2, y2) representing the line
        
    Returns:
        Float representing the distance
    """
    x, y = point
    x1, y1, x2, y2 = line
    
    # If x1 == x2 and y1 == y2, the line is a point
    if x1 == x2 and y1 == y2:
        return calculate_distance(x, y, x1, y1)
    
    # Calculate the distance using the formula
    # d = |Ax + By + C| / sqrt(A² + B²)
    # where A = y2 - y1, B = x1 - x2, C = x2*y1 - x1*y2
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    
    # Calculate the distance
    distance = abs(A * x + B * y + C) / math.sqrt(A ** 2 + B ** 2)
    
    return distance