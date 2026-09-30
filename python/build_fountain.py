import os
from PIL import Image

# Palette definition
PALETTE = {
    ".": (0, 0, 0, 0),
    "#": (43, 38, 54, 255),    # #2b2636 Soft dark slate outline
    "S": (26, 22, 36, 130),    # #1a1624 Contact ground shadow (alpha 130)
    
    # Marble shades
    "H": (245, 245, 247, 255), # Specular ivory highlight
    "L": (216, 220, 230, 255), # Bright marble
    "M": (157, 162, 181, 255), # Midtone marble
    "D": (107, 112, 134, 255), # Shadow marble
    "V": (67, 72, 92, 255),    # Deep crevice / inner basin shadow
    
    # Water shades (exception palette)
    "W": (255, 255, 255, 255), # Foam crest / bubble / water glint
    "A": (110, 226, 255, 255), # Light cyan spray / ripple highlight
    "B": (0, 170, 255, 255),   # #00aaff Vibrant water stream / surface
    "C": (12, 107, 168, 255),  # Deep water shade / pool depth
}

print("Base setup ready")
