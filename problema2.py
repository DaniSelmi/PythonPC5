import pandas as pd
import sqlite3
from pymongo import MongoClient

# Paso 1: Cargar el dataset y explorar el dataframe
df = pd.read_csv('winemag-data-130k-v2.csv')
print(df.head())
print(df.info())
print(df.describe())

# Paso 2: Renombrar columnas
df.rename(columns={
    'country': 'pais',
    'points': 'puntos',
    'price': 'precio',
    'winery': 'bodega'
}, inplace=True)

# Crear nuevas columnas
# 1. Crear una columna "continente" según el país
continente_map = {
    'US': 'América',
    'France': 'Europa',
    'Italy': 'Europa',
    'Chile': 'América',
    'Argentina': 'América',
    # agregar más países según el dataset
}
df['continente'] = df['pais'].map(continente_map)

# 2. Crear una columna "rango_precio" para clasificar los vinos según el precio
df['rango_precio'] = pd.cut(df['precio'], bins=[0, 20, 50, 100, 500], labels=['Bajo', 'Medio', 'Alto', 'Muy Alto'])

# 3. Crear una columna "calidad" según los puntos
df['calidad'] = pd.cut(df['puntos'], bins=[0, 85, 90, 95, 100], labels=['Regular', 'Buena', 'Muy Buena', 'Excelente'])

# Paso 3: Generar reportes

# Reporte 1: Promedio de precio por continente
reporte1 = df.groupby('continente')['precio'].mean().reset_index()
reporte1.to_csv('reporte1.csv', index=False)

# Reporte 2: Cantidad de vinos por calidad y continente
reporte2 = df.groupby(['continente', 'calidad']).size().reset_index(name='cantidad')
reporte2.to_excel('reporte2.xlsx', index=False)

# Reporte 3: Mejores vinos por país (máxima puntuación)
reporte3 = df.loc[df.groupby('pais')['puntos'].idxmax()]
conn = sqlite3.connect('reporte3.sqlite')
reporte3.to_sql('mejores_vinos', conn, if_exists='replace', index=False)

# Reporte 4: Promedio de puntos y precio por país
reporte4 = df.groupby('pais').agg({'puntos': 'mean', 'precio': 'mean'}).reset_index()

# Guardar el reporte 4 en MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['wine_db']
collection = db['reporte4']
collection.insert_many(reporte4.to_dict('records'))

print("Reportes generados y guardados en diversos formatos.")

# Paso 4: Enviar uno de los reportes por correo (simulado aquí con un print)
# Ejemplo para enviar el reporte1 por correo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def enviar_correo():
    sender_email = "tu_correo@gmail.com"
    receiver_email = "destinatario@gmail.com"
    subject = "Reporte de Vinos"
    body = "Adjunto el reporte de vinos en formato CSV."

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Adjuntar el cuerpo del correo
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo
    filename = "reporte1.csv"
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    
    msg.attach(part)

    # Enviar el correo
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, "tu_contraseña")
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

    print("Correo enviado con éxito.")

# Simulación de enviar el correo
enviar_correo()