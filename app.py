# Importar las librerías necesarias
import streamlit as st
import pandas as pd
import qrcode
from pathlib import Path
import os
import zipfile

# Crear una carpeta para guardar los códigos QR
if not os.path.exists('qrcodes'):
    os.makedirs('qrcodes')

st.title('Generador de códigos QR')

# Solicitar el archivo al usuario
uploaded_file = st.file_uploader("Carga tu archivo .xlsx", type='xlsx')

if uploaded_file is not None:
    # Leer el archivo
    archivo_excel = pd.read_excel(uploaded_file)

    # Iterar sobre cada fila
    for index, fila in archivo_excel.iterrows():
        # Construir el contenido del QR a partir de todos los datos de la fila
        contenido_qr = '\n'.join([f"{columna}: {fila[columna]}" for columna in archivo_excel.columns])

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(contenido_qr)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Obtener el número de la primera columna para el nombre del archivo
        numero_fila = fila.iloc[0]

        # Guardar el QR en el directorio con el nombre basado en el número de la fila
        img.save(f"qrcodes/qr_{numero_fila}.png")

    # Crear un archivo zip
    with zipfile.ZipFile('qrcodes.zip', 'w') as zipf:
        for file in os.listdir('qrcodes'):
            zipf.write(os.path.join('qrcodes', file))

    # Proporcionar un enlace para descargar el archivo zip
    if os.path.exists('qrcodes.zip'):
        st.download_button(
            label="Descargar códigos QR",
            data=open('qrcodes.zip', 'rb'),
            file_name="qrcodes.zip",
        )
