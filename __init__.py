"""
Blender Add-on: Tattoo Master for inZOI
Automates workflow for applying high-quality tattoos on MetaHuman meshes (body and head)
using texture painting in Stencil mode, ensuring compatibility with Unreal Engine export.
"""

import bpy
import os
import importlib
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator, Panel, AddonPreferences
from bpy_extras.io_utils import ImportHelper, ExportHelper
from . import helpers
from . import brush_manager
from . import preferences

# Force reload of submodules to ensure changes are picked up
importlib.reload(helpers)
importlib.reload(brush_manager)
importlib.reload(preferences)


bl_info = {
    "name": "Tattoo Master inZOI",
    "author": "TRESDTRES",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tattoo Studio",
    "description": "Automates tattoo application on inZOI characters using Stencil painting",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}


class TATTOO_OT_import_metahuman_fbx(Operator, ImportHelper):
    """Import inZOI FBX and set up automatic material"""
    bl_idname = "tattoo.import_metahuman_fbx"
    bl_label = "Import inZOI FBX"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".fbx"
    filter_glob: StringProperty(default="*.fbx", options={'HIDDEN'})

    # Additional property for texture path
    texture_path: StringProperty(
        name="Base Color Texture",
        description="Path to the base color texture (T_body_BC.*)",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        # Force Viewport to SOLID mode to prevent GPU driver crashes during heavy import
        # This avoids the GPU trying to render complex shaders while geometry is being processed
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'SOLID'

        # Import FBX
        filepath = self.filepath
        if not filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}

        # Import the FBX file
        # Optimized for static meshes (Skin only, no bones)
        bpy.ops.import_scene.fbx(
            filepath=filepath,
            use_anim=False,
            ignore_leaf_bones=True,
            force_connect_children=False,
            use_custom_normals=False,  # Changed to False to prevent viewport crashes
            use_image_search=False     # Prevent hangs searching for missing textures
        )

        context.view_layer.update()

        # Find the imported body object
        body_obj = helpers.get_inzoi_body_object()
        if not body_obj:
            self.report({'WARNING'}, "No body object found in imported FBX")
            return {'CANCELLED'}

        # Ensure UV map exists (required for texture painting)
        if not body_obj.data.uv_layers:
            body_obj.data.uv_layers.new(name="UVMap")

        # Create material with texture
        material = helpers.create_character_material(body_obj, self.texture_path if self.texture_path else "")

        self.report({'INFO'}, f"Imported inZOI FBX and created material for {body_obj.name}")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Set the default directory from preferences if available
        try:
            addon_prefs = context.preferences.addons.get(__package__)
            if addon_prefs and addon_prefs.preferences.default_export_path:
                self.filepath = addon_prefs.preferences.default_export_path
        except:
            pass  # Use default path if preferences not available

        # Call the original invoke
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


class TATTOO_OT_resize_texture_to_4k(Operator):
    """Resize the active texture to 4K resolution"""
    bl_idname = "tattoo.resize_texture_to_4k"
    bl_label = "Resize Texture to 4K"

    def execute(self, context):
        obj = context.active_object
        if not obj or not obj.active_material:
            self.report({'ERROR'}, "No active object with material selected")
            return {'CANCELLED'}

        image_node = helpers.get_active_image_texture_node(obj)
        if not image_node or not image_node.image:
            self.report({'ERROR'}, "No image texture found in active material")
            return {'CANCELLED'}

        image = image_node.image
        # Check if image has valid dimensions
        if image.size[0] == 0 or image.size[1] == 0:
            self.report({'ERROR'}, "Invalid image dimensions - image may not be loaded properly")
            return {'CANCELLED'}

        current_size = max(image.size[0], image.size[1])

        # Get target resolution from preferences
        try:
            addon_prefs = context.preferences.addons.get(__package__)
            if addon_prefs:
                target_resolution = addon_prefs.preferences.default_resolution
            else:
                target_resolution = 4096  # Default to 4K
        except:
            target_resolution = 4096  # Default to 4K in case of error

        if current_size >= target_resolution:
            self.report({'INFO'}, f"Texture is already {current_size}x{current_size}, no resize needed")
            return {'FINISHED'}

        # Resize the image to target resolution
        image.scale(target_resolution, target_resolution)

        self.report({'INFO'}, f"Resized texture from {current_size}x{current_size} to {target_resolution}x{target_resolution}")
        return {'FINISHED'}


class TATTOO_OT_setup_tattoo_brush(Operator):
    """Setup the tattoo brush with stencil mode"""
    bl_idname = "tattoo.setup_tattoo_brush"
    bl_label = "Setup Tattoo Brush"

    def execute(self, context):
        try:
            brush = brush_manager.setup_tattoo_brush()
            self.report({'INFO'}, "Tattoo brush configured with stencil mode")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


class TATTOO_OT_load_tattoo_image(Operator, ImportHelper):
    """Load a tattoo image for the stencil brush"""
    bl_idname = "tattoo.load_tattoo_image"
    bl_label = "Load Tattoo Image"

    filename_ext = ".png;.jpg;.jpeg;.tga;.bmp"
    filter_glob: StringProperty(default="*.png;*.jpg;*.jpeg;*.tga;*.bmp", options={'HIDDEN'})

    auto_resize: BoolProperty(
        name="Auto-Resize to 4K",
        description="Resize image to 4K maintaining aspect ratio to prevent pixelation",
        default=True
    )

    def execute(self, context):
        filepath = self.filepath
        if not filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}

        try:
            brush, image = brush_manager.load_tattoo_image(filepath, self.auto_resize)
            
            # Warning if image is small and resize was disabled
            if not self.auto_resize and max(image.size) < 4096:
                self.report({'WARNING'}, f"Low resolution image ({image.size[0]}x{image.size[1]}). 4K is recommended.")
            
            self.report({'INFO'}, f"Loaded tattoo image: {os.path.basename(filepath)}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

    def invoke(self, context, event):
        # Set the default directory from preferences if available
        try:
            addon_prefs = context.preferences.addons.get(__package__)
            if addon_prefs and addon_prefs.preferences.default_texture_path:
                self.filepath = addon_prefs.preferences.default_texture_path
        except:
            pass

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class TATTOO_OT_rotate_stencil(Operator):
    """Rotate the tattoo stencil by 90 degrees"""
    bl_idname = "tattoo.rotate_stencil"
    bl_label = "Rotate Stencil 90°"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        import math
        
        if context.mode != 'PAINT_TEXTURE':
            self.report({'WARNING'}, "Must be in Texture Paint mode")
            return {'CANCELLED'}

        brush = context.tool_settings.image_paint.brush
        if not brush or not brush.texture_slot:
            self.report({'WARNING'}, "No active brush or texture slot found")
            return {'CANCELLED'}

        # Rotate by 90 degrees (pi/2 radians)
        brush.texture_slot.angle += (math.pi / 2)
        
        return {'FINISHED'}


class TATTOO_OT_export_tattooed_texture(Operator, ExportHelper):
    """Export the tattooed texture"""
    bl_idname = "tattoo.export_tattooed_texture"
    bl_label = "Export Tattooed Texture"

    filename_ext = ".png"
    filter_glob: StringProperty(default="*.png;*.tga", options={'HIDDEN'})

    # Define the file type
    file_type: EnumProperty(
        name="Format",
        description="Choose the file format for export",
        items=[
            ('png', "PNG", "Export as PNG format"),
            ('tga', "TGA", "Export as TGA format")
        ],
        default='png'
    )

    def execute(self, context):
        obj = context.active_object
        if not obj or not obj.active_material:
            self.report({'ERROR'}, "No active object with material selected")
            return {'CANCELLED'}

        image_node = helpers.get_active_image_texture_node(obj)
        if not image_node or not image_node.image:
            self.report({'ERROR'}, "No image texture found in active material")
            return {'CANCELLED'}

        image = image_node.image

        # Set the file extension based on user choice
        if self.file_type == 'png':
            filepath = self.filepath
            if not filepath.endswith('.png'):
                filepath += '.png'
        else:  # TGA
            filepath = self.filepath
            if not filepath.endswith('.tga'):
                filepath += '.tga'

        # Save the image
        image.filepath_raw = filepath
        image.file_format = 'PNG' if self.file_type == 'png' else 'TARGA'
        image.save()

        self.report({'INFO'}, f"Exported tattooed texture to: {filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Set the default directory from preferences if available
        try:
            addon_prefs = context.preferences.addons.get(__package__)
            if addon_prefs and addon_prefs.preferences.default_export_path:
                self.filepath = addon_prefs.preferences.default_export_path
        except:
            pass  # Use default path if preferences not available

        # Call the original invoke
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


class TATTOO_OT_export_usd(Operator, ExportHelper):
    """Export the mesh and textures as USD for UE5"""
    bl_idname = "tattoo.export_usd"
    bl_label = "Export USD (UE5)"

    filename_ext = ".usdc"
    filter_glob: StringProperty(default="*.usdc;*.usda", options={'HIDDEN'})

    auto_save_textures: BoolProperty(
        name="Auto-Save Textures",
        description="Save dirty textures before exporting",
        default=True
    )

    def execute(self, context):
        if not context.active_object:
            self.report({'ERROR'}, "No active object selected")
            return {'CANCELLED'}

        # Ensure we are in Object Mode
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Auto-save texture before export
        if self.auto_save_textures:
            obj = context.active_object
            image_node = helpers.get_active_image_texture_node(obj)
            if image_node and image_node.image and image_node.image.is_dirty:
                try:
                    image_node.image.save()
                    self.report({'INFO'}, f"Auto-saved texture: {image_node.image.name}")
                except Exception as e:
                    self.report({'WARNING'}, f"Could not auto-save texture: {str(e)}")

        # Export USD with settings optimized for UE5
        bpy.ops.wm.usd_export(
            filepath=self.filepath,
            selected_objects_only=True,
            export_materials=True,
            export_textures=True,
            relative_paths=True
        )

        self.report({'INFO'}, f"Exported USD to: {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Set default from preferences
        try:
            addon_prefs = context.preferences.addons.get(__package__)
            if addon_prefs:
                self.auto_save_textures = addon_prefs.preferences.auto_save_textures
                if addon_prefs.preferences.default_export_path:
                    self.filepath = addon_prefs.preferences.default_export_path
        except:
            pass

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class TATTOO_OT_select_body(Operator):
    """Select the inZOI body object"""
    bl_idname = "tattoo.select_body"
    bl_label = "Select Body"
    bl_description = "Select the inZOI body mesh"

    def execute(self, context):
        body_obj = helpers.get_inzoi_body_object()
        if body_obj:
            helpers.switch_to_mesh(body_obj.name)
            self.report({'INFO'}, f"Selected body: {body_obj.name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No body object found")
            return {'CANCELLED'}


class TATTOO_OT_select_head(Operator):
    """Select the inZOI head object"""
    bl_idname = "tattoo.select_head"
    bl_label = "Select Head"
    bl_description = "Select the inZOI head mesh"

    def execute(self, context):
        head_obj = helpers.get_inzoi_head_object()
        if head_obj:
            helpers.switch_to_mesh(head_obj.name)
            self.report({'INFO'}, f"Selected head: {head_obj.name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No head object found")
            return {'CANCELLED'}


class TATTOO_OT_select_object(Operator):
    """Select a specific object"""
    bl_idname = "tattoo.select_object"
    bl_label = "Select Object"
    bl_description = "Select a specific object"

    object_name: StringProperty(
        name="Object Name",
        description="Name of the object to select",
        default=""
    )

    def execute(self, context):
        if not self.object_name:
            self.report({'ERROR'}, "No object name specified")
            return {'CANCELLED'}

        obj = bpy.data.objects.get(self.object_name)
        if obj and obj.type == 'MESH':
            helpers.switch_to_mesh(obj.name)
            # Try to create material if it doesn't exist
            if not obj.active_material:
                helpers.create_character_material(obj)
            self.report({'INFO'}, f"Selected: {obj.name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Object '{self.object_name}' not found or not a mesh")
            return {'CANCELLED'}


class TATTOO_OT_load_skin_texture(Operator, ImportHelper):
    """Load a skin texture image and apply it to the active object"""
    bl_idname = "tattoo.load_skin_texture"
    bl_label = "Load Skin Texture"

    filename_ext = ".png;.jpg;.jpeg;.tga;.bmp"
    filter_glob: StringProperty(default="*.png;*.jpg;*.jpeg;*.tga;*.bmp", options={'HIDDEN'})

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}

        # Check for unsaved changes in current texture
        image_node = helpers.get_active_image_texture_node(obj)
        if image_node and image_node.image and image_node.image.is_dirty:
            # Allow overwriting if it's a generated texture (likely the default blank one)
            if image_node.image.source != 'GENERATED':
                self.report({'ERROR'}, "Current texture has unsaved changes! Save it first to avoid losing work.")
                return {'CANCELLED'}

        filepath = self.filepath
        if not filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}

        try:
            # Use the helper to apply the material/texture
            helpers.create_character_material(obj, filepath)

            self.report({'INFO'}, f"Loaded skin texture: {os.path.basename(filepath)}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error loading texture: {str(e)}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # Set the default directory from preferences if available
        try:
            addon_prefs = context.preferences.addons.get(__package__)
            if addon_prefs and addon_prefs.preferences.default_skin_path:
                self.filepath = addon_prefs.preferences.default_skin_path
        except:
            pass

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class TATTOO_OT_clear_texture(Operator):
    """Clear the current skin texture to start over"""
    bl_idname = "tattoo.clear_texture"
    bl_label = "Clear Texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH' or not obj.active_material:
            return {'CANCELLED'}

        image_node = helpers.get_active_image_texture_node(obj)
        if image_node:
            # Check for unsaved changes
            if image_node.image and image_node.image.is_dirty:
                self.report({'ERROR'}, "Current texture has unsaved changes! Save it first.")
                return {'CANCELLED'}

            image_node.image = None
            self.report({'INFO'}, "Texture cleared")
            return {'FINISHED'}
        return {'CANCELLED'}


class TATTOO_OT_enter_texture_paint(Operator):
    """Switch to Texture Paint mode and enable Material Preview"""
    bl_idname = "tattoo.enter_texture_paint"
    bl_label = "Switch to Texture Paint"

    def execute(self, context):
        if context.object and context.object.type == 'MESH':
            bpy.ops.object.mode_set(mode='TEXTURE_PAINT')
            
            # Switch viewport shading to MATERIAL preview to ensure texture is visible
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'MATERIAL'
        return {'FINISHED'}


class TATTOO_PT_panel(Panel):
    """Creates a Panel in the 3D View sidebar for inZOI Tattoo Studio"""
    bl_label = "inZOI Tattoo Studio"
    bl_idname = "TATTOO_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "inZOI Tattoo Studio"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Instructions section
        box = layout.box()
        box.label(text="Workflow Steps", icon='INFO')
        col = box.column(align=True)
        col.label(text="1. Load Avatar (Import or Select)")
        col.label(text="2. Load Skin Texture")
        col.label(text="3. Go to Texture Paint Mode")
        col.label(text="4. Load Tattoo Image")
        col.label(text="5. Paint Tattoos")
        col.label(text="6. Export Result")

        # Import section
        box = layout.box()
        box.label(text="1. Load Avatar", icon='IMPORT')
        col = box.column(align=True)
        col.operator("tattoo.import_metahuman_fbx", text="Import inZOI FBX", icon='FILE_FOLDER')

        # Existing objects section
        col.separator()
        col.label(text="Or select existing:", icon='OBJECT_DATA')

        # Find all mesh objects that could be inZOI
        inzoi_objects = []
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and ('body' in obj.name.lower() or 'head' in obj.name.lower() or
                                      'inzoi' in obj.name.lower() or 'character' in obj.name.lower()):
                inzoi_objects.append(obj)

        if inzoi_objects:
            for obj in inzoi_objects:
                op = col.operator("tattoo.select_object", text=f"  {obj.name}", icon='OBJECT_DATA')
                op.object_name = obj.name
        else:
            col.label(text="  No existing inZOI objects found", icon='ERROR')

        # Check if we have objects to work with
        obj = context.active_object

        # Step 2: Load skin texture
        if obj and obj.type == 'MESH':
            box = layout.box()
            box.label(text="2. Load Skin Texture", icon='IMAGE_DATA')
            col = box.column(align=True)

            # Check if object already has a material with texture
            has_texture = False
            if obj.active_material:
                image_node = helpers.get_active_image_texture_node(obj)
                if image_node and image_node.image:
                    has_texture = True
                    img = image_node.image
                    w, h = img.size
                    col.label(text=f"Current: {img.name} ({w}x{h})", icon='IMAGE_DATA')

            if not has_texture:
                # Create material with texture button
                col.operator("tattoo.load_skin_texture", text="Load inZOI Skin Texture", icon='FILEBROWSER')
            else:
                col.label(text="Texture already loaded", icon='CHECKMARK')
                col.operator("tattoo.load_skin_texture", text="Replace Skin Texture", icon='FILE_REFRESH')
                col.operator("tattoo.clear_texture", text="Clear / Reset Texture", icon='TRASH')

        # Step 3: Go to Texture Paint
        box = layout.box()
        box.label(text="3. Texture Paint Mode", icon='BRUSH_DATA')
        col = box.column(align=True)

        # Button to switch to texture paint mode
        if obj and obj.type == 'MESH':
            if context.mode == 'PAINT_TEXTURE':
                col.label(text="Already in Texture Paint", icon='CHECKMARK')
            else:
                col.operator("tattoo.enter_texture_paint", text="Switch to Texture Paint", icon='IMAGE_RGB_ALPHA')
        else:
            col.label(text="Select an object first", icon='ERROR')

        # Step 4: Load tattoo image
        box = layout.box()
        box.label(text="4. Load Tattoo Image", icon='IMAGE_RGB')
        col = box.column(align=True)

        if context.mode == 'PAINT_TEXTURE' and obj and obj.type == 'MESH':
            col.operator("tattoo.load_tattoo_image", text="Load Tattoo Image", icon='IMAGE_DATA')
            col.operator("tattoo.setup_tattoo_brush", text="Setup Tattoo Brush", icon='BRUSH_DATA')
            col.operator("tattoo.rotate_stencil", text="Rotate Stencil 90°", icon='FILE_REFRESH')
        else:
            col.label(text="Switch to Texture Paint first", icon='ERROR')

        # Step 5: Resolution and Export
        if obj and obj.type == 'MESH' and obj.active_material:
            box = layout.box()
            box.label(text="5. Process & Export", icon='EXPORT')
            col = box.column(align=True)

            # Check if we can resize (valid object and image)
            can_resize = obj and obj.type == 'MESH' and obj.active_material
            if can_resize:
                image_node = helpers.get_active_image_texture_node(obj)
                can_resize = image_node and image_node.image and image_node.image.size[0] > 0 and image_node.image.size[1] > 0

            row = col.row()
            row.enabled = bool(can_resize)
            row.operator("tattoo.resize_texture_to_4k", text="Resize to 4K", icon='IMAGE_DATA')

            # Check if we can export (valid object and image)
            can_export = obj and obj.type == 'MESH' and obj.active_material
            if can_export:
                image_node = helpers.get_active_image_texture_node(obj)
                can_export = image_node and image_node.image and image_node.image.size[0] > 0 and image_node.image.size[1] > 0

            row = col.row()
            row.enabled = bool(can_export)
            row.operator("tattoo.export_tattooed_texture", text="Export Tattooed Texture", icon='EXPORT')

            col.operator("tattoo.export_usd", text="Export to UE5 (USD)", icon='SCENE_DATA')

        # Show current selection info
        if obj and obj.type == 'MESH':
            layout.separator()
            row = layout.row()
            row.label(text=f"Active: {obj.name}", icon='OBJECT_DATA')
            if obj.active_material:
                row.label(text=f"Material: {obj.active_material.name}", icon='MATERIAL')


classes = (
    TATTOO_OT_import_metahuman_fbx,
    TATTOO_OT_resize_texture_to_4k,
    TATTOO_OT_setup_tattoo_brush,
    TATTOO_OT_load_tattoo_image,
    TATTOO_OT_rotate_stencil,
    TATTOO_OT_export_tattooed_texture,
    TATTOO_OT_export_usd,
    TATTOO_OT_select_body,
    TATTOO_OT_select_head,
    TATTOO_OT_select_object,
    TATTOO_OT_load_skin_texture,
    TATTOO_OT_clear_texture,
    TATTOO_OT_enter_texture_paint,
    TATTOO_PT_panel,
    preferences.TATTOO_AddonPreferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    # Load settings from JSON if available (delayed to ensure context is ready)
    bpy.app.timers.register(lambda: preferences.load_settings(__package__), first_interval=0.1)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()