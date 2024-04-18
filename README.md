### What the project does
A "simple" Python script, which, if run within Blender will read a list[csv file] of stars and convert the angle location [Right Ascension and Declination] in to XYZ-coordinates to plot the stars as 3D objects on a imaginary spherical surface. Creating a celestial sphere.

### Why the project is useful
It is one of my first Python projects, which has taught me a lot and still to this day brings me always back to it to figure more out about the Blender Python API and Python.
This is also my first project published on Github. I hope it can inspire you and help me to learn more.

### How users can get started with the project
Feel free to use the code, improve it. Maybe we can create a Blender Astronomy Plug-In. 

### Where users can get help with your project
TBD

### Who maintains and contributes to the project
[TBD]

### The script

Here I will go over the code the explain what is happening. Express ideas and point out problems.
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
