### Para correr el flask server:

##### Para instalar las dependencias de python usando pip

 ```bash
 sudo apt-get update && sudo apt-get -y upgrade
 sudo apt-get install python-pip
 ```

##### Para usar virtualenv y no tener todas las dependencias globales.
 
 ###### Instalar virtualenv
  ```bash
  pip install virtualenv
  ```
 
 ###### Generar un nuevo entorno virtual de nombre venv 
  ```bash
  virtualenv venv
  ```
  
 ###### Activar el entorno virtual
  ```bash
  . venv/bin/activate
  ```
##### Instalar dependencias
 ```bash
 pip install -r requirements.txt
 ```

##### Lanzar server
 ```bash
 python app.py
 ```

### EJEMPLOS DE USO más adelante
