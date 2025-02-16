# solr
imple
# **Proyecto de Implementación y Gestión de Solr**

Este proyecto proporciona un conjunto de comandos y configuraciones para el despliegue, la importación de datos, la creación de imágenes Docker y la gestión de contenedores Solr.

## **Secciones**

### **Deploy**
- **deploy-list-images**: Despliega las imágenes listadas en el proyecto.

### **GDataimport**
- **data-import-run**: Ejecuta el comando para importar datos a Solr.
  - Comando:
    ```bash
    make data-import-run CORE=santander_profession MODEL=full PARAMS=null
    ```

### **Global**
- **build-image-solr**: Crea una imagen Docker con las dependencias empaquetadas.

### **Local**
- **sync-container-config**: Sincroniza los archivos de configuración desde S3.
- **up**: Inicia el contenedor Docker.
- **down**: Destruye el proyecto, deteniendo y eliminando los contenedores Docker.
- **log**: Muestra los logs del contenedor Docker.
- **migrate**: Ejecuta las migraciones necesarias para el contenedor Docker.

## **Uso**

### **Deploy**
Para desplegar las imágenes en el proyecto, puedes usar el siguiente comando:

```bash
make deploy-list-images
