import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import cv2
import io

"""
# Computer Vision
## Liveness Detection

O detector de Liveness (Vivacidade) tem por objetivo estabelecer um índice que atesta o quão 
confiável é a imagem obtida pela câmera.
Imagens estáticas, provindas de fotos manipuladas, são os principais focos de fraude neste tipo de validação.
Um modelo de classificação deve ser capaz de ler uma imagem da webcam, classificá-la como (live ou não) e 
exibir sua probabilidade da classe de predição.

"""

uploaded_file = st.file_uploader('Tente uma outra imagem', type=["png", "jpg"])
if uploaded_file is not None:
    img_stream = io.BytesIO(uploaded_file.getvalue())
    imagem = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)
    st.image(imagem, channels="BGR")


camera = st.camera_input("Tire sua foto", help="Lembre-se de permitir ao seu navegador o acesso a sua câmera.")

if camera is not None:
    bytes_data = camera.getvalue()
    imagem = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)


if camera or uploaded_file:

    with st.spinner('Classificando imagem...'):
        imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        classificador_face = cv2.CascadeClassifier('streamlit-app//haarcascade_frontalface_default.xml')
        faces = classificador_face.detectMultiScale(imagem_gray, 1.3, 3)

        imagem_anot = imagem.copy()

        for (x, y, w, h) in faces:
            cv2.rectangle(imagem_anot, (x, y), (x+w, y+h), (0, 0, 255), 2)

        st.image(imagem_anot, channels="BGR")
    
    st.success('Imagem com Vivacidade, probabilidade de 87%!')