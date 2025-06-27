# SimpleLauncher

Este launcher está enfocado en permitir a los usuarios ejecutar e instalar distintas versiones de Minecraft de manera simple.

- [Requisitos](#requisitos)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Consideraciones](#consideraciones)
- [Trabajo en proceso](#trabajo-en-proceso)
- [Trabajo a futuro](#trabajo-a-futuro)
## Requisitos
- Python 3.13
- PySide6
- JDK

## Configuración

El launcher usa un archivo de configuración `config.ini` en el que se pueden configurar los distintos paths, URLs e informacion necesaria para el correcto funcionamiento del launcher. El archivo se divide en diferentes secciones.

Las rutas que viene configuradas por defecto corresponden a sistemas Linux. Para su correcto funcionamiento deben configurarse para el sistema donde se ejecute este sistema. 

### `[URLS]`

En esta sección se configuran las URL's de donde el launcher descargará la información del juego. 

- `versions_manifest_url` : Direccion de descarga del archivo `version_manifest.json` que contiene la información de las distintas versiones.
- Para poder descargar los assets del juego se requiere de la direccion `https://resources.download.minecraft.net`, sin embargo esta direccion no se puede configurar desde el archivo `config.ini`. Por el momento esa direccion se programa directamente en código en el archivo `model/asset_index.py` en una variable llamada `ASSETS_URL`. Esta url se agregará al archivo de configuracion en futuras versiones. 

### `[JVM]`
JVM hace referencia a todas las configuraciones relacionadas con la Java Virtual Machine. 

- `java_path` : Path directo al archivo binario de java. Para realizar las pruebas se utilizó el JDK de [ADOPTIUM](https://adoptium.net/es/) para sistemas Linux. La ruta por defecto busca el binario de java dentro de la carpeta raiz en `jdk/bin/java`

### `[PATHS]`
Rutas de acceso a recursos dentro del computador.

- `game_dir` : Ruta de instalación del juego. Por defecto en Linux: `/home/{USER}/.minecraft`, Windows: `%APPDATA%/.minecraft`.

### `[LAUNCHER_INFO]`

- `version` : Version del launcher.
- `name` : Nombre del launcher.

### `[USER]`

- `name` : Nombre de usuario del jugador. Se puede dejar vacío por defecto y se almacenará el ultimo nombre de usuario ingresado. 

## Ejecución
Para ejecutarlo es necesario contar con el JDK. 

Descargamos el repositorio.

```bash
git clone https://github.com/Tzintzun/SimpleLauncher.git
```

Instalamos PySide6
```bash
pip install PySide6
```

Ahora simplemente ejecutamos `SimpleLauncherUi.py`
```bash
python SimpleLauncherUi.py
```

## Consideraciones
- Debido a cambios en el manifiesto de cada versión, el launcher solo puede descargar y ejecutar versiones posteriores a la `1.13.x`
- Solo es capaz de ejecutar versiones vanilla del juego. 
- El botón de `Verificar` aun no está implementado.

## Trabajo en proceso
- Soporte para todas las versiones vanilla del juego.
- Comprobación del Hash del archivo al descargar.
- Implementación del verificacion de archivos para las versiones instaladas.
- Implementación de carpeta de configuracion.
- Empaquetado y distribución del launcher.

## Trabajo a futuro
- Agregar soporte para ejecutar versiones Forge y Fabric.
