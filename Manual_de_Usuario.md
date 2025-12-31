# Manual de Usuario - inZOI Tattoo Studio

## Descripción General

El addon **inZOI Tattoo Studio** automatiza el proceso de aplicación de tatuajes en personajes inZOI para Blender, permitiendo crear tatuajes de alta calidad que se exportarán posteriormente a Unreal Engine.

## Requisitos del Sistema

- Blender 4.0 o superior (recomendado 4.2+)
- Un personaje inZOI importado o disponible en la escena
- Texturas de alta resolución (recomendado 4096x4096)

## Configuración Inicial

### 1. Instalación del Addon

1. En Blender, ir a `Edit > Preferences > Add-ons`
2. Hacer clic en `Install...`
3. Seleccionar el archivo `__init__.py` del addon
4. Activar la casilla junto a "3D View: Tattoo Master for in"
5. El panel "inZOI Tattoo Studio" aparecerá en la barra lateral (N-panel)

## Flujo de Trabajo Completo

### Paso 1: Importar el Avatar inZOI

1. En el panel "inZOI Tattoo Studio", ir a la sección "1. Load Avatar"
2. Hacer clic en "Import inZOI FBX" para importar tu personaje
3. Alternativamente, si ya tienes un avatar cargado, usar la sección "Or select existing" para seleccionarlo

### Paso 2: Cargar la Textura del Avatar

1. Ir a la sección "2. Load Skin Texture"
2. Si el avatar ya tiene una textura, se mostrará como "Texture already loaded"
3. Si no tiene textura, hacer clic en "Load inZOI Skin Texture" y seleccionar el archivo de textura (formato PNG, JPG, etc.)
4. La textura debe ser de alta resolución (4096x4096 para calidad óptima)

### Paso 3: Ajustar la Resolución de la Textura

1. Ir a la sección "5. Process & Export"
2. Hacer clic en "Resize to 4K" para convertir la textura a 4096x4096 píxeles
3. El addon verificará si la textura ya está en la resolución correcta
4. IMPORTANTE: Las texturas deben estar a 4096x4096 para evitar pixelación en el juego

### Paso 4: Preparar el Modo de Pintura

1. Ir a la sección "3. Texture Paint Mode"
2. Hacer clic en "Switch to Texture Paint" para cambiar al modo de pintura de textura
3. El área de vista 3D cambiará para mostrar las herramientas de pintura

### Paso 5: Cargar la Imagen del Tatuaje

1. Ir a la sección "4. Load Tattoo Image"
2. Hacer clic en "Load Tattoo Image"
3. Seleccionar la imagen del tatuaje (debe ser 4096x4096 para calidad óptima)
4. IMPORTANTE: El tatuaje también debe estar a 4096x4096 para evitar pixelación

### Paso 6: Configurar el Pincel de Tatuaje

1. En la misma sección "4. Load Tattoo Image", hacer clic en "Setup Tattoo Brush"
2. El pincel se configurará automáticamente con:
   - Modo de mezcla: Multiply (Multiplicar)
   - Color: Blanco (1.0, 1.0, 1.0)
   - Intensidad (Strength): 0.750
   - Modo de mapeo: Stencil (Plantilla)

### Paso 7: Pintar el Tatuaje

1. En el modo Texture Paint, usar el pincel para aplicar el tatuaje
2. El tatuaje se aplicará como una máscara negra sobre la piel del avatar
3. Para invertir la imagen del tatuaje (blanco se convierte en negro), usar la opción de inversión si está disponible
4. Ajustar el tamaño del pincel con el atajo `[` y `]`
5. Ajustar la intensidad con el deslizador en las propiedades del pincel

### Paso 8: Exportar la Textura Final

1. Ir a la sección "5. Process & Export"
2. Hacer clic en "Export Tattooed Texture"
3. Seleccionar la ubicación y nombre del archivo
4. Elegir formato PNG o TGA según las necesidades del proyecto
5. La textura exportada contendrá el tatuaje aplicado

## Configuración Avanzada

### Preferencias del Addon

1. Ir a `Edit > Preferences > Add-ons`
2. Seleccionar "Tattoo Master for in"
3. En la sección de preferencias, puedes configurar:
   - Ruta predeterminada para texturas
   - Ruta predeterminada para exportación
   - Resolución predeterminada (4096 para calidad óptima)
   - Opción para crear UV automáticamente

### Configuración Manual del Pincel

Si necesitas ajustar manualmente el pincel:

1. En modo Texture Paint, seleccionar el pincel
2. En las propiedades del pincel:
   - Cambiar "Blend" a "MUL" (Multiply)
   - Ajustar "Color" a blanco (1.0, 1.0, 1.0)
   - Ajustar "Strength" a 0.750
   - En "Texture", seleccionar la imagen del tatuaje
   - En "Mapping", seleccionar "Stencil"
   - Ajustar "Offset" y "Size" para posicionar el tatuaje

## Consejos y Recomendaciones

1. **Resolución**: Siempre usar texturas de 4096x4096 para evitar pixelación
2. **Formato de tatuaje**: Usar imágenes PNG con transparencia para mejores resultados
3. **Color del tatuaje**: El blanco en la imagen del tatuaje se convertirá en negro en la piel
4. **Prueba gradual**: Aplicar tatuajes pequeños primero para probar la configuración
5. **Guardado frecuente**: Guardar el archivo de Blender regularmente durante el trabajo
6. **UV Maps**: Asegurarse de que el modelo tenga UV desplegados correctamente

## Solución de Problemas

### El botón "Resize to 4K" está deshabilitado
- Verificar que hayas seleccionado un objeto con material y textura
- Asegurarte de que la textura esté cargada correctamente

### El tatuaje no aparece al pintar
- Verificar que estés en modo Texture Paint
- Asegurarte de que el pincel esté configurado en modo Stencil
- Comprobar que la imagen del tatuaje esté correctamente cargada

### Textura pixelada
- Asegurarte de que tanto la textura base como el tatuaje estén a 4096x4096
- Verificar que hayas usado el botón "Resize to 4K" antes de pintar

### No puedo seleccionar el avatar
- Verificar que el nombre del objeto contenga "body", "head", "inzoi" o "character"
- Asegurarte de que el objeto sea de tipo MESH

## Exportación para inZOI/Unreal Engine

1. La textura exportada debe mantenerse en formato PNG o TGA
2. El tamaño final será 4096x4096, el juego lo reducirá a 2048 según sea necesario
3. Asegurarte de que la textura exportada tenga el nombre correcto para que el juego la reconozca
4. La textura se puede importar directamente en Unreal Engine como textura de cuerpo o cabeza

## Atajos de Teclado Útiles

- `Ctrl + Tab`: Cambiar entre modos de edición
- `[` y `]`: Ajustar tamaño del pincel
- `Shift + F` o `F`: Cambiar entre modos de vista
- `D` + `B`: Abrir el selector de pinceles

## Contacto y Soporte

Para soporte adicional o reportar problemas:
- Revisar los archivos README incluidos con el addon
- Consultar la documentación de Blender para temas generales
- Asegurarte de usar la versión más reciente del addon

---

*Versión del Manual: 1.0*  
*Fecha: Diciembre 2025*  
*Addon: Tattoo Master for in*