"""
Preferences panel for the Tattoo Master addon
"""
import bpy
import os
import json
from bpy.props import StringProperty, BoolProperty, IntProperty


def get_config_path():
    return os.path.join(os.path.dirname(__file__), "config.json")


def save_settings(self, context):
    data = {
        "default_texture_path": self.default_texture_path,
        "default_skin_path": self.default_skin_path,
        "default_fbx_path": self.default_fbx_path,
        "default_export_path": self.default_export_path,
        "default_resolution": self.default_resolution,
        "use_auto_uv": self.use_auto_uv,
        "auto_save_textures": self.auto_save_textures
    }
    
    try:
        with open(get_config_path(), 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Tattoo Master: Error saving config: {e}")


def load_settings(package_name):
    path = get_config_path()
    if not os.path.exists(path):
        return
        
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            
        addon = bpy.context.preferences.addons.get(package_name)
        if addon:
            prefs = addon.preferences
            if "default_texture_path" in data: prefs.default_texture_path = data["default_texture_path"]
            if "default_skin_path" in data: prefs.default_skin_path = data["default_skin_path"]
            if "default_fbx_path" in data: prefs.default_fbx_path = data["default_fbx_path"]
            if "default_export_path" in data: prefs.default_export_path = data["default_export_path"]
            if "default_resolution" in data: prefs.default_resolution = data["default_resolution"]
            if "use_auto_uv" in data: prefs.use_auto_uv = data["use_auto_uv"]
            if "auto_save_textures" in data: prefs.auto_save_textures = data["auto_save_textures"]
            print(f"Tattoo Master: Settings loaded from {path}")
    except Exception as e:
        print(f"Tattoo Master: Error loading config: {e}")


class TATTOO_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Default paths
    default_texture_path: StringProperty(
        name="Default Texture Path",
        description="Default path for base color textures",
        subtype='DIR_PATH',
        update=save_settings
    )
    
    default_skin_path: StringProperty(
        name="Default Skin Path",
        description="Default path for skin textures",
        subtype='DIR_PATH',
        update=save_settings
    )
    
    default_fbx_path: StringProperty(
        name="Default FBX Path",
        description="Default path for importing inZOI FBX models",
        subtype='DIR_PATH',
        update=save_settings
    )
    
    default_export_path: StringProperty(
        name="Default Export Path", 
        description="Default path for exporting tattooed textures",
        subtype='DIR_PATH',
        update=save_settings
    )
    
    # Default settings
    default_resolution: IntProperty(
        name="Default Resolution",
        description="Default texture resolution",
        default=4096,
        min=512,
        max=16384,
        update=save_settings
    )
    
    use_auto_uv: BoolProperty(
        name="Auto Create UV Maps",
        description="Automatically create UV maps if none exist",
        default=True,
        update=save_settings
    )
    
    auto_save_textures: BoolProperty(
        name="Auto-Save Textures (USD)",
        description="Automatically save painted textures before USD export",
        default=True,
        update=save_settings
    )

    def draw(self, context):
        layout = self.layout
        
        # File paths section
        box = layout.box()
        box.label(text="Default Paths", icon='FILEBROWSER')
        col = box.column(align=True)
        col.prop(self, "default_texture_path", text="Default Tattoo Path")
        col.prop(self, "default_skin_path")
        col.prop(self, "default_fbx_path")
        col.prop(self, "default_export_path")
        
        # Settings section
        box = layout.box()
        box.label(text="Default Settings", icon='SETTINGS')
        col = box.column(align=True)
        col.prop(self, "default_resolution")
        col.prop(self, "use_auto_uv")
        col.prop(self, "auto_save_textures")