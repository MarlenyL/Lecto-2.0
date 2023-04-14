FROM ubuntu 

#Install updates
RUN apt-get update && \
      apt-get -y install sudo

#Install python3
RUN apt install python3 -y

#Adding Lecto
ADD Lecto_Fase-2 /home/Lecto_Fase-2

#Installing tesseract
#RUN sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel

#Echo for sudo
#RUN echo 'root' | passwd --stdin root 

#Other dependencies
RUN sudo apt install libtesseract-dev -y

#RUN sudo apt-get install tesseract-ocr-spa
#RUN sudo apt-get install tesseract-ocr-eng

#Virtual env
#RUN sudo apt install python3-env


#RUN python3 -m venv /home/Lecto_Fase-2/venv

#RUN source /home/Lecto_Fase-2/venv/bin/activate

#Installing dependencies
#RUN pip install -r /home/Lecto_Fase-2/requirements.txt

#Levanta el server
#RUN uvicorn /home/Lecto_Fase-2/lecto:app --reload