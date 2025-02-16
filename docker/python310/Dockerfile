FROM python:3.10-slim
# Define un directorio de trabajo para tu aplicación
ONBUILD ADD app /app/
ADD ./ /app/

ONBUILD ADD app /app/aviso/conf
ONBUILD ADD app /app/lead/conf
ONBUILD ADD app /app/dataimport/

WORKDIR /app/dataimport
WORKDIR /app
# Instala las herramientas necesarias
RUN apt-get update -y
RUN apt-get install -y curl
# Instala el paquete 'openjdk-11-jre-headless'
RUN tar -xzf openjdk-11.0.2_linux-x64_bin.tar.gz -C /usr/local
RUN update-alternatives --install /usr/bin/java java /usr/local/jdk-11.0.2/bin/java 100
ENV JAVA_HOME=/usr/local/jdk-11.0.2

# Configura la variable de entorno JAVA_HOME
ENV JAVA_HOME=/usr/local/jdk-11.0.2


# Verifica que Python 3.10 se ha instalado correctamente
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#
RUN python3.10 -m pip install JPype1
RUN pip install uuid
