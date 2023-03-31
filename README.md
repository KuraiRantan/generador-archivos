* [Uso](#uso)
    * [Código fuente](#código-fuente)
    * [Aplicación](#aplicación)

# Uso

## Código fuente

**Nota:** ***Requisito tener instalado Python 3.4+ en el equipo.***

Abrir una terminal y ejecutar los siguientes comandos:

1. ### Crear entorno virtual.
    Estando en la raíz del proyecto(a la altura del archivo ```requirements.txt```) ejecutar el comando:
    ~~~
    python -m venv env
    ~~~

2. ### Activar el entorno virtual
    * Windows:
    ~~~
    .\env\Scripts\activate
    ~~~
    * Linux:
    ~~~
    source ./env/bin/activate
    ~~~

3. ### Instalar dependencias
    Una vez creado y activado el entorno virtual, en la raíz del proyecto se encuentra el archivo `requirements.txt` el cual contiene la paquetería necesaria para el correcto funcionamiento de la aplicación. Para instalar dichos paquetes en nuestro entorno virtual debemos ejecutar el siguiente comando:
    ~~~
    pip install -r requirements.txt
    ~~~

4. ### Ejecutar aplicación
    Terminados los pasos anteriores solo bastará con ubicarnos a la altura del archivo `app.py` que está en la carpeta `src` y ejecutar el comando:
    ~~~
    python app.py
    ~~~

## Aplicación
Descargar la aplicación ya sea para Windows o Linux, una vez descargada, identificarla en el administrador de archivos y abrirla haciendo doble clic sobre ella. [Enlaces de descarga](https://kurairantan.github.io/#proyectos)

[VIDEO: Descarga de ejecutable](https://res.cloudinary.com/di6mevrkr/video/upload/v1680243093/generador_documentos/descargar-ejecutable.webm)

__*A medida que siga los pasos encontrara los archivos utilizados para el ejemplo de uso.*__

1. Seleccionar la plantilla que debe tener extensión .docx. [Descargar plantilla](https://www.dropbox.com/s/lqqmcgembn6t60i/plantilla.docx?dl=0)

~~~
Aprende programación.

Aprende ${{lenguaje de programacion}} y su framework estrella ${{framework}} junto a el manejo de bases de datos ${{data base}}.
~~~
[VIDEO: Seleccionar plantilla](https://res.cloudinary.com/di6mevrkr/video/upload/v1680243087/generador_documentos/seleccionar-plantilla.webm)

2. Seleccionar los datos que deben estar dentro de un archivo con extensión .txt.
La primera fila del archivo serán las variables a reemplazar dentro de la plantilla y todo deberá ir separado por `;`. [Descargar archivo de datos](https://www.dropbox.com/s/wlzzhnomzs30z90/datos.txt?dl=0)
~~~
lenguaje de programacion;framework;data base
Python;Django;Postgresql
PHP;Laravel;Mysql
C#;Blazor;SQL server
~~~
[VIDEO: Seleccionar datos](https://res.cloudinary.com/di6mevrkr/video/upload/v1680243087/generador_documentos/seleccionar-datos.webm)

3. Seleccionar la carpeta de destino(donde queremos guardar los archivos).
[VIDEO: Seleccionar carpeta destino](https://res.cloudinary.com/di6mevrkr/video/upload/v1680243079/generador_documentos/seleccionar-salida.webm)

4. Ingresar el formato de reemplazo utilizado en la plantilla.
[VIDEO: Ingresar formato reemplazo](https://res.cloudinary.com/di6mevrkr/video/upload/v1680243078/generador_documentos/formato-reemplazo.webm)


5. Seleccionar el tipo de documento de salida(pdf o word siendo word el seleccionado por defecto).
Realizar clic sobre el botón `GENERAR` a partir del cual iniciara el proceso de generación de los documentos.
[VIDEO: Seleccionar tipo y generar documentos](https://res.cloudinary.com/di6mevrkr/video/upload/v1680243081/generador_documentos/generar.webm)


6. Confirmar si queremos o no abrir la carpeta en donde se ubican nuestros archivos.
[VIDEO: Confirmar abrir carpeta](https://res.cloudinary.com/di6mevrkr/video/upload/v1680243050/generador_documentos/abrir-resultado.webm)
