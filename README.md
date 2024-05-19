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

## Estructuras de control en Jinja2

Las estructuras de control nos permiten controlar el flujo de nuestra aplicación.
Ejemplo de su uso con if/else:

```html
{% if user_ip %}
<h1>Hello navegador, tu IP es {{user_ip}}</h1>
{% else %}
<a href="{{ url_for('index') }}">Ir a inicio</a>
{% endif %}
```

## Ciclos en Jinja 2
Los ciclos nos permiten iterar sobre una lista de elementos.
Para ello creamos una lista en el archivo app.py. que luego enviaremos a la plantilla.

```python
todos = ['Tarea 1', 'Tarea 2', 'Tarea 3']
@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')

    return render_template('hello.html', user_ip=user_ip, todos=todos)
```

Para evitar enviar tantos parametros al template, utilizamos el contexto.
Contexto es:
- Un diccionario de datos que se envía a la plantilla.
  
  ```python
  return render_template('hello.html', **context)
  ```

Con esta forma de enviar el contexto evitamos, además, el tener que utilizar la forma context.atributo en la plantilla.

## Heredar templates

Heredar templates, extender templeates o incluir templates en otros templates, es una funcionalidad muy útil porque:
- Nos permite reutilizar código.
- Nos permite tener una estructura de archivos más organizada.
- Nos permite tener un código más limpio.
- Nos permite tener un código más legible.
- Nos permite tener un código más mantenible.

Para heredar un template, debemos crear un archivo base.html que contenga la estructura base de nuestra aplicación. Y es este el que extendemos en los otros templates.

base.html
```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask app | {% endblock %}</title>
  </head>
  <body>
    {% block content %}
    {% endblock %}
  </body>
  </html>
```

hello.html
```html
{% extends 'base.html' %}
{% block title %}
  {{ super() }}
  Bienvenido 
{% endblock %}

{% block content %}
  {% if user_ip %}
    <h1>Hello navegador, tu IP es {{user_ip}}</h1>
  {% else %}
    <a href="{{ url_for('index') }}">Ir a inicio</a>
  {% endif %}
    <ul>
      {% for todo in todos %}
        <li>{{todo}}</li>
      {% endfor %}
    </ul>
{% endblock %}
```
Luego utilizamos las macros:
- Macros: Son bloques de código que se pueden reutilizar en diferentes partes de la aplicación.
- Para crear una macro, utilizamos la palabra clave **macro**.
- Para utilizar una macro, utilizamos la palabra clave **import**.
- Creamos un archivo macros.html
- Declaramos la macro en el inicio del archivo seguido del nombre, el cual en este caso recibirá un parámetro todo. Luego declaramos donde termina el macro.

```html
{% macro render_todo(todo) %}
  <li>{{todo}}</li>
{% endmacro %}
```