"""
Brush management functions for the Tattoo Master addon
"""
import bpy
from . import helpers


def setup_tattoo_brush():
    """Setup the tattoo brush with stencil mode."""
    # Get the active object
    obj = bpy.context.active_object

    # Validate that we have a mesh object with UVs
    if not obj or obj.type != 'MESH':
        raise Exception("No mesh object selected")

    # Check preferences for auto UV creation
    addon_prefs = bpy.context.preferences.addons.get(__package__)
    if addon_prefs:
        use_auto_uv = addon_prefs.preferences.use_auto_uv
    else:
        use_auto_uv = True  # Default value

    if use_auto_uv and not helpers.get_uv_layer(obj):
        # Try to create a UV layer if none exists
        if not obj.data.uv_layers:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.mesh.uv_texture_add()

    # Switch to Texture Paint mode if not already
    if bpy.context.mode != 'PAINT_TEXTURE':
        # First make sure we're in object mode before switching to texture paint
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Select the active object to ensure it's properly set
        if obj and obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='TEXTURE_PAINT')

    # Get the active brush
    tool_settings = bpy.context.tool_settings
    if hasattr(tool_settings, 'image_paint'):
        brush = tool_settings.image_paint.brush
        if not brush:
            # If no brush exists, try to get the first available one
            for b in bpy.data.brushes:
                if b.use_paint_image:
                    brush = b
                    break
            if not brush:
                # Create a new brush if none exists
                brush = bpy.data.brushes.new(name="TattooBrush", mode='IMAGE')
    else:
        # Fallback: try to get brush from paint settings
        paint_settings = bpy.context.tool_settings.image_paint
        brush = paint_settings.brush

    if not brush:
        raise Exception("Could not get or create a brush for texture painting")

    # Set brush properties
    brush.blend = 'MUL'  # Multiply blend mode
    brush.color = (1.0, 1.0, 1.0)  # White color
    brush.strength = 0.75

    # Ensure the brush has a texture slot
    if not brush.texture_slot:
        # Create a texture slot if it doesn't exist
        pass  # The texture slot will be created when we assign a texture

    # Set the texture slot to stencil mode
    if brush.texture_slot:
        brush.texture_slot.map_mode = 'STENCIL'

    return brush


def load_tattoo_image(filepath, resize_to_4k=False):
    """Load a tattoo image for the stencil brush."""
    # Load the image
    image = bpy.data.images.load(filepath)

    # Auto-resize logic (maintain aspect ratio)
    if resize_to_4k:
        width, height = image.size
        max_dim = max(width, height)
        target_res = 4096
        
        if max_dim < target_res and max_dim > 0:
            scale_factor = target_res / max_dim
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image.scale(new_width, new_height)

    # Setup the brush
    brush = setup_tattoo_brush()

    # Create or get a texture data block (Brush needs a Texture, not just an Image)
    texture_name = "Tattoo_Stencil_Texture"
    texture = bpy.data.textures.get(texture_name)
    if not texture:
        texture = bpy.data.textures.new(texture_name, type='IMAGE')
    texture.image = image
    brush.texture = texture

    # Set the texture slot to stencil mode
    if brush.texture_slot:
        brush.texture_slot.map_mode = 'STENCIL'

    return brush, image