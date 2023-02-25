# File: radecstar.py 
# Name: "Right Ascension Declination Star" Version 1.1

# (c)2023 by Ron Spider, rspaida@gmail.com, [test]

# https://www.johnpAratt.com/items/astronomy/mag_5_stars.html
# Add to mag_5_stars.csv file: 
# Polaris https://en.wikipedia.org/wiki/Polaris
# Hind's Crimson Star https://en.wikipedia.org/wiki/R_Leporis

# --- Imports ---
import bpy
import csv
import math
import time
from pathlib import Path
# import pandas as pd

# --- Globals ---
star_amount = 3000 # line to read from the CVS file
size = 10
# mag_limit = 4.5
# con_limit = "Cas"


# --- Functions ---
# Getting Star Name
def star_name_conv(name, ID):
    if name == "":
        return ID
    else: 
        return name
    

# Ranger Mapper
# a = in range min, b = in range max
# c = out range min, d = out range max
def range_map(val_in, a, b, c, d):
    val_out = (val_in - a) / (b - a) * (d - c) + c
    
    return(val_out)


# Converting magnitut to size
def mag_conv(mag_val):
    mag_out_val = range_map(mag_val, 5.5, -3.0, 0.001, 0.1)
    
    return(mag_out_val)
    

# Converting Right Ascension to float angle 
def ra_conv(ra, ram, ras):
    ra_ang = ra + ram / 60 + ras / 3600
    ra_val = range_map(ra_ang, 0, 24, 0, 360)
        
    return(ra_val)


# Converting Declination to float angle
def dec_conv(dec, decm, decs, ns):
    if ns == "S":
        dec_ang = dec + decm / 60 + decs / 3600
    else:
        dec_ang = (dec + decm / 60 + decs / 3600) * -1
    dec_val = range_map(dec_ang, -90, 90, 0, 180)
    
    return(dec_val)
  
# Assigning Stellar Classification
def stellar_class(stel):
    c_index = 0
    c = stel[:1]
    if c == "O":
        c_index = 0
    elif c == "B":
        c_index = 1
    elif c == "A":
        c_index = 2
    elif c == "F":
        c_index = 3
    elif c == "G":
        c_index = 4
    elif c == "K":
        c_index = 5
    elif c == "M":
        c_index = 6            
    
    return c_index


# def cle_sphere(rad):
#     bpy.ops.mesh.primitive_uv_sphere_add(segments=4, ring_count=4, radius=rad, enter_editmode=False, location=(0, 0, 0))
#     for obj in bpy.context.selected_objects:
#         obj.name = "00_Celestrial_Sphere"
#         bpy.ops.object.shade_smooth()


# --- Main ---
# Creating Collection for star classes [https://en.wikipedia.org/wiki/Stellar_classification]
# Delete default collection to keep index start at 0 = O_Stars
# Stella Classification: O, B, A, F, G, K, and M,
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="O_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="B_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="A_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="F_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="G_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="K_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="M_stars")

# main loop, reading file
data_folder = Path("C:\\Users\\ronny\\Documents\\Blender\\Blender_Stars")
file_to_open = data_folder / "mag_5_stars.csv"
file = open(file_to_open)
star_file = csv.DictReader(file)

for i in range(0,star_amount):
    tic = time.perf_counter() # Set first timer counter
    i = i + 1
    row1 = next(star_file)

    id = row1[' HR']
    name = str(row1['Name'])
    ID = str(row1['ID'])
    con = str(row1['Con'])
    ra = float(row1['RA'])
    ram = float(row1['RAm'])
    ras = float(row1['RAs'])
    ns = str(row1['NS'])
    dec = float(row1['Dec'])
    decm = float(row1['Dm'])
    decs = float(row1['Ds'])
    vmag = float(row1['Vmag'])
    sptype = str(row1['Sp Type'])
    
    toc_a = time.perf_counter() # Set "a" timer count
    
    star_name = star_name_conv(name, ID)
    mag_out_val = mag_conv(vmag)
    ra_val = ra_conv(ra, ram, ras)
    dec_val = dec_conv(dec, decm, decs, ns)
    stell = stellar_class(sptype)
    
    # RA to Radians
    ra_rad = math.radians(ra_val)
    # DEC to Radians
    de_rad = math.radians(dec_val)
    
    # Angles to x,y,z
    r = size # projection sphere size
    x = r * math.sin(de_rad) * math.cos(ra_rad)
    y = r * math.sin(de_rad) * math.sin(ra_rad)
    z = r * math.cos(de_rad)
    
    s = mag_out_val
    
    toc_b = time.perf_counter() # Set "b" timer count
    
    # blender_draw(s, x, y, z, star_name, name):
    # def blender_draw(vmag, mag_limit, con_limit, s, x, y, z, star_name, name):
    # Blender commands
    # if vmag < mag_limit and con == con_limit:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=4, ring_count=4, radius=s, enter_editmode=False, location=(x, y, z))
    bpy.ops.object.move_to_collection(collection_index=stell) # Move star into correct collection [Index number]
    for obj in bpy.context.selected_objects:
        obj.name = star_name + "_" + sptype 
        if name != "":
            bpy.context.object.show_name = True
    
    toc_c = time.perf_counter() # Set "c" timer count
    
    # --- Terminal feed back ---
    print("------------ Job: " + str(i) + " of " + str(star_amount) + (f" in {toc_c - tic:0.4f} seconds -------------"))
    print(f"Read CVS line in              {toc_a - tic:0.4f} seconds.")
    print(f"Converted and drawn in        {toc_c - toc_a:0.4f} seconds.")
    print(f"Drawn in                      {toc_c - toc_b:0.4f} seconds.")
    print(id, name, ID, ra, ram, ras, ns, dec, decm, decs, vmag, sptype)
    print("ra_val = " + str(round(ra_val,5)))
    print("dec_val = " + str(round(dec_val,5)))
    print("x = " + str(round(x,5)))
    print("y = " + str(round(y,5)))
    print("z = " + str(round(z,5)))
    print("s = " + str(round(s,5)))

    # else:
    #    print(f"Job {i} skipped")

    
