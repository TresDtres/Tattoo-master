# Tattoo Master for inZOI

**Tattoo Master** es un addon de Blender diseñado para automatizar el flujo de trabajo de aplicación de tatuajes de alta calidad en mallas de MetaHuman (cuerpo y cabeza) para inZOI. Utiliza el modo de pintura de texturas con *Stencil* (plantilla) y asegura la compatibilidad con la exportación a Unreal Engine 5.

## Instalación

1. Descarga este repositorio como un archivo ZIP (Code > Download ZIP).
2. Abre Blender (Versión 4.0 o superior recomendada).
3. Ve a **Edit > Preferences** (Editar > Preferencias).
4. Selecciona la pestaña **Add-ons**.
5. Haz clic en **Install...** y selecciona el archivo ZIP descargado.
6. Activa el addon buscando **"3D View: Tattoo Master inZOI"**.

## Configuración

Una vez activado, despliega las preferencias del addon en la lista de addons (o en el panel lateral):

1. Ve a la sección **Default Paths** y configura tus carpetas de trabajo:
   - **Default Tattoo Path**: Carpeta donde guardas tus imágenes/diseños de tatuajes.
   - **Default Skin Path**: Carpeta con las texturas base de la piel.
   - **Default FBX Path**: Carpeta donde tienes tus modelos FBX de inZOI.
   - **Default Export Path**: Carpeta donde se guardarán las texturas exportadas.

> **Nota:** Estas configuraciones se guardan localmente en tu equipo y no se sobrescribirán al actualizar el addon.

## Uso Rápido

El panel principal se encuentra en la **Barra Lateral de la Vista 3D** (Presiona `N` para mostrarla) bajo la pestaña **inZOI Tattoo Studio**.

### Flujo de trabajo:

1. **Import inZOI FBX**: Carga tu modelo FBX de inZOI.
2. **Load/Replace Skin Texture**: Carga la textura de piel base (se redimensiona a 4K automáticamente para mejor calidad).
3. **Texture Paint Mode**: Cambia automáticamente al modo de pintura y configura la vista.
4. **Load Tattoo Image**: Carga tu imagen de tatuaje. Esto configurará el pincel en modo *Stencil*.
   - Usa `Click Derecho` para mover el stencil.
   - Usa `Shift + Click Derecho` para escalar.
   - Usa `Ctrl + Click Derecho` para rotar.
5. **Pinta** sobre el modelo donde desees el tatuaje.
6. **Export**:
   - **Export Tattooed Texture**: Guarda solo la textura de color resultante (PNG/TGA).
   - **Export USD (UE5)**: Exporta el modelo y texturas en formato USD compatible con Unreal Engine 5.

## Características

- Importación optimizada de FBX de inZOI.
- Configuración automática de materiales y UVs.
- Sistema de pincel Stencil automatizado.
- Redimensionado automático de texturas a 4K.
- Exportación directa a formatos compatibles con UE5.

## Créditos

## Créditos

Desarrollado por TRESDTRES.

