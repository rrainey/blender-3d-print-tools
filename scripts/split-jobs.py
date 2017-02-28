# A Blender script for slicing a large object into smaller objects suitable for 
# individual 3D print jobs.
#
# Designed for a MakerBot Replictor 2 (adaptable for others)
#
# This script assumes the scale of your Blender model is in millimeters (Makerbot native)
# The script slices along YZ-plane by moving along the X-axis at roughly 6-inch intervals
# Each slice is exported as an STL file.
#
# Usage:
#   Select the object to be "sliced". 
#   Open a Text Editor windor, load this script. 
#   Run this script.
#
# Copyright (c) 2017, Riley B Rainey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import bpy
import os.path 
home = os.path.expanduser("~")

base_mm = -850 # X-coordinate of base of model
incr_mm = 6*25 # 6 * 25.4mm; interval between slices
i=1
objname="blade"

scn = bpy.context.scene
src_obj = bpy.context.active_object
src_obj.select = False

new_obj1 = src_obj.copy()
new_obj1.data = src_obj.data.copy()
# select newobj1
scn.objects.link(new_obj1)
scn.objects.active = new_obj1
new_obj1.select = True
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
bpy.ops.mesh.reveal()
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bisect(plane_co=(base_mm + incr_mm*i, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0), use_fill=True, 
	clear_inner=False, clear_outer=True, threshold=0.0001, xstart=0, xend=0, ystart=0, yend=0, cursor=1002)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
# now export (switch "up" axis to X)
basename= os.path.join(home, objname + "%02d" % i + ".stl")
bpy.ops.export_mesh.stl(filepath=basename, check_existing=False, axis_forward='Y', axis_up='X', 
	filter_glob="*.stl", use_selection=True, global_scale=1.0, 
	use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OFF')
new_obj1.select = False

rem_obj = src_obj.copy()
rem_obj.data = src_obj.data.copy()
scn.objects.link(rem_obj)
scn.objects.active = rem_obj
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
bpy.ops.mesh.reveal()
bpy.ops.mesh.select_all(action='SELECT')
# select rem_obj
bpy.ops.mesh.bisect(plane_co=(base_mm + incr_mm*i, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0), use_fill=True, clear_inner=True, 
	clear_outer=False, threshold=0.0001, xstart=0, xend=0, ystart=0, yend=0, cursor=1002)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
rem_obj.select = False

for i in range (2,11):
	new_obj1 = rem_obj.copy()
	new_obj1.data = rem_obj.data.copy()
    # select newobj1
	scn.objects.link(new_obj1)
	scn.objects.active = new_obj1
	new_obj1.select = True
	
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	bpy.ops.mesh.reveal()
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.bisect(plane_co=(base_mm + incr_mm*i, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0), use_fill=True, clear_inner=False, 
		clear_outer=True, threshold=0.0001, xstart=0, xend=0, ystart=0, yend=0, cursor=1002)
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	basename= os.path.join(home, objname + "%02d" % i + ".stl")
	bpy.ops.export_mesh.stl(filepath=basename, check_existing=False, axis_forward='Y', axis_up='X', 
		filter_glob="*.stl", use_selection=True, global_scale=1.0, 
		use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OFF')
	new_obj1.select = False
	
	# select rem_obj
	scn.objects.active = rem_obj
	rem_obj.select = True
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	bpy.ops.mesh.reveal()
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.bisect(plane_co=(base_mm + incr_mm*i, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0), use_fill=True, clear_inner=True, 
		clear_outer=False, threshold=0.0001, xstart=0, xend=0, ystart=0, yend=0, cursor=1002)
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	rem_obj.select = False
	
basename= os.path.join(home, objname + "%02d" % i + ".stl")
bpy.ops.export_mesh.stl(filepath=basename, check_existing=False, axis_forward='Y', axis_up='X', 
	filter_glob="*.stl", use_selection=True, global_scale=1.0, 
	use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OFF')