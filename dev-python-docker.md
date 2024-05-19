# Docker con Flask


Para continuar el curso, y ya construido el contenedor usar los siguientes comandos para seguir usando el mismo contenedor:

```bash
source venv/bin/activate
docker start -a <id-contenedor>
```

Luego para finalizar:
  
  ```bash
  docker stop <id-contenedor>
  deactivate
  ```

**********************************************

Para construir la imagen y contenedor.


El original es con fastapi, pero adaptamos para Flask
La practica está en Projects/Platzi/docker/ flask-python-dev
Construimos la imagen

```bash
docker build -t flask-app .
```


Corremos el contenedor
```bash
docker run -it -p 5000:5000 -v $(pwd):/usr/src/app flask-app
```

Si ya está creado reutilizar los contenedores con:

docker stop [idContenedor]

docker start -a [idContenedor]















El Dockerfile completo para flask:
  
  ```Dockerfile
  FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt.

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY. /app

# Set the environment variable
ENV FLASK_APP=app.py

# Expose the port that the Flask app runs on
EXPOSE 5000

# Set the ENTRYPOINT command to run the Flask app with Markdown support
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000", "-m", "markdown"]

# Run the Flask app
CMD ["app.py"]

  ```

