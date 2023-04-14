import fitz
from datetime import datetime
import numpy as np
from PIL import Image

# doc = fitz.open('C:/Users/rodri/Desktop/Pruebas.pdf')
# print('Comienza: '+ str(datetime.now()))
# count = 0
# for page in doc:
#     count+=1
#     pix = page.get_pixmap()
#     pix.save(f'docs/pagina_{count}.jpg')

print('Fin: '+ str(datetime.now()))

# for i in range(1,10):
#     doc = fitz.open(f'./docs/pagina_{i}.jpeg')
#     img = doc[0].get_pixmap(alpha=False)
#     img_arr = np.frombuffer(img.samples, dtype=np.uint8).reshape(img.height, img.width, 3)
#     img_gray = np.dot(img_arr[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
#     threshold = 150
#     img_bin = np.where(img_gray > threshold, 255, 0).astype(np.uint8)
#     print(img_bin)
#     fitz_pixmap = fitz.Pixmap(img_bin)
#     doc_bin = fitz.new_page(width=fitz_pixmap.width, height=fitz_pixmap.height)
#     doc_bin.insert_image(fitz.Rect(0, 0, fitz_pixmap.width, fitz_pixmap.height), pixmap=fitz_pixmap)
#     doc_bin.save(f'docs/plt-pagina_{i}.jpg')


# for i in range(1,10):
#     img  = fitz.open(f'docs/pagina_{i}.jpg')[0]
#     pixmap = fitz.Pixmap("ruta_de_la_imagen.jpg")
#     #gray_Img = img.get_pixmap.grayscale()

#     #result = image.threshold(127)    

#     #gray_Img.save(f'docs/imagen_binaria_{i}.jpg')
pdf_doc  = fitz.open("C:/Users/rodri/Desktop/Pruebas.pdf")

for pg in range(pdf_doc.page_count):
    page = pdf_doc[pg]
    pix = page.get_pixmap(alpha=False)
    img_bytes = pix.samples

    img = Image.frombytes('RGB', (pix.width, pix.height), img_bytes)
    img = img.convert('L')
    print(pg)
    #img.save()