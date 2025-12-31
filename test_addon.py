"""
Test script for Tattoo Master addon
This script can be run in Blender's scripting workspace to test the addon functionality
"""
import bpy
import os

def test_addon():
    """Test the Tattoo Master addon functionality"""
    print("Testing Tattoo Master addon...")
    
    # Check if the addon is registered
    # Check multiple possible folder names
    possible_names = ["tattoo_master", "Tatto_Master", "tatto_master", "Tattoo_Master"]
    is_registered = False
    for name in possible_names:
        if name in bpy.context.preferences.addons:
            print(f"✓ Tattoo Master addon is registered as '{name}'")
            is_registered = True
            break
            
    if not is_registered:
        print("✗ Tattoo Master addon is NOT registered")
        print(f"  Checked names: {possible_names}")
        return False
    
    # Test operators exist
    operators = [
        "tattoo.import_metahuman_fbx",
        "tattoo.resize_texture_to_4k", 
        "tattoo.setup_tattoo_brush",
        "tattoo.load_tattoo_image",
        "tattoo.rotate_stencil",
        "tattoo.export_tattooed_texture",
        "tattoo.export_usd",
        "tattoo.select_body",
        "tattoo.select_head",
        "tattoo.select_object",
        "tattoo.load_skin_texture",
        "tattoo.clear_texture",
        "tattoo.enter_texture_paint"
    ]
    
    missing_ops = []
    for op in operators:
        if not hasattr(bpy.ops, op.split('.')[1]):  # Get the part after the dot
            # Try to access the operator differently
            try:
                op_parts = op.split('.')
                op_module = getattr(bpy.ops, op_parts[0])
                op_func = getattr(op_module, op_parts[1])
            except AttributeError:
                missing_ops.append(op)
    
    if missing_ops:
        print(f"✗ Missing operators: {missing_ops}")
    else:
        print("✓ All operators are available")
    
    # Test panel exists
    panel_found = False
    for panel_class in bpy.types.Panel.__subclasses__():
        if hasattr(panel_class, 'bl_idname') and panel_class.bl_idname == 'TATTOO_PT_panel':
            panel_found = True
            break
    
    if panel_found:
        print("✓ Tattoo Studio panel is available")
    else:
        print("✗ Tattoo Studio panel is NOT available")
    
    print("Test completed!")
    return True

# Run the test
if __name__ == "__main__":
    test_addon()