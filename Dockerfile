# Base image para Lambda con Python 3.8
FROM public.ecr.aws/lambda/python:3.8

# Copiar el archivo de requerimientos a /var/task (directorio por defecto de Lambda)
COPY requirements.txt /var/task/

# Instalar las dependencias en /var/task (sin caché)
RUN pip install --no-cache-dir -r /var/task/requirements.txt --target /var/task/

# Copiar todo el contenido de la aplicación a /var/task/
COPY . /var/task/

# Comando para Lambda (asegúrate de que 'main.py' contiene un handler llamado 'handler')
CMD ["app.main.handler"]
