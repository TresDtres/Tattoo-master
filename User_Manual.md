# User Manual - inZOI Tattoo Studio

## General Description

The **inZOI Tattoo Studio** addon automates the process of applying tattoos on inZOI characters for Blender, allowing you to create high-quality tattoos that will be exported to Unreal Engine.

## System Requirements

- Blender 4.0 or higher (recommended 4.2+)
- An inZOI character imported or available in the scene
- High-resolution textures (recommended 4096x4096)

## Initial Setup

### 1. Addon Installation

1. In Blender, go to `Edit > Preferences > Add-ons`
2. Click `Install...`
3. Select the `__init__.py` file of the addon
4. Check the box next to "3D View: Tattoo Master for in"
5. The "inZOI Tattoo Studio" panel will appear in the sidebar (N-panel)

## Complete Workflow

### Step 1: Import the inZOI Avatar

1. In the "inZOI Tattoo Studio" panel, go to section "1. Load Avatar"
2. Click "Import inZOI FBX" to import your character
3. Alternatively, if you already have an avatar loaded, use the "Or select existing" section to select it

### Step 2: Load the Avatar Texture

1. Go to section "2. Load Skin Texture"
2. If the avatar already has a texture, it will show as "Texture already loaded"
3. If no texture exists, click "Load inZOI Skin Texture" and select the texture file (PNG, JPG, etc. format)
4. The texture should be high resolution (4096x4096 for optimal quality)

### Step 3: Adjust Texture Resolution

1. Go to section "5. Process & Export"
2. Click "Resize to 4K" to convert the texture to 4096x4096 pixels
3. The addon will verify if the texture is already at the correct resolution
4. IMPORTANT: Textures must be 4096x4096 to avoid pixelation in the game

### Step 4: Prepare Paint Mode

1. Go to section "3. Texture Paint Mode"
2. Click "Switch to Texture Paint" to change to texture paint mode
3. The 3D view area will change to show paint tools

### Step 5: Load the Tattoo Image

1. Go to section "4. Load Tattoo Image"
2. Click "Load Tattoo Image"
3. Select the tattoo image (should be 4096x4096 for optimal quality)
4. IMPORTANT: The tattoo should also be 4096x4096 to avoid pixelation

### Step 6: Configure the Tattoo Brush

1. In the same section "4. Load Tattoo Image", click "Setup Tattoo Brush"
2. The brush will be automatically configured with:
   - Blend mode: Multiply
   - Color: White (1.0, 1.0, 1.0)
   - Strength: 0.750
   - Mapping mode: Stencil

### Step 7: Paint the Tattoo

1. In Texture Paint mode, use the brush to apply the tattoo
2. The tattoo will be applied as a black mask over the avatar's skin
3. To invert the tattoo image (white becomes black), use the inversion option if available
4. Adjust brush size with shortcuts `[` and `]`
5. Adjust strength with the slider in the brush properties

### Step 8: Export the Final Texture

1. Go to section "5. Process & Export"
2. Click "Export Tattooed Texture"
3. Select the location and filename
4. Choose PNG or TGA format according to project needs
5. The exported texture will contain the applied tattoo

## Advanced Settings

### Addon Preferences

1. Go to `Edit > Preferences > Add-ons`
2. Select "Tattoo Master for in"
3. In the preferences section, you can configure:
   - Default texture path
   - Default export path
   - Default resolution (4096 for optimal quality)
   - Option to create UV automatically

### Manual Brush Configuration

If you need to manually adjust the brush:

1. In Texture Paint mode, select the brush
2. In brush properties:
   - Change "Blend" to "MUL" (Multiply)
   - Set "Color" to white (1.0, 1.0, 1.0)
   - Set "Strength" to 0.750
   - In "Texture", select the tattoo image
   - In "Mapping", select "Stencil"
   - Adjust "Offset" and "Size" to position the tattoo

## Tips and Recommendations

1. **Resolution**: Always use 4096x4096 textures to avoid pixelation
2. **Tattoo format**: Use PNG images with transparency for best results
3. **Tattoo color**: White in the tattoo image will become black on the skin
4. **Gradual testing**: Apply small tattoos first to test the setup
5. **Frequent saves**: Save the Blender file regularly during work
6. **UV Maps**: Ensure the model has properly unwrapped UVs

## Troubleshooting

### "Resize to 4K" button is disabled
- Verify that you have selected an object with material and texture
- Make sure the texture is loaded correctly

### Tattoo doesn't appear when painting
- Verify you are in Texture Paint mode
- Ensure the brush is set to Stencil mode
- Check that the tattoo image is correctly loaded

### Pixelated texture
- Make sure both the base texture and tattoo are 4096x4096
- Verify you used the "Resize to 4K" button before painting

### Can't select the avatar
- Verify the object name contains "body", "head", "inzoi" or "character"
- Ensure the object is of type MESH

## Export for inZOI/Unreal Engine

1. The exported texture should remain in PNG or TGA format
2. The final size will be 4096x4096, the game will reduce it to 2048 as needed
3. Make sure the exported texture has the correct name for the game to recognize it
4. The texture can be imported directly into Unreal Engine as body or head texture

## Useful Keyboard Shortcuts

- `Ctrl + Tab`: Switch between edit modes
- `[` and `]`: Adjust brush size
- `Shift + F` or `F`: Switch between view modes
- `D` + `B`: Open brush selector

## Contact and Support

For additional support or to report issues:
- Check the README files included with the addon
- Consult Blender documentation for general topics
- Make sure you are using the latest version of the addon

---

*Manual Version: 1.0*  
*Date: December 2025*  
*Addon: Tattoo Master for in*