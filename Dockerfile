FROM alpine:3.10

# Install required packages
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

COPY . usr/src/app
    
WORKDIR /usr/src/app

RUN pip3 --no-cache-dir install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

EXPOSE 5000

ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

