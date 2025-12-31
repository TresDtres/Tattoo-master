# Tattoo Master for inZOI

**Tattoo Master** is a Blender addon designed to automate the workflow of applying high-quality tattoos on MetaHuman meshes (body and head) for inZOI. It uses texture painting mode with *Stencil* and ensures compatibility with Unreal Engine 5 export.

## Installation

1. Download this repository as a ZIP file (Code > Download ZIP).
2. Open Blender (Version 4.0 or higher recommended).
3. Go to **Edit > Preferences**.
4. Select the **Add-ons** tab.
5. Click **Install...** and select the downloaded ZIP file.
6. Activate the addon by searching for **"3D View: Tattoo Master inZOI"**.

## Configuration

Once activated, expand the addon preferences in the addons list (or in the side panel):

1. Go to the **Default Paths** section and configure your working folders:
   - **Default Tattoo Path**: Folder where you keep your tattoo images/designs.
   - **Default Skin Path**: Folder with base skin textures.
   - **Default FBX Path**: Folder where you have your inZOI FBX models.
   - **Default Export Path**: Folder where exported textures will be saved.

> **Note:** These settings are saved locally on your machine and will not be overwritten when updating the addon.

## Quick Usage

The main panel is located in the **3D View Sidebar** (Press `N` to show it) under the **inZOI Tattoo Studio** tab.

### Workflow:

1. **Import inZOI FBX**: Load your inZOI FBX model.
2. **Load/Replace Skin Texture**: Load the base skin texture (automatically resized to 4K for better quality).
3. **Texture Paint Mode**: Automatically switches to paint mode and sets up the view.
4. **Load Tattoo Image**: Load your tattoo image. This will set up the brush in *Stencil* mode.
   - Use `Right Click` to move the stencil.
   - Use `Shift + Right Click` to scale.
   - Use `Ctrl + Right Click` to rotate.
5. **Paint** on the model where you want the tattoo.
6. **Export**:
   - **Export Tattooed Texture**: Saves only the resulting color texture (PNG/TGA).
   - **Export USD (UE5)**: Exports the model and textures in USD format compatible with Unreal Engine 5.

## Features

- Optimized inZOI FBX import.
- Automatic material and UV setup.
- Automated Stencil brush system.
- Automatic texture resizing to 4K.
- Direct export to UE5 compatible formats.

## Credits

Developed by TRESDTRES.
