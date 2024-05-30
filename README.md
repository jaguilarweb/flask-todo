# Curso Flask

Este proyecto se construye con base a notas del Curso de Flask. Este curso recorre los fundamentos del micro-framework Flask para Python. Al final del mismo se crea un proyecto TODO LIST, con un CRUD, usando extensiones como WTF, Bootstrap y Blueprints.

Nota personal: También aprovecho este curso para practicar el uso y configuración de contenedores Docker para crear mi ambiente de desarrollo; el uso de Git para prácticar comandos de esta herramienta de versionamiento y subir un repositorio remoto a Github; flask_testing para realizar pruebas unitarias y el uso de pip como manejador de dependencias de Python.

Plataforma: Platzi 

## ¿Qué es Flask?

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
Este codigo es vulnerable a XSS. Una vez que la cookie user_ip es guardada en el browser, el usuario es capaz de modificarla y ejecutar lo que guste.

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

## Incluir archivos estáticos

Para incluir archivos estáticos, como CSS, JS, imágenes, etc., debemos crear un directorio llamado **static** en la raíz de nuestro proyecto.

Luego, dentro de este directorio, creamos un directorio por tipo de archivo, css, imagenes, etc. 

Finalmente, en nuestro archivo HTML, incluimos los archivos estáticos con la función **url_for**.

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
```

En el caso de las imágenes, las referenciamos:

```html
<img src="{{ url_for('static', filename='img/logo.png') }}" alt="Logo">
```

## Páginas de error

Para manejar errores en Flask, debemos crear una función que maneje el error y retornar un template con el error.

Desde el archivo principal:

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404
```

## Bootstrap

Bootstrap es un framework de diseño que nos permite crear aplicaciones web de manera rápida y sencilla.
Para utilizar Bootstrap debemos incluir la librería en el archivo requirements.txt y luego ejecutar en la consola:
  
  ```bash
  pip install -r requirements.txt
  ```

Ahora podemos hacer uso de boostrap en la aplicación, así que lo agregamos:

```html
{% extends 'bootstrap/base.html' %}
```

Considerando que la plantilla de flask contiene bloques pre definidos [Bloques](https://pythonhosted.org/Flask-Bootstrap/basic-usage.html#templates) vamos a aprovechar esos recursos para reconfigurar nuestra plantilla base y así eliminar los elementos html innecesarios ya que se encuentran incluidos en los bloques de flask. Ejm: html, head, body, etc.


## Definir tipo de ambiente
Para definir el tipo de ambiente en el que se ejecutará nuestra aplicación, debemos crear una variable de entorno $FLASK_ENV.

Si definimos un ambiente de desarrollo la variable tomará el siguiente valor:
  
```bash
  export FLASK_ENV=development
```

Para el caso de estar usando Docker, definimos la variable en el Dockerfile:
  
```Dockerfile
  ENV FLASK_ENV=development
```

## Session en flask
Para manejar sesiones en flask, lo primero que debemos hacer es crear una llave secreta.
Para ello, utilizamos una propiedad del objeto 'app' llamada ´config´. Y es un diccionario que tiene llaves y valores. Una de esas llaves se llama `SECRET_KEY`.
  
  ```python
  app.config['SECRET_KEY'] = 'String_secreta'
  ```

Ahora podemos usar session para obtener información que antes pbteníamos de la cookie, pero en forma más segura porque encripta la información:

```python
@app.route('/')
def index():
    user_ip = request.remote_addr
    session['user_ip'] = user_ip
    return redirect(url_for('hello'))
```
  
  ```python
@app.route('/hello')
def hello():
    user_ip = session.get('user_ip')
    return render_template('hello.html', user_ip=user_ip, todos=todos)
```
Esto nos permitirá ver en el inspector del navegador, en la sección aplicación la siguiente información:
-----------------------------------------------------------------------------
|  Nombre   |       Valor       | Dominio  | Path | Expires | Tamaño | Http |
|-----------|-------------------|----------|------|---------|--------|------|
| session   | eyJ1c2VyX2lwIjoi  | 0.0.0.0  |  /   | Sesión  |  77    |  ✓   |
|           | MTkyLjE2OC42NS4xI |          |      |         |        |      |
|           | n0.ZlYpZw.7E-27c5 |          |      |         |        |      |
|           | lfN2RfsxjajRa0Hoz |          |      |         |        |      |
|           | b3s               |          |      |         |        |      |


### Objetos de flask

- request: Información sobre la petición que realiza el browser
- session: Storage que permanece entre cada request
- g: Objeto que se usa para almacenar información temporal durante el ciclo de vida de la aplicación. Storage temporal, se reinicia en cada request.
- current_app: Punto de acceso al objeto de la aplicación actual. Información sobre la aplicación actual.


## Formularios (Formas)
Flask tiene un objeto llamado `form` que nos permite crear formularios en la web
Para ello debemos importar `FlaskForm` de `flask_wtf` y `StringField`, `SubmitField` de `wtforms`.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
```

Ahora podemos crear un formulario con el siguiente código:
  
  ```python
class TodoForm(FlaskForm):
    todo = StringField('Todo')
    submit = SubmitField('Enviar')
  ```

Para renderizarlo lo enviamos en el contexto desde la ruta '/' a hello.html.
Y en ese archivo renderizamos:

```html
  <div class="container">
    <form action="{{ url_for('hello') }}" method="post">
      {{ loginForm.username }}
      {{ loginForm.username.label }}
    </form>
```

Para aprovechar los estilos, también podemos hacer uso de un quick_form.
Quick_form: 
- Es una macro que nos permite renderizar un formulario de manera rápida.
  
  ```html
    <div class="container">
      {{ quick_form(loginForm) }}
    </div>
  ```

## Validación de formularios
Para validar formularios en flask, debemos importar `DataRequired` de `wtforms.validators`.

```python
from wtforms.validators import DataRequired
```

Ahora podemos agregar validaciones a los campos del formulario.

```python
class TodoForm(FlaskForm):
    todo = StringField('Todo', validators=[DataRequired()])
    submit = SubmitField('Enviar')
```

## Agregar metodo post

Para agregar un método post a una ruta, debemos importar `request` de `flask`.

```python
from flask import request
```
Y en la ruta, debemos agregar el método post.
  
  ```python
  @app.route('/', methods=['GET', 'POST'])
  ```

## Mensajes de error
Para agregar mensajes de error, debemos importar `flash` de `flask`.
  
  ```python
  from flask import flash
  ```
Y en la ruta, agregamos un mensaje de error.
  
  ```python
  @app.route('/', methods=['GET', 'POST'])
  def index():
      user_ip = request.remote_addr
      todo_form = TodoForm()
      if todo_form.validate_on_submit():
          flash('La tarea se ha agregado con éxito')
          return redirect(url_for('hello'))
      return render_template('hello.html', user_ip=user_ip, todos=todos, form=todo_form)
  ```

Para mostrar el mensaje de error en la plantilla, debemos agregar el siguiente código:
  
  ```html
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
  ```

  ## flask-testing
  Para realizar pruebas en flask, debemos instalar la librería `flask-testing`.
  
  ```bash
  pip install flask-testing
  ```
  Recordar que otra forma de instalar estas dependecias es incluirlas directamente en el archivo requirements.tx y luego correr:
    
  ```bash
  pip install -r requirements.txt
  ```

Ahora podemos utilizar las clases.
Vamos a crear un comando para correr las pruebas.
Para lo anterior, vamos al archivo principal y escribimos el siguiente código:

```python
@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
```

Ahora creamos un directorio llamado `tests` en la raíz de nuestro proyecto.

Dentro de este directorio, creamos un archivo llamado `test_basics.py`.

En este archivo, importamos `unittest` y `TestCase` de `flask_testing`.

```python
import unittest
from flask_testing import TestCase
```

Ahora creamos una clase llamada `TestBasics` que hereda de `TestCase`.

```python
class TestBasics(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assert_200(response)
```

Para correr las pruebas, ejecutamos el siguiente comando en la consola:

```bash
flask test
```
