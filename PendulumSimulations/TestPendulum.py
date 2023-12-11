import bpy
import numpy as np
import mathutils
import random
import time
import glob

import subprocess
import sys
import os
 
# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
 
# upgrade pip
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
 
# install required packages
subprocess.call([python_exe, "-m", "pip", "install", "scipy"])

from scipy.integrate import odeint

sim_time = 10.0

def pend(y, t, b, c):
    theta, omega = y
    dydt = [omega, -b*omega - c*np.sin(theta)]
    return dydt

FPS = 24

bpy.context.scene.frame_end = sim_time * FPS

bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0.0, -10.0, 2), rotation=(np.pi/2-np.pi/20,0.0,0.0), scale=(1, 1, 1))

material_array = ["Black marble ceramics", 
    "Brick Pavement Gray Green  Wall",     "Carbon FIber",
    "Colored Crystal Glass",
    "Duct tape",
    "Green woven carpet",
    "Procedural Edgewear Mask With Scratches",
    "Sand colored ceramic floor"]

bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.ops.transform.resize(value=(37.1368, 37.1368, 37.1368), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=True, proportional_edit_falloff='SMOOTH', proportional_size=0.239392, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
bpy.context.object.data.materials.append(bpy.data.materials.get("Sand colored ceramic floor"))

for i in range(8):
    bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(-10*np.sin(np.pi*2*i/8), -10*np.cos(np.pi*2*i/8), 10-(5/4)*(4-i)), scale=(1, 1, 1))
    bpy.context.object.data.energy = 50-(50-8)*i


def set_blenderkit_material(object_name, material_url):
    bpy.data.window_managers["WinMan"].blenderkitUI.asset_type = 'MATERIAL'
    
    bpy.data.window_managers["WinMan"].blenderkit_mat.search_keywords = material_url
    
    bpy.ops.view3d.blenderkit_asset_bar_widget(do_search=False, keep_running=True)
    bpy.ops.view3d.blenderkit_asset_bar_widget(do_search=False, keep_running=True)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.material_slot_select()
    bpy.ops.uv.cube_project(cube_size=1, correct_aspect=False)
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.scene.blenderkit_download(asset_index=0, target_object=object_name, material_target_slot=0, model_location=(-0.000143051, 0.138622, 1), model_rotation=(0, 0, 0))
    
def set_material(object_name, material):
    bpy.data.objects[object_name].data.materials.append(material)


def draw_pendulum(number = 0, theta1=0,theta2=0, starting_position=mathutils.Vector((0.0,0.0,0.0))):
    bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
    
    bpy.ops.wm.obj_import(filepath=os.path.abspath("FreeCADModels/Pendulum/FirstLinkage.obj"))
    
    bpy.ops.transform.resize(value=(0.001, 0.001, 0.001))
    
    bpy.context.object.location = starting_position
    
    bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
    
    bpy.ops.transform.rotate(value=-np.pi/2, orient_axis='Z', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 7.54979e-08, 1), (0, -1, 7.54979e-08)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.ops.transform.rotate(value=theta1, orient_axis='Z', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 7.54979e-08, 1), (0, -1, 7.54979e-08)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    bpy.context.object.keyframe_insert(data_path="location", frame=1)
    bpy.context.object.keyframe_insert(data_path="rotation_euler", frame=1)
    bpy.context.object.keyframe_insert(data_path="scale", frame=1)
    bpy.ops.transform.rotate(value=-theta1, orient_axis='Z', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 7.54979e-08, 1), (0, -1, 7.54979e-08)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    
    y0 = [theta1, 0.0]
    t = np.linspace(0, sim_time, bpy.context.scene.frame_end)
    sol = odeint(pend, y0, t, args=(0.25, 5.0))
    
    for i, y_curr in enumerate(sol):
        bpy.ops.transform.rotate(value=y_curr[0], orient_axis='Z', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 7.54979e-08, 1), (0, -1, 7.54979e-08)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.context.object.keyframe_insert(data_path="location", frame=i)
        bpy.context.object.keyframe_insert(data_path="rotation_euler", frame=i)
        bpy.context.object.keyframe_insert(data_path="scale", frame=i)
        bpy.ops.transform.rotate(value=-y_curr[0], orient_axis='Z', orient_type='LOCAL', orient_matrix=((1, 0, 0), (0, 7.54979e-08, 1), (0, -1, 7.54979e-08)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
    
    bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
    
    bpy.context.object.name = "Pendulum" + str(number)
    
    set_material("Pendulum" + str(number), bpy.data.materials.get(random.choice(material_array)))
    
    
dx = 1
dy = 0.5
dz = 0.3
rows = 3
columns = 3


for x in range(columns):
    for y in range(rows):
        current_position = mathutils.Vector((dx*(columns//2-x), dy*(y), 1.27+y*dz))
        draw_pendulum(str(x)+"_"+str(y), random.uniform(0, 2*np.pi), random.uniform(0, 2*np.pi), current_position)