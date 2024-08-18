import pandas as pd
import zipfile
import os
import requests
from pymongo import MongoClient
import matplotlib.pyplot as plt

# 1. Descargar el archivo .zip
url = "https://netsg.cs.sfu.ca/youtubedata/0333.zip"
zip_file_path = "0333.zip"

print("Descargando el archivo...")
response = requests.get(url)
with open(zip_file_path, 'wb') as file:
    file.write(response.content)
print("Archivo descargado.")

# 2. Descomprimir el archivo .zip
extracted_folder = "youtube_data"
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
print("Archivo descomprimido.")

# 3. Leer el archivo descomprimido con pandas

data_file = os.path.join(extracted_folder, os.listdir(extracted_folder)[0])
df = pd.read_csv(data_file, sep='\t', header=None)

df.columns = ["video_id", "uploader", "age", "category", "length", "views", "rate", "ratings", "comments", "related_ids"]

print(df.head())  

# 4. Quedarse con las columnas necesarias
df_filtered = df[["video_id", "age", "category", "views", "rate"]]

# 5. Realizar un filtrado básico (ejemplo: seleccionar ciertas categorías)
categorias_interes = ['Music', 'Comedy', 'Entertainment']
df_filtered = df_filtered[df_filtered['category'].isin(categorias_interes)]
print("Datos filtrados según las categorías de interés.")

# 6. Exportar los datos a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["youtube_db"]
collection = db["videos"]
collection.insert_many(df_filtered.to_dict('records'))
print("Datos exportados a MongoDB.")

# 7. Crear gráficos

# Gráfico 1: Distribución de visualizaciones por categoría
plt.figure(figsize=(10,6))
df_filtered.groupby('category')['views'].sum().plot(kind='bar')
plt.title('Distribución de Visualizaciones por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Visualizaciones')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizaciones_por_categoria.png")
plt.show()

# Gráfico 2: Calificación promedio por categoría
plt.figure(figsize=(10,6))
df_filtered.groupby('category')['rate'].mean().plot(kind='bar', color='orange')
plt.title('Calificación Promedio por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Calificación Promedio')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("calificacion_promedio_por_categoria.png")
plt.show()

print("Gráficos creados y guardados como imágenes.")

# Enlace de los datos en MongoDB:
print("Enlace de los datos: mongodb://localhost:27017/youtube_db.videos")
