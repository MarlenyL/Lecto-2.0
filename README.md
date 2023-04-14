# Integrantes
-   Rocio Marleny
-   Christian Gerardo
-   Diana Sánchez
-   Rodrigo Valle

## comando para instalar todas las librerías

```
pip install -r requirements.txt
```

## Cosas que se instalarán

```
pip install scikit-image
pip install pytesseract
pip install spacy
pip install es-core-news-sm
pip install syltippy
pip install pdf2image
pip install fpdf
pip install PyPDF2==2.9
pip install fpdf2
pip install matplotlib
pip install fastapi
pip install uvicorn
pip install fitz   
pip install PyMuPDF
pip install numpy 
```


## Manera de ejecutarlo en visual studio/otro compilador

##### Si se quiere ejecutar con args parse ejecutar así

```
python lecto.py --Pdf <Ruta de pdf> --First <Primera pagina (1)> --Last <Ultima pagina (1)>
```

## Ejemplo

```
python lecto.py --Pdf 'C:/Users/user/Desktop/File.pdf' --First '1' --Last '1'
```

##### Si se quiere ejecutar sin args únicamente modificar en constants.py las variables:
-   PdfRoute
-   FirstPage
-   LastPage

Posterior se ejecuta así

```
python lecto.py
```


# Linux instalation of pytesseract
```
#Update the system
sudo apt update

#Add tesseract to the system 
sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel

#install tesseract
sudo apt install -y tesseract-ocr

#DEv tool
sudo apt install libtesseract-dev

#Install spanish
sudo apt-get install tesseract-ocr-spa

#Install ingles - a futuro
sudo apt-get install tesseract-ocr-eng
```


## Trabajar con FastApi (crea server y Api)

Deben irse a la carpeta del proyecto, ejecutar SIEMPRE todos los pasos (excepto el primero que solo una vez se ejecuta), no olvidar desactivar el ambiente

```
#Instala la librería de virtualenv
pip install virtualenv virtualenv

#Antes de este paso moverse desde terminal a donde está el proyecto
#Crea un ambiente virtual
virtualenv venv

#Activa el ambiente
venv\Scripts\activate

#Instala en el ambiente todas las librerías a utilizar
pip install -r requirements.txt

#Ejecuta el server
uvicorn lecto:app --reload

#Correr unicamente en consola
python lecto.py

#Desactiva el ambiente
deactivate
```

## Trabajar con FastApi en Linux

Deben irse a la carpeta del proyecto, ejecutar SIEMPRE todos los pasos (excepto el primero que solo una vez se ejecuta), no olvidar desactivar el ambiente

```
#Instala la librería de virtualenv
sudo apt install python3-env

#Antes de este paso moverse desde terminal a donde está el proyecto
#Crea un ambiente virtual
python3 -m venv env

#Activa el ambiente
source env/bin/activate


#Instala en el ambiente todas las librerías a utilizar
pip install -r requirements.txt

#Levanta el server
uvicorn lecto:app --reload

#Correr unicamente en consola
python lecto.py

#Desactiva el ambiente
deactivate
```


## Dentro del server

-   El index va a dar un mensaje de bienvenida
-   Para probar funcionalidades, en el buscador colocar:

```
http://127.0.0.1:8000/function/{Pdf}/{First Page}/{Last Page}

#Ejemplo
http://127.0.0.1:8000/function/User-Dektop-Pruebas/1/3


#Ver documentación de fastApi
http://127.0.0.1:8000/docs
```

**Cosas a considerar**
-   En el método Get el nombre del pdf debe de ir sin la extensión .pdf
-   Poner la ruta, omitiendo el C:/, sustituyendo cada / por -



# Instalacion de docket
 
-   Correr en terminal windows para instalar la terminal de linux.

 ```
wsl --install
 ```

-   Descargar de <a href='https://www.docker.com/products/docker-desktop/'>aquí</a> el instalador de docker para su sistema operativo.