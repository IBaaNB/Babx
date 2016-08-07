import bpy
import os

basedir = os.path.dirname(bpy.data.filepath)

if not basedir:
  raise Exception("Blend file is not saved")

scene = bpy.context.scene

obj_active = scene.objects.active
selection = bpy.context.selected_objects

bpy.ops.object.select_all(action='DESELECT')

for obj in selection:

  obj.select = True
    
  last_loc = obj.location.xyz
  last_rot_x = obj.rotation_euler.x
  last_rot_y = obj.rotation_euler.y
  last_rot_z = obj.rotation_euler.z

  obj.location = (0, 0, 0)
  obj.rotation_euler = (0, 0, 0)

  scene.objects.active = obj

  name = bpy.path.clean_name(obj.name)
  fn = os.path.join(basedir, name)

  bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, object_types={'MESH'})
    
  obj.location = last_loc
  obj.rotation_euler = (last_rot_x, last_rot_y, last_rot_z)
    
  obj.select = False
    
  print("written:", fn)


scene.objects.active = obj_active

for obj in selection:
    obj.select = True
