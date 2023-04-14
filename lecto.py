import os
import re
from spacy import load, parts_of_speech, lexeme, tokens

import matplotlib
import matplotlib.pyplot as plt
import pytesseract
import skimage.io
import es_core_news_sm
from constants import *
from skimage.color import rgb2gray
from skimage.filters import (threshold_otsu, thresholding)

from syltippy import syllabize
from PIL import Image
from pdf2image import convert_from_path
from perspicuity.perspicuity import *
import json
from datetime import datetime
import argparse
from math import ceil
from pdf import *


#librerías relacionadas a la api y server
from fastapi import FastAPI

#Librerias procesos paralelos
from multiprocessing import Pool


#Aplicacion Apifast
app = FastAPI()


number_pages = 0
first_page = 1
last_page = 1
Image.MAX_IMAGE_PIXELS = None
basedir = os.path.dirname(__file__)
current_date = ''
global file_pil_images
import fitz
import numpy as np


#Convierte las páginas de un archivo PDF a imágenes y las guarda en un arreglo
def create_images_from_file(values, Lista):
    file_pil_images = []
    for page in range(values['first_page'], values['last_page']+1, 10):
        file_pil_images.extend(convert_from_path(values['file_path'], dpi=900, first_page=Lista[0], last_page = Lista[len(Lista)-1]))
        
    Count = 1
    Aux = []
    for i in range(len(Lista)):
        Aux.append((file_pil_images[i],i))
        if Count==5 and i!= (len(Lista)-1):
            Pool().map(create_images, Aux)
            Count = 0
            Aux = []
        else:
            Count+=1
        if i == (len(Lista)-1):
            Pool().map(create_images, Aux)

def deletePlot():
    try:
        os.remove('docs/plot-FernandezHuerta-hist.png')
        os.remove('docs/plot-MuLegibility-hist.png')
        os.remove('docs/plot-resByParagraph.png')
        os.remove('docs/plot-SzigrisztPazos-hist.png')
    except Exception as e:
        return None

def TestFuntion(Pdf, First, Last):
    pdf_doc  = fitz.open(Pdf)
    Aux =1
    for pg in range(First-1, Last):
        page = pdf_doc[pg]
        pix = page.get_pixmap(alpha=False)
        img_bytes = pix.samples

        img = Image.frombytes('RGB', (pix.width, pix.height), img_bytes)
        img = img.convert('L')
        img.save(f'docs/plt-pagina_{Aux}.jpg')
        Aux+=1


#Guarda las imágenes creadas en la ruta especificada
def create_images(Aux):
    file_path = define_file_path(f'pagina_'+ str(Aux[1]+1) + '.jpg')
    Aux[0].save(file_path, 'JPEG')


def Binarizacion(i):
    file_name = define_file_name(i)

    text = str(((pytesseract.image_to_string(Image.open(DOCS_ROUTE+'plt-'+file_name),lang='spa',config='-c page_separator='' '))))
    text = text.replace('-\n', '')

    open(OUTPUT_TEXT, "a", encoding="utf-8").write(text)
    #print(f'fin hoja {i}')


#La imagen se convierte primero a escala de grises y luego se binariza para obtener mejores resultados
def refine_image(Lista):

    Count = 1
    Aux = []
    var = 1
    for i in range(len(Lista)):
        Aux.append(var)
        var+=1
        if Count==5 and i!= (len(Lista)-1):
            Pool().map(Binarizacion, Aux)
            Count = 0
            Aux = []
        else:
            Count+=1
        if i == (len(Lista)-1):
            Pool().map(Binarizacion, Aux)




    open(OUTPUT_TEXT, "a", encoding="utf-8").close()

#Se crea la imagen binarizada y se guarda. La imagen en escala de grises se desecha 
def plot_image(plot_configs, binary_otsu):
    matplotlib.rcParams['font.size'] = 12
    mult=5
    plt.figure(figsize=((int)(plot_configs['width']/plot_configs['dpi'])*mult, (int)(plot_configs['height']/plot_configs['dpi'])*mult))
    plt.imshow(binary_otsu, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig(plot_configs['file_path'], bbox_inches='tight')
    plt.cla()
    plt.close()

def define_file_name(number): 
    return 'pagina_'+ str(number) + '.jpg'

def define_file_path(file_name):
    return DOCS_ROUTE+file_name

#Elimina las imagenes originales, a las que no se les ha aplicado ningún algoritmo de procesamiento de imágenes
def delete_files(first_page, last_page):
    global number_pages
    number_pages = number_pages
    for i in range(1, last_page-first_page+2):
        file_name = define_file_name(i)
        file_path = define_file_path(file_name)
        try:
            #os.remove(file_path)
            os.remove(DOCS_ROUTE+'plt-'+file_name)
        except Exception as e:
            continue

#Devuelve el texto depurado 
def refine_text(Lines):
    raw_text = extract_file_text(Lines)
    return substract_from_text(raw_text)

#Junta todas las líneas de un texto en una sola variable
def extract_file_text(Lines):
    text_raw = ''
    for line in Lines:
        text_raw += line
    return text_raw

#Limpia el texto usando expresiones regulares
def substract_from_text(raw_text):
    raw_text = re.sub(r'[0-9]+([\.\,\+\-\*\/][0-9]+)*(%*)', '', raw_text)
    raw_text = re.sub(r'@', '', raw_text)
    raw_text = re.sub(r'(\.|\!|\?|\:)[\r\n\v\f][\r\n\v\f ]+', r'\1@', raw_text)
    raw_text = re.sub(r'(\[[ \t]*\])*(\([ \t]*\))*(\{[ \t]*\})*', '', raw_text)
    raw_text = re.sub(r'([ \t][ \t]+)', ' ', raw_text)
    raw_text = raw_text.encode("latin-1","ignore").decode("latin-1")
    refined_text = re.sub(r'[\r\n\t\v\f]+', ' ', raw_text)
    return refined_text

#Cuenta la cantidad de frases en un párrafo  
def calculate_phrases(phrases): 
    counter = 0
    
    for phrase in phrases:
        counter += 1
    return counter

#Cuenta la cantidad de palabras en un párrafo
def calculate_words(words):
    counter = 0
    
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            counter += 1
    return counter

#Cuenta la cantidad de sílabas en un párrafo
def calculate_syllables(words):
    syllables_counter = 0
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            syllables_counter += get_word_syllables(word)
    return syllables_counter

#Extrae las sílabas de cada palabra
def get_word_syllables(word):
    syllables, stress = syllabize(u'{}'.format(word.text))
    return len(syllables)

#Cuenta las letras en una palabra
def get_letters_per_word(words):
    letters_counter = []
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            letters_counter.append(len(word))
    
    return letters_counter

#Evalúa las fórmulas de perspicuidad con los datos obtenidos y obtiene los resultados
def calculate_perspicuity(perspicuity_values):
    return {
        SIGRISZPAZOS: round(SzigrisztPazos(perspicuity_values).calculate(),2),    
        FERNANDEZHUERTA: round(FernandezHuerta(perspicuity_values).calculate(),2),
        MULEGIBILITY: round(MuLegibility(perspicuity_values).calculate(),2),
    }

def clean_file(file):
    open(file, "w", encoding="utf-8").close()

#Función principal que maneja todo el flujo del programa
def process_file(Param):
    global current_date
    clean_file(OUTPUT_TEXT)
    clean_file(OUTPUT_FILE)

    save_route = 'C:/Users/rodri/Desktop/Git/Lecto_fase-2/'

    
    Lista = []
    for i in range(Param[1],Param[2]+1):
        Lista.append(i)    

    #Proceso paralelizado
    TestFuntion(Param[0], Param[1], Param[2])
    refine_image(Lista)

    delete_files(Param[1], Param[2])

    nlp = es_core_news_sm.load()

    szigriszt_values = []
    fernandez_huerta_values = []
    mu_legibility_values = []
    general_values = []

    with open(OUTPUT_FILE, "a", encoding="utf-8") as text_file:
        pharagraphs = []
        raw_file = open(OUTPUT_TEXT, "r", encoding="utf-8")
        Lines = raw_file.readlines()
        refined_text = refine_text(Lines)
        pharagraphs = refined_text.split('@')
        pharagraphs = list(filter(None, pharagraphs))
        csvSeparator = ";"

        Text = 'Parrafo'+csvSeparator+SIGRISZPAZOS_TEXT+'/'+INFLESZ_TEXT+csvSeparator+FERNANDEZHUERTA_TEXT+csvSeparator+MULEGIBILITY_VAR_TEXT

        plotData = {
            SIGRISZPAZOS: [],
            FERNANDEZHUERTA: [],
            MULEGIBILITY: []
        }
        paragraphsNumbers = []

        for index, pharagraph in enumerate(pharagraphs):
            tokenized_pharagraph = nlp(pharagraph)

            letters_counter = get_letters_per_word(tokenized_pharagraph)

            word_counter = calculate_words(tokenized_pharagraph)
            phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
            syllables_counter = calculate_syllables(tokenized_pharagraph)
            
            perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter }
            result = calculate_perspicuity(perspicuity_values)

            paragraphsNumbers.append(index+1)
            plotData[SIGRISZPAZOS].append(result[SIGRISZPAZOS])
            plotData[FERNANDEZHUERTA].append(result[FERNANDEZHUERTA])
            plotData[MULEGIBILITY].append(result[MULEGIBILITY])

            #Armando objetos para obtener las tablas de mejores y peores
            sigrizt_result = {"parrafo": str(index), "indice_perspicuidad": str(result[SIGRISZPAZOS])}
            fernandez_result = {"parrafo": str(index), "indice_perspicuidad": str(result[FERNANDEZHUERTA])} 
            mu_result = {"parrafo": str(index), "indice_perspicuidad": str(result[MULEGIBILITY])} 
            general_result = {"parrafo": str(index), "indice_perspicuidad": str((result[SIGRISZPAZOS]+result[FERNANDEZHUERTA]+result[MULEGIBILITY])/3.0)} 
            #Agregando cada objeto en arreglo de cada tipo
            szigriszt_values.append(sigrizt_result)
            fernandez_huerta_values.append(fernandez_result)
            mu_legibility_values.append(mu_result)
            general_values.append(general_result)

            #Validar si la propiedad gen_csv viene true para generar en el archivo csv los indices que necesitamos
            Value = str(index) + csvSeparator + str(result[SIGRISZPAZOS])  + csvSeparator + str(result[FERNANDEZHUERTA])+ csvSeparator + str(result[MULEGIBILITY])
            results = []
            pdf_complete_report = []
            final_analysis = {"parrafo": pharagraph, "palabrasParrafo":word_counter, "frasesParrafo":phrases_counter, "silabasParrafo":syllables_counter, 'perspicuidad':result}
            results.append([pharagraph, final_analysis])
        plot_aggregate_results(paragraphsNumbers, plotData)

        #Crea el json
        jsonFile = dict(zip(Text.split(';'), Value.split(';')))

        #PDF
        sorted_formulas = sort_formulas_results(general_values)
        
        szigriszt_average = calculate_average_formulas(szigriszt_values)
        fernandez_huerta_average = calculate_average_formulas(fernandez_huerta_values)
        mu_average = calculate_average_formulas(mu_legibility_values)

        for result in results:
            print(result, file=text_file)
        values_to_print = {}
        values_to_print = {SIGRISZPAZOS: {"value": szigriszt_average, "name": SIGRISZPAZOS_TEXT}, FERNANDEZHUERTA: {"value": fernandez_huerta_average, "name": FERNANDEZHUERTA_TEXT}, "LegibilidadMu": {"value": mu_average,"name": MULEGIBILITY_VAR_TEXT}, "Inflesz": {"value": szigriszt_average, "name": INFLESZ_TEXT}}
        #generatePDF(values_to_print, save_route, Param[0], sorted_formulas, pdf_complete_report, len(pharagraphs))
        deletePlot()



        return jsonFile
    
############    
#Apartado PDF
############
def sort_formulas_results(formulas):
    return sorted(formulas, key=lambda x: float(x["indice_perspicuidad"]), reverse=True)
#Obtiene el índice de perspicuidad promedio de todos los párrafos por cada fórmula 
def calculate_average_formulas(formula):
    counter = 0
    total_sum = 0

    for table_object in formula:
        counter += 1
        total_sum += float(table_object[SORT_FIELD])
    
    if counter == 0:
        return 0
    average = total_sum/counter
    return round(average, 2)

#Crea todos los gráficos que se agregan al PDF de resultados
def plot_aggregate_results(paragraphsNumbers, plotData):
    bins = [0,10,20,30,40,50,60,70,80,90,100]
    plt.clf()
    plt.figure(figsize=[5.5,5], dpi=100)
    plt.hist(plotData[SIGRISZPAZOS], bins, color = "blue", ec = "black")
    plt.ylabel(LABEL_CANT_PARRAFOS)
    plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
    plt.title('Resultados de '+SIGRISZPAZOS_TEXT+'/'+INFLESZ_TEXT);
    plt.savefig(DOCS_ROUTE+PLOT_SIGRISZPAZOS)
    plt.clf()
    plt.figure(figsize=[5.5,5], dpi=100)
    plt.hist(plotData[FERNANDEZHUERTA], bins, color = "red", ec = "black")
    plt.ylabel(LABEL_CANT_PARRAFOS)
    plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
    plt.title('Resultados de '+FERNANDEZHUERTA_TEXT);
    plt.savefig(DOCS_ROUTE+PLOT_FERNANDEZHUERTA)
    plt.clf()
    plt.figure(figsize=[5.5,5], dpi=100)
    plt.hist(plotData[MULEGIBILITY], bins, color = "green", ec = "black")
    plt.ylabel(LABEL_CANT_PARRAFOS)
    plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
    plt.title('Resultados de '+MULEGIBILITY_TEXT);
    plt.savefig(DOCS_ROUTE+PLOT_MULEGIBILITY)
    plt.clf()
    plt.figure(figsize=[10,6], dpi=250)
    plt.xlabel(LABEL_NUM_PARRAFO)
    plt.ylabel(LABEL_VALOR_PERSPICUIDAD)
    plt.title('');
    plt.grid(True)
    plt.plot(paragraphsNumbers, plotData[SIGRISZPAZOS], color='blue', marker='.', label=(SIGRISZPAZOS_TEXT+'/'+INFLESZ_TEXT))
    plt.plot(paragraphsNumbers, plotData[FERNANDEZHUERTA], color='red', marker='.', label=FERNANDEZHUERTA_TEXT)
    plt.plot(paragraphsNumbers, plotData[MULEGIBILITY], color='green', marker='.', label=MULEGIBILITY_TEXT)
    plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",mode="expand", borderaxespad=0, ncol=3)
    plt.ylim(ymin=0)
    plt.savefig(DOCS_ROUTE+PLOT_PARAGRAPHS)
    plt.clf()

def generatePDF(values_to_print, file_route, file_name, sorted_formulas, pdf_complete_report, number_of_pharagraphs):
    global current_date
    pdf = PDF()
    pdf.add_page()
    pdf.titles("ANÁLISIS DE LEGIBILIDAD")
    pdf.print_resumen(values_to_print, file_name)
    pdf.print_complete_report(pdf_complete_report, sorted_formulas, number_of_pharagraphs)
    pdf.add_page()
    pdf.seccion("Anexos")
    pdf.anexos()
    pdf.output(file_route+'/Resultados de análisis.pdf','F')
##############
#Fin apartado PDF
#############

#Con esto se obtiene toda la ruta del pdf excepto el archivo.pdf
def gettinRoute(Param):
    List =  Param[0].split('/')[0:len(Param[0].split('/'))-1]
    line=''
    for i in List:
        line += (i+'/')
    Param.append(line)

    return Param



@app.get("/")
def index():    
    return 'Bienvenido!'


@app.get("/function/{Pdf}/{First}/{Last}")
def PrincipalFunction(Pdf: str, First: int, Last: int):
    #Sustituye - por / para enviar la ruta en el navegador/URL
    Aux = Pdf.replace("-","/")
    #Agrega extension .pdf
    PdfLoc = f"C:/{Aux}.pdf"

    #Arreglo con datos a utilizar
    Param = [PdfLoc, First, Last]

    #Separa el nombre del archivo de la ruta de pdf
    Param = gettinRoute(Param)


    #Funcion principal
    Results = process_file(Param)
    return Results

def TestFun():
    TimeList = []
    for i in os.listdir('input_folder'):
        Init = datetime.now()
        Last = int(re.findall(r'\d+', i)[0])
        Loc = f'input_folder/{i}'
        print(f'Leyendo {Loc}')
        process_file([Loc,1,Last])
        End = datetime.now()
        Aux = f'{Last},{End-Init}'
        TimeList.append(Aux)     
    with open('docs/Results.csv', 'w') as f:
        for elemento in TimeList:
            f.write(elemento + '\n')


#Codigo para ejecutar programa en consola
if __name__ == '__main__':
    # Pdf = 'Users-rodri-Desktop-a'
    # First = 3
    # Last = 152

    # #Sustituye - por / para enviar la ruta en el navegador/URL
    # Aux = Pdf.replace("-","/")
    # #Agrega extension .pdf
    # PdfLoc = f"C:/{Aux}.pdf"

    # #Arreglo con datos a utilizar
    # Param = [PdfLoc, First, Last]

    # #Separa el nombre del archivo de la ruta de pdf
    # Param = gettinRoute(Param)


    # print('Inicio: '+ str(datetime.now()))
    # #Funcion principal
    # #print(process_file(Param))
    # print('Fin: '+ str(datetime.now()))
    TestFun()

