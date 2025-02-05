### What the project does
A "simple" Python script, which, if run within Blender will read a list[csv file] of stars and convert the angle location [Right Ascension and Declination] in to XYZ-coordinates to plot the stars as 3D objects on a imaginary spherical surface. Creating a celestial sphere.

Be aware, since I do all my work from linux based systems this code is not optimized for windows. Mainly OS relate stuff like paths and file naming conventions.
It is on the to-do list to improve on that.

### Why the project is useful
It is one of my first Python projects, which has taught me a lot and still to this day brings me always back to it to figure more out about the Blender Python API and Python.
This is also my first project published on Github. I hope it can inspire you and help me to learn more.

### How users can get started with the project
Feel free to use the code, improve it. Maybe we can create a Blender Astronomy Plug-In. 

### Where users can get help with your project
For Blender relate stuff check out these links

[https://www.blender.org ](https://www.blender.org/) 

[https://docs.blender.org/api/current/index.html](https://docs.blender.org/api/current/index.html)

For Python stuff as always

[https://www.python.org/](https://www.python.org/)

I'm using these python moduels. 

```python
# --- Imports ---
import bpy # Blender module
import csv
import math
import time # for the perfomance timers, optional
from pathlib import Path # combing file name and path
import os
```

### Who maintains and contributes to the project
[TBD]

### The script

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
