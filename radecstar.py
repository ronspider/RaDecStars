# File: radecstar.py
# Name: "Right Ascension Declination Star" Version 1.1
# 2023 by RS [test]

# --- Information, Rescouces ---
# Run this script in Blender
# https://www.blender.org/


# https://www.johnpAratt.com/items/astronomy/mag_5_stars.html
# Add to mag_5_stars.csv file:
# HR 424 Polaris https://en.wikipedia.org/wiki/Polaris [for better oriantation, northern hemnis., experimental]
# HR 1607 Hind's Crimson Star https://en.wikipedia.org/wiki/R_Leporis [my favorit star, experimental]

# --- Imports ---
import bpy # Blender module
import csv
import math
import time # for the perfomance timers, optional
from pathlib import Path # combing file name and path
import os

# --- Globals ---
star_amount = 3000 # lines to read from the CVS file [current has 3922]
size = 10 # projection sphere size
# mag_limit = 4.5 # [experimantel] 
# con_limit = "Cas" # [experimantel]


# --- Functions ---
# Function, Getting Star Name
def star_name_conv(name, ID):
    if name == "":
        return ID
    else:
        return name


# Function, Ranger Mapper
# a = in range min, b = in range max
# c = out range min, d = out range max
def range_map(val_in, a, b, c, d):
    val_out = (val_in - a) / (b - a) * (d - c) + c

    return(val_out)


# Function, Converting magnitut [brightness] to size
def mag_conv(mag_val):
    mag_out_val = range_map(mag_val, 5.5, -3.0, 0.001, 0.1)

    return(mag_out_val)


# Function, Converting Right Ascension to float angle
def ra_conv(ra, ram, ras):
    ra_ang = ra + ram / 60 + ras / 3600
    ra_val = range_map(ra_ang, 0, 24, 0, 360)

    return(ra_val)


# Function, Converting Declination to float angle
def dec_conv(dec, decm, decs, ns):
    if ns == "S":
        dec_ang = dec + decm / 60 + decs / 3600
    else:
        dec_ang = (dec + decm / 60 + decs / 3600) * -1
        
    dec_val = range_map(dec_ang, -90, 90, 0, 180)

    return(dec_val)

# Function, Assigning Stellar Classification [experimental]
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


# Function, Dummy sphere [experimental]
# def cle_sphere(rad): 
#     bpy.ops.mesh.primitive_uv_sphere_add(segments=4, ring_count=4, radius=rad, enter_editmode=False, location=(0, 0, 0))
#     for obj in bpy.context.selected_objects:
#         obj.name = "00_Celestrial_Sphere"
#         bpy.ops.object.shade_smooth()


# --- Main ---
# Creating Collection for star classes [https://en.wikipedia.org/wiki/Stellar_classification]
# Before running the script, delete default collection to keep index start at 0 = O_Stars
# Stella Classification: O, B, A, F, G, K, and M,
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="O_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="B_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="A_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="F_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="G_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="K_stars")
bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="M_stars")

# Main, reading csv file
data_folder = Path("/home/spider/RaDecStars/") # In Linux just change the name 'spider' to yours 
file_to_open = data_folder / "mag_5_stars.csv" # make sure this script and the 'mag_5_stars.csv' file are in the same folder
file = open(file_to_open)
star_file = csv.DictReader(file)

# Main, loop
for i in range(0,star_amount):
    tic = time.perf_counter() # Start performance timer
    i = i + 1 # I know i += 1
    row1 = next(star_file)
    
    # assigning column values to variables
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
    
    toc_a = time.perf_counter() # Set "a" performance timer check point
    
    # Passing variables to the Functions
    star_name = star_name_conv(name, ID)
    mag_out_val = mag_conv(vmag)
    ra_val = ra_conv(ra, ram, ras)
    dec_val = dec_conv(dec, decm, decs, ns)
    stell = stellar_class(sptype) # [experimental]
    
    # RA to Radians
    ra_rad = math.radians(ra_val)
    # DEC to Radians
    de_rad = math.radians(dec_val)
    
    # Angles to x,y,z - The real magic/math happens here
    r = size # assigning projection sphere size [global]
    x = r * math.sin(de_rad) * math.cos(ra_rad) # Blender Position X
    y = r * math.sin(de_rad) * math.sin(ra_rad) # Blender Position Y
    z = r * math.cos(de_rad)                    # Blender Position Z
    
    s = mag_out_val # Blender Size, Star size, based on it's brighness
    
    toc_b = time.perf_counter() # Set "b" performance timer check point
    
    # blender_draw(s, x, y, z, star_name, name):
    # def blender_draw(vmag, mag_limit, con_limit, s, x, y, z, star_name, name):
    # Blender commands
    bpy.ops.mesh.primitive_uv_sphere_add(segments=4, ring_count=4, radius=s, enter_editmode=False, location=(x, y, z))
    bpy.ops.object.move_to_collection(collection_index=stell) # Move star into correct collection [Index number, Experimental]
    for obj in bpy.context.selected_objects:
        obj.name = star_name + "_" + sptype 
        if name != "":
            bpy.context.object.show_name = True
    
    toc_c = time.perf_counter() # Set "c" performance time check point
    
    # --- Terminal feedback ---
    os.system('clear')
    print("------------ Job: " + str(i) + " of " + str(star_amount) + (f" in {toc_c - tic:0.4f} seconds -------------"))
    print(f"Read CVS line in                 {toc_a - tic:0.4f} seconds.")
    print(f"Converted and drawn in           {toc_c - toc_a:0.4f} seconds.")
    print(f"Drawn in                         {toc_c - toc_b:0.4f} seconds.")
    print(id, name, ID, ra, ram, ras, ns, dec, decm, decs, vmag, sptype)
    print("ra_val  = " + str(round(ra_val,5)))
    print("dec_val = " + str(round(dec_val,5)))
    print("   x    = " + str(round(x,5)))
    print("   y    = " + str(round(y,5)))
    print("   z    = " + str(round(z,5)))
    print("   s    = " + str(round(s,5)))

# Note: this loop slows down.

    
