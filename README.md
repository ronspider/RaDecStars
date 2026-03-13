# Celestial Sphere Blender Script

## Overview

This is a Python script designed to run within Blender that reads a CSV file containing star data and converts celestial coordinates (Right Ascension and Declination) into 3D XYZ coordinates. The script then plots these stars as 3D objects on an imaginary spherical surface, creating a visual celestial sphere.

## Features

- Converts Right Ascension and Declination to 3D XYZ coordinates
- Creates a celestial sphere visualization in Blender
- Reads star data from CSV files
- Simple and lightweight implementation

## ⚠️ Platform Note

This code was developed primarily on Linux-based systems. While the core functionality should work across platforms, there may be OS-related issues with file paths and naming conventions on Windows. Cross-platform compatibility improvements are planned for future releases.

## Why This Project Exists

This was one of my first Python projects and has been an invaluable learning experience. It continues to serve as a reference point for deepening my understanding of:

- The Blender Python API
- Python programming fundamentals
- Astronomical coordinate systems

As my first project published on GitHub, I hope it inspires others and contributes to collaborative learning.

## Getting Started

### Requirements

- Blender (with Python scripting support)
- Python modules (see below)

### Usage

1. Place the script in your Blender scripts directory or run it directly within Blender's Text Editor
2. Prepare a CSV file with star data (Right Ascension and Declination columns)
3. Run the script to generate the celestial sphere

### Python Modules Used
```python
# --- Imports ---
import bpy # Blender module
import csv
import math
import time # for the perfomance timers, optional
from pathlib import Path # combing file name and path
import os
```
*Please refer to the original repository for the complete list of dependencies.*

## Contributing

Feel free to:
- Use the code for your own projects
- Submit improvements or bug fixes
- Collaborate on expanding functionality

There's potential to evolve this into a full-fledged Blender Astronomy Plugin—contributions welcome!

## Getting Help

### Blender Resources
- [Blender Official](https://www.blender.org)
- [Blender Python API Documentation](https://docs.blender.org/api/current/index.html)

### Python Resources
- [Python Official Website](https://www.python.org/)

---

*This project is open source and welcomes community contributions. Happy stargazing! 🌟*



## Notes
Here I will go over the code and explain what is does. Express ideas and point out problems.
And, yes I'm a noob. 

#### Functions

```python
# Getting Star Name
def star_name_conv(name, ID):
    if name == "":
        return ID
    else: 
        return name
```
#### Blender

Here is the actual interaction with Blender.
```python
    # blender_draw(s, x, y, z, star_name, name):
    # def blender_draw(vmag, mag_limit, con_limit, s, x, y, z, star_name, name):
    # Blender commands
    bpy.ops.mesh.primitive_uv_sphere_add(segments=4, ring_count=4, radius=s, enter_editmode=False, location=(x, y, z))
    bpy.ops.object.move_to_collection(collection_index=stell) # Move star into correct collection [Index number, Experimental]
    for obj in bpy.context.selected_objects:
        obj.name = star_name + "_" + sptype 
        if name != "":
            bpy.context.object.show_name = True
```
This line I added so the display gets updated. Something to see in the Blender 3D view port besides the terminal output.
```python
    # Update the 3D- View Ports
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
```
