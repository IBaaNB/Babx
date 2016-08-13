# ##### BEGIN MIT LICENSE BLOCK #####
# 
# Copyright (c) 2016 Pleum
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

'''
Babx add-on
Help you to use FBX batch export for use in game engine.
'''

bl_info = {
    "name": "Babx",
    "description": "FBX Batch export helper.",
    "author": "Pleum",
    "version": (1, 0),
    "blender": (2, 77, 0),
    "location": "Tools > Export Tab",
    "warning": "Beta",
    "wiki_url": "https://github.com/pleum/Babx",
    "tracker_url": "https://github.com/pleum/Babx/issues",
    "support": "COMMUNITY",
    "category": "Import-Export"
    }

import bpy
import os

class BabxExportPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Babx"
    bl_label = "Babx Batch Export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Export'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label("FBX Batch export helper.")

        box = layout.box()
        box.label("Select all object you wish.")

        row = box.row()
        row.prop(scene, "babx_export_path", text_ctxt="Export Path")

        box.operator("export.babx")

class BabxExport(bpy.types.Operator):
    """Export your all model."""
    bl_idname = "export.babx"
    bl_label = "Export"
    
    def execute(self, context):
        scene = context.scene

        # Check basedir
        basedir = bpy.path.abspath(scene.babx_export_path) if scene.babx_export_path != "" else os.path.dirname(bpy.data.filepath)

        if not basedir:
            self.report({'ERROR'}, "You must choose export folder or save blend file.")
            return {'CANCELLED'}

        print(basedir)

        # Get active model
        obj_active = scene.objects.active
        selection = context.selected_objects

        bpy.ops.object.select_all(action='DESELECT')

        # Start export
        for obj in selection:
            obj.select = True

            # Get current loc, rot
            last_loc = obj.location.xyz
            last_rot_x = obj.rotation_euler.x
            last_rot_y = obj.rotation_euler.y
            last_rot_z = obj.rotation_euler.z
            
            # Reset loc, rot to zero
            obj.location = (0, 0, 0)
            obj.rotation_euler = (0, 0, 0)

            scene.objects.active = obj

            name = bpy.path.clean_name(obj.name)
            fn = os.path.join(basedir, name)
            
            # Export current fbx
            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, object_types={'MESH'})

            # Back to last current loc, rot
            obj.location = last_loc
            obj.rotation_euler = (last_rot_x, last_rot_y, last_rot_z)

            obj.select = False
        
        scene.objects.active = obj_active

        for obj in selection:
            obj.select = True

        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.babx_export_path = bpy.props.StringProperty(name="Export Path", description="FBX Export folder", subtype='DIR_PATH')
    
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.babx_export_path

if __name__ == "__main__":
    register()
