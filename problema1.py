import pandas as pd

df_airbnb = pd.read_csv("./data/airbnb.csv")

######## Ejercicio 1 - Realizar un analisis exploratorio de los datos

# Ver las primeras filas del dataset
print(df_airbnb.head())

# Dimensiones del dataset
print("Shape:", df_airbnb.shape)

# Nombre de las columnas
print("Columns:", df_airbnb.columns)

# Resumen estadístico de las columnas numéricas
print(df_airbnb.describe())

# Información general del dataset (tipos de datos, valores nulos, etc.)
print(df_airbnb.info())

# Verificar si hay valores nulos
print(df_airbnb.isnull().sum())

######## Ejercicio 2 - Realizar Filtrados a Datos

##### Caso 1: Alicia y su familia
# Cumplir con las condiciones
df_alicia = df_airbnb[(df_airbnb['reviews'] > 10) & (df_airbnb['overall_satisfaction'] > 4)]

# Ordenar por puntuación y luego por número de críticas
df_alicia = df_alicia.sort_values(by=['overall_satisfaction', 'reviews'], ascending=[False, False])

# Mostrar las 3 mejores opciones
print(df_alicia.head(3))


##### Caso 2: Roberto y Clara

# IDs de las propiedades de Roberto y Clara
roberto_id = 97503
clara_id = 90387

# Filtrar las propiedades de Roberto y Clara
df_roberto_clara = df_airbnb[(df_airbnb['room_id'] == roberto_id) | (df_airbnb['room_id'] == clara_id)]

# Guardar el resultado en un archivo Excel
df_roberto_clara.to_excel("roberto.xls", index=False)

print(df_roberto_clara)

##### Caso 3: Diana y su presupuesto

# Filtrar las propiedades con un precio menor o igual a 50€
df_diana = df_airbnb[df_airbnb['price'] <= 50]

# Dar preferencia a las habitaciones compartidas
df_shared_rooms = df_diana[df_diana['room_type'] == 'Shared room']

# Ordenar las habitaciones compartidas por puntuación (de mayor a menor)
df_shared_rooms = df_shared_rooms.sort_values(by='overall_satisfaction', ascending=False)

# Si no hay suficientes habitaciones compartidas, agregar otros tipos de habitaciones
if len(df_shared_rooms) < 10:
    df_remaining = df_diana[df_diana['room_type'] != 'Shared room']
    df_remaining = df_remaining.sort_values(by='price', ascending=True)
    df_diana_final = pd.concat([df_shared_rooms, df_remaining.head(10 - len(df_shared_rooms))])
else:
    df_diana_final = df_shared_rooms.head(10)

print(df_diana_final)


######## Ejercicio 3 - Realizar Agrupamientos de Datos

# Agrupamiento 1: Precio promedio por vecindario
precio_promedio_vecindario = df_airbnb.groupby('neighborhood')['price'].mean().reset_index()
precio_promedio_vecindario = precio_promedio_vecindario.sort_values(by='price', ascending=False)
print(precio_promedio_vecindario)

# Agrupamiento 2: Número de alojamientos por tipo de propiedad
alojamientos_por_tipo = df_airbnb.groupby('room_type').size().reset_index(name='count')
print(alojamientos_por_tipo)

import matplotlib.pyplot as plt
import seaborn as sns

# Gráfico del precio promedio por vecindario
plt.figure(figsize=(10, 6))
sns.barplot(x='price', y='neighborhood', data=precio_promedio_vecindario, palette='viridis')
plt.title('Precio Promedio por Vecindario en Lisboa')
plt.xlabel('Precio Promedio (€)')
plt.ylabel('Vecindario')
plt.show()

# Gráfico del número de alojamientos por tipo de propiedad
plt.figure(figsize=(8, 6))
sns.barplot(x='room_type', y='count', data=alojamientos_por_tipo, palette='muted')
plt.title('Número de Alojamientos por Tipo de Propiedad')
plt.xlabel('Tipo de Propiedad')
plt.ylabel('Número de Alojamientos')
plt.show()