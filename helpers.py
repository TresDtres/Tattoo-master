"""
Helper functions for the Tattoo Master addon
"""
import bpy
import os


def get_active_image_texture_node(obj):
    """Get the active Image Texture node from the object's material."""
    if not obj or not obj.active_material:
        return None
    
    material = obj.active_material
    if material.use_nodes:
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                return node
    return None


def get_inzoi_body_object():
    """Find the inZOI body object by name."""
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and ('body' in obj.name.lower() or 'body' in obj.data.name.lower() or 'character' in obj.name.lower()):
            return obj
    return None


def get_inzoi_head_object():
    """Find the inZOI head object by name."""
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and ('head' in obj.name.lower() or 'head' in obj.data.name.lower() or 'character' in obj.name.lower()):
            return obj
    return None


def ensure_uv_layer(obj):
    """Ensure the object has a UV layer."""
    if not obj.data.uv_layers:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.mesh.uv_texture_add()
        return True
    return False


def create_character_material(obj, image_path=None):
    """Create or update a material for the character object with an image texture."""
    # Check preferences for auto UV creation
    try:
        addon_prefs = bpy.context.preferences.addons.get(__package__)
        if addon_prefs:
            use_auto_uv = addon_prefs.preferences.use_auto_uv
            target_resolution = addon_prefs.preferences.default_resolution
        else:
            use_auto_uv = True  # Default value
            target_resolution = 4096
    except:
        use_auto_uv = True  # Default value in case of error
        target_resolution = 4096

    if use_auto_uv and not obj.data.uv_layers:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.mesh.uv_texture_add()

    # Create or get material
    material_name = f"{obj.name}_TattooMaterial"
    material = bpy.data.materials.get(material_name)

    if not material:
        material = bpy.data.materials.new(name=material_name)
        obj.data.materials.append(material)
    else:
        obj.active_material = material

    # Enable use of nodes
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear existing nodes
    nodes.clear()

    # Create shader nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')

    # Position nodes
    output_node.location = (400, 0)
    bsdf_node.location = (200, 0)

    # Link nodes
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Create image texture node
    image_node = nodes.new(type='ShaderNodeTexImage')
    image_node.location = (0, 0)

    # Load image if provided
    final_image = None
    
    if image_path:
        # Try loading directly first
        try:
            final_image = bpy.data.images.load(image_path)
        except:
            # Try absolute path if direct load fails
            try:
                abs_path = bpy.path.abspath(image_path)
                final_image = bpy.data.images.load(abs_path)
            except:
                pass
        
        if final_image:
            # Auto-scale if resolution is lower than target
            if final_image.size[0] < target_resolution or final_image.size[1] < target_resolution:
                final_image.scale(target_resolution, target_resolution)
        else:
            # If path was provided but failed to load, raise error instead of fallback
            raise RuntimeError(f"Failed to load image: {image_path}")
    else:
        # Fallback: Create a default white image if no path provided
        final_image = bpy.data.images.new(f"{obj.name}_BC", width=target_resolution, height=target_resolution)
        final_image.generated_color = (0.8, 0.8, 0.8, 1.0)  # Light gray

    image_node.image = final_image

    # Connect image to BSDF
    links.new(image_node.outputs['Color'], bsdf_node.inputs['Base Color'])

    return material


def switch_to_mesh(obj_name):
    """Switch to the specified mesh object."""
    obj = bpy.data.objects.get(obj_name)
    if obj and obj.type == 'MESH':
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select and make active the target object
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        return True
    return False


def get_uv_layer(obj):
    """Get the active UV layer of an object."""
    if obj and obj.type == 'MESH':
        if obj.data.uv_layers.active:
            return obj.data.uv_layers.active
    return None