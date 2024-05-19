# Curso Flask

Este es un framework minimalista escrito en python es flexible es lo mas simple.
No tiene arquitectura especifica y tiene un ORM.

Flask extension, librerías de flask que extienden su funcionalidad.
Usa el ninja template.


## Configuración del entorno

Para configurar el entorno de desarrollo, se debe instalar las dependencias del proyecto.

Dependencias que debemos tener:

- Python 3
- Pip (paquetería para python)
- Virtualenv (para crear entornos virtuales)

```bash
  pip install -r requirements.txt
```

## Pasos para crear la aplicación

1.- Crear el directorio de la aplicación

```bash
  mkdir flask_app
  cd flask_app
```

2.- Crear el entorno virtual dentro del directorio creado

```bash
  virtualenv venv --python=python3.7
```

## Variables de contexto

Flask provee varios tipos de variables que no brindan el contexto de nuestra aplicación una de ellas es **request**.
Esta variable nos permite acceder a los datos que vienen en la petición.

Para ello primero debemos de importar **request** de Flask.

```python
  from flask import Flask, request
```
Y podemos usarlo en nuestra función, usando un atributo de **request** que es `remote_addr`. Este atributo guarda la ip del usuario.
  
```python
  @app.route('/')
  def hello_world():
      user_ip = request.remote_addr
      return 'Hello Navegador!, tu IP es {}'.format(user_ip)
```


## Ciclos de Request y response

Hay un Browser que hace una petición al servidor y el servidor regresa una respuesta.

Ahora veremos como Flask utiliza los request y responses para poder regresar la información que necesitamos.

Con el ejemplo anterior, usando la variable de contexto **request** obtuvimos la IP del usuario (que ingresó a nuestra aplicación).

Ahora creamos un nuevo objeto llamado **response**, y con el vamos a regresar una respuesta de flask. Luego vamos a guardar la IP del usuario en una cookie, en luagr de obtenerla directamente del **request**.

```python
@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)

    return response
```

En esta nueva ruta, obtuvimos la IP del usuario, guardamos la IP en una cookie y redirigimos el usuario a la ruta '/hello'.

```python
@app.route('/hello')
def hello():    
    user_ip = request.cookies.get('user_ip')
    
    return 'Hello Navegador!, tu IP es {}'.format(user_ip)
```

En esta nueva ruta, obtenemos la IP del usuario de la cookie y la mostramos en la respuesta.

### Consideraciones de seguridad
Este codigo es vulnerable a XSS. Una ves que la cookie user_ip es guardada en el browser, el usuario es capaz de modificarla y ejecutar lo que guste.

Para evitar esto, puede ser útil importar escape de flask, y hacer lo siguiente:

```python
@app.route("/hello")
def ip():
	user_ip = request.cookies.get('user_ip')
	user_ip = escape(user_ip)
	return "Tu ip es {}".format(user_ip)
```

## Templates con Jinja 2

Los templates son archivos HTML que permiten renderizar la información de una manera más amigable para el usuario.
Flask tiene un sistema de templates que permite renderizar los templates de manera sencilla.
Para usar los templates:

- Primero debemos crear un directorio llamado **templates** en la raíz de nuestro proyecto.
- Dentro de este directorio, creamos un archivo llamado **hello.html**.
- Luego, en nuestro archivo **app.py**, importamos el objeto **render_template** de flask.
- Finalmente, en nuestra ruta **/hello**, retornamos el template **hello.html**.

```python
from flask import Flask, request, make_response, redirect, render_template
app = Flask(__name__)
@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)
    return response

@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    return render_template('hello.html', user_ip=user_ip)
```


