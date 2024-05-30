# Flask en Docker

Esta es una práctica para incorporar Flask en Docker.
SOLO PARA DESARROLLO

NO usar para producción.

## Requisitos

- Docker
- Docker Compose
- Python
- Pip
- virtualenv (instalación solo una vez)

```bash
pip3 install virtualenv
```

Para la siguiente implementación se usaron los siguientes video tutoriales de referencia:

[Fuente](https://www.youtube.com/watch?v=YENw-bNHZwg) |

[Referencia 2] (https://www.youtube.com/watch?v=BvvH3ohis6E)


## Instrucciones

1. Crear un entorno virtual

```bash
virtualenv venv
```
Donde venv es el nombre que le doy al entorno virtual y es personalizable.

2. Activar el entorno virtual

```bash
source venv/bin/activate
```

Puedo desactivar el entorno con:
  
  ```bash
  deactivate
  ```

  Considerar que el entorno queda creado como una carpeta de librerías en el directorio raiz del proyecto, en forma local. Es por ello que los comandos deben ser corridos en los directorios raíz del proyecto.

  Cuando el ambiente virtual está activado, puedo ver en la terminal el prompt así:
  
  ```bash
  (venv) $
  ```

3. Instalar Flask (utilizar uno de los dos comandos)
  
```bash
  pip install flask
  pip3 install flask
```

4. Crear el archivo app.py

```python
  from flask import Flask, jsonify

  app = Flask(__name__)

  @app.route('/', methods=['GET'])
  def ping():
    return jsonify({"response": "hello world!"})

  if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
```

Mantener el puerto como 5000 ya que genera problemas cuando se cambia el valor del puerto.

5. Probar ejecutar la aplicación

En el directorio raíz, con la terminal ejecutar:

```bash
python3 src/app.py
```

6. Crear el archivo Dockerfile

Para crearlo, vamos a considerar instalar una versión de linux llamada alphine. Así como en otras distribuciones, tiene un gestor de packetes "apk" que es equivalente al "apt-get" de otras distribuciones linux.

- Creamos los sistemas que necesitamos:

```Dockerfile
# Instala sistema linux desde la imagen alpine
FROM alpine:3.10

# Install required packages
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip \

```

- Ahora necesitamos copiar los archivos desde mi ambiente local al contenedor y viceversa.

```Dockerfile

# Set the working directory (CREAMOS el directorio de trabajo en el contenedor)
WORKDIR /app

# Copy the current directory contents into the container at /app (COPIAS DE TODA LA CONTENIDO DE LA CARPETA ACTUAL AL CONTENEDOR)
COPY . /app 

```

- Ahora necesitamos los requisitos de la aplicación. Para lo anterior creamos un archivo llamado requirement.

Podemos usar el comando si hemos estado instalando librerias desde la consola y aún no hemos creado el archivo txt:
```bash
pip freeze > requirements.txt
```

El comando anterior crea el archivo requirement.txt con todas las dependencias que hasta ese momento son necesarias para la aplicación.

- Ahora necesitamos instalar las dependencias en el contenedor.

```Dockerfile
RUN pip3 --no-cache-dir install -r requirements.txt
```

- Ahora necesitamos exponer el puerto de la aplicación.

```Dockerfile
# Make port 5000 available to the world outside this container
EXPOSE 5000
```

- Ahora necesitamos ejecutar la aplicación.

```Dockerfile
# Run app.py when the container launches
CMD ["python3", "src/app.py"]
```

7. Construimos nuevamente la imagen

```bash
docker build -t flask-app .
```

8. Ejecutamos la imagen

- En forma interactva:

```bash
docker run -it --publish 5000:5000 flask-app
```

- En forma de proceso (background)

```bash
docker run -d -p 5000:5000 flask-app
```

Si ya está construido podemos usar:

```bash
docker start id-contendedor
```