from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QPointF, QRectF

from src.models.constants import NodeType, ForceType

def draw_node(scene, x, y, node_type, zoom_level=1.0):
    """Draw a node on the scene with the given type"""
    # Base size adjusted for zoom
    base_size = 8
    size = base_size * zoom_level
    
    if node_type == NodeType.SIMPLE:
        # Simple node: red circle
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setWidth(1)
        brush = QBrush(QColor("red"), Qt.BrushStyle.SolidPattern)
        return scene.addEllipse(x-size, y-size, size*2, size*2, pen, brush)
    
    elif node_type == NodeType.FIXED:
        # Fixed support: blue triangle
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setWidth(1)
        brush = QBrush(QColor("blue"), Qt.BrushStyle.SolidPattern)
        
        # Create triangle path
        path = QPainterPath()
        path.moveTo(x, y-size*1.6)  # Top point
        path.lineTo(x-size*1.6, y+size*1.6)  # Bottom left
        path.lineTo(x+size*1.6, y+size*1.6)  # Bottom right
        path.closeSubpath()
        
        return scene.addPath(path, pen, brush)
    
    elif node_type == NodeType.HINGE:
        # Hinge: green circle with white cross
        # Draw circle
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setWidth(1)
        brush = QBrush(QColor("green"), Qt.BrushStyle.SolidPattern)
        node = scene.addEllipse(x-size, y-size, size*2, size*2, pen, brush)
        
        # Draw cross
        cross_pen = QPen(QColor("white"))
        cross_pen.setWidth(max(2, int(2 * zoom_level)))
        scene.addLine(x-size, y, x+size, y, cross_pen)
        scene.addLine(x, y-size, x, y+size, cross_pen)
        
        return node
    
    elif node_type == NodeType.ELASTIC:
        # Elastic: purple circle with springs
        # Draw circle
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setWidth(1)
        brush = QBrush(QColor("purple"), Qt.BrushStyle.SolidPattern)
        node = scene.addEllipse(x-size, y-size, size*2, size*2, pen, brush)
        
        # Draw springs
        spring_pen = QPen(QColor("black"))
        spring_pen.setWidth(max(1, int(zoom_level)))
        
        # Draw diagonal springs
        scene.addLine(x-size*1.6, y-size*1.6, x-size, y-size, spring_pen)
        scene.addLine(x-size*1.6, y+size*1.6, x-size, y+size, spring_pen)
        scene.addLine(x+size*1.6, y-size*1.6, x+size, y-size, spring_pen)
        scene.addLine(x+size*1.6, y+size*1.6, x+size, y+size, spring_pen)
        
        return node
    
    return None

def draw_force(scene, x, y, force_type, value, zoom_level=1.0):
    """Draw a force on the scene with the given type and value"""
    # Base size adjusted for zoom
    base_size = 10
    size = base_size * zoom_level
    
    if force_type == ForceType.POINT:
        # Point force: arrow
        pen = QPen(QColor("red"))
        pen.setWidth(max(2, int(2 * zoom_level)))
        arrow = scene.addLine(x, y, x, y-size*2, pen)
        
        # Add arrowhead
        path = QPainterPath()
        path.moveTo(x, y-size*2)  # Tip
        path.lineTo(x-size*0.5, y-size*1.5)  # Left
        path.lineTo(x+size*0.5, y-size*1.5)  # Right
        path.closeSubpath()
        
        brush = QBrush(QColor("red"), Qt.BrushStyle.SolidPattern)
        scene.addPath(path, pen, brush)
        
        # Add value text
        text = scene.addText(f"{value} kN")
        text.setPos(x+size, y-size*2.5)
        text.setDefaultTextColor(QColor("red"))
        
        return arrow
    
    elif force_type == ForceType.RECTANGLE:
        # Rectangular force: rectangle with arrow
        pen = QPen(QColor("red"))
        pen.setWidth(1)
        brush = QBrush(QColor("red"), Qt.BrushStyle.SolidPattern)
        
        width = size * 2
        height = size * 3
        rect = scene.addRect(x-width/2, y-height, width, height, pen, brush)
        
        # Add value text
        text = scene.addText(f"{value} kN/m")
        text.setPos(x-width/2, y-height-20)
        text.setDefaultTextColor(QColor("black"))
        
        return rect
    
    elif force_type == ForceType.TRIANGLE:
        # Triangular force: triangle
        pen = QPen(QColor("red"))
        pen.setWidth(1)
        brush = QBrush(QColor("red"), Qt.BrushStyle.SolidPattern)
        
        width = size * 2
        height = size * 3
        
        path = QPainterPath()
        path.moveTo(x, y)  # Bottom point
        path.lineTo(x-width/2, y-height)  # Top left
        path.lineTo(x+width/2, y-height)  # Top right
        path.closeSubpath()
        
        return scene.addPath(path, pen, brush)
    
    return None