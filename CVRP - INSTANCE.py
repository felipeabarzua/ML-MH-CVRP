#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[92]:


# RECOPILACION DE DATOS 

# Lectura de las instancias de CVRPLIB

#A-n32-k5

# PRIMERO DEBEMOS LEER DEL ARCHIVO 

import numpy as np 
import pandas as pd 

# Nombre de la instancia 
fname = 'Augerat/A-n80-k10.vrp'

#DONDE

# A : AUTOR DE LA INSTANCIA 
# N : NÚMERO DE NODOS O CIUDADES A VISITAR
# K : NÚMERO DE VEHICULOS DISPONIBLES

# CREAMOS UNA VARIABLE LINEAS COMO LISTA PARA ALMACENAR LA DATA DE LA INSTANCIA

lineas = []

# ABRIMOS LA INSTANCIA Y RECOPILAMOS LA DATA COMO LISTA

with open (fname , 'rt') as f:
    for f_lineas in f:
        lineas.append(f_lineas)

# OBTENIENDO CAPACIDAD DE LOS VEHICULOS,CANTIDAD DE NODOS,CANTIDAD DE VEHICULOS COMO STRING

dimension_str = lineas[3]
capacidad_str = lineas[5]
vehiculos_str = lineas[0]

# CAMBIANDO EL TIPO DE STRING A INTEGER

instancia = lineas[0]

capacidad = int((capacidad_str[10:]))

nodos = int(dimension_str[12:])

vehiculos = int(vehiculos_str[14:])

clientes = nodos - 1

print(instancia)
print("La cantidad de vehiculos son de:" , vehiculos)
print("\n")
print("La capacidad de los vehiculos es de : " ,capacidad)
print("\n")
print ("La cantidad de nodos que tiene la instancia es: " , nodos)
print("\n")


extraer_coordenadas = nodos + 7


# OBTENGO LOS DATOS DE LAS COORDENADAS DE LOS NODOS EN UN ARREGLO 


data_coordenadas = lineas[7 : extraer_coordenadas]


# AHORA HAY QUE OBTENER LAS DEMANDAS DE CADA CIUDAD 

extraer_demandas = extraer_coordenadas + 1

data_demandas = lineas[extraer_demandas : extraer_demandas + nodos ]


# SEPARAR LOS DATOS DE EL ARREGLO DE COORDENADAS 

limpieza_coordenadas = []
limpieza_demandas = []


for x in data_coordenadas:
    limpieza_coordenadas.append(x.split())
    
for y in data_demandas:
    limpieza_demandas.append(y.split())
    


#CREACION DEL DATAFRAME Y ALMACENANDO LA DATA DE LIMPIEZA_COORDENADAS

print("Creacion del DATAFRAME de los nodos con sus demandas respectivas")
print("\n")


df = pd.DataFrame({
        "x" : [int(limpieza_coordenadas[x][1]) for x in range(0,nodos)],
        "y" : [int(limpieza_coordenadas[x][2]) for x in range(0,nodos)],
        "demanda" : [int(limpieza_demandas[x][1]) for x in range(0,nodos)]
})
    

print(df)    
print("\n")
    
    
# Generando los arcos o los caminos que se pueden recorrer 

print("DATAFRAME de los nodos con su distancia euclidiana")
print("\n")
df_distancias = pd.DataFrame({
    
        "nodos" : [(i,j) for i in range(0,nodos) for j in range(0,nodos) if i < j], # ANTES i != j 1
        "distancia" : [np.hypot(int(limpieza_coordenadas[i][1]) - int(limpieza_coordenadas[j][1]) ,  int(limpieza_coordenadas[i][2]) -  int(limpieza_coordenadas[i][2]) ) for i in range(0, nodos) for j in range(0,nodos) if i < j] # i != j 
      
})

print(df_distancias)
print("\n")


# In[ ]:


# CLUSTERING DE LA DATA 

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


k = vehiculos

demanda = df['demanda']

centroide = {
    
    i+1: [np.random.randint(0,nodos) , np.random.randint(0,)]
    for i in range(k)
    
}

x = []
for i in range(0,nodos):
    x.append(i)


fig = plt.figure(figsize=(15,10))
plt.scatter(df['x'] , df['y'] , color='k')
colmap = {1 : 'red' , 2 : 'blue' , 3: 'green' , 4 : 'purple' , 5 : 'brown' , 6 : 'pink' , 7 : 'indigo' , 8 : 'yellow' , 9 : 'cyan' , 10 : 'orange' }

for i in centroide.keys():
    plt.scatter(*centroide[i] , color=colmap[i])
    
plt.xlim(0,150)
plt.ylim(0,150)
plt.show()




# In[228]:


def asignar_centroide(df , centroide):
    for i in centroide.keys():
        df['distancia_desde_{}'.format(i)] = (
            
           # np.hypot(df['x'] - centroide[i][0] , df['y'] - centroide[i][1])
            np.sqrt( (df['x'] - centroide[i][0])**2 + (df['y'] - centroide[i][1])**2 )
        )
                
    distancia_centroide = ['distancia_desde_{}'.format(i) for i in centroide.keys()]
    df['cercania'] = df.loc[: , distancia_centroide].idxmin(axis=1)
    df['cercania'] = df['cercania'].map(lambda x : int(x.lstrip('distancia_desde_')))
    df['color'] = df['cercania'].map(lambda x : colmap[x])    
    return df


df = asignar_centroide(df , centroide)
print(df)
print("\n")
print("\n")



print("AHORA GRAFICANDO LOS PUNTOS RELACIONADOS (CERCANIA) CON EL CENTROIDE ACTUAL")
fig = plt.figure(figsize=(15,10))
plt.scatter(df['x'],df['y'],color = df['color'] , alpha=0.5 ,  edgecolor ='k')
for i in centroide.keys():
    plt.scatter(*centroide[i] , color = colmap[i])
    
plt.xlim(0,150)
plt.ylim(0,150)
plt.show()


        


# In[ ]:


# CAMBIANDO EL CENTROIDE 

import copy

centroide_anterior = copy.deepcopy(centroide)

def update(k):
    for i in centroide.keys():
        centroide[i][0]  = np.mean(df[df['cercania'] == i]['x'])
        centroide[i][1]  = np.mean(df[df['cercania'] == i]['demanda'])

    return k 
    
centroide = update(centroide)

fig = plt.figure(figsize=(15,10))
ax = plt.axes()
plt.scatter(df['x'] , df['y'] , color=df['color'] , alpha=0.5 , edgecolor='k')
for i in centroide.keys():
    plt.scatter(*centroide[i] ,color = colmap[i])
plt.xlim(0,150)
plt.ylim(0,150)

for i in centroide.keys():
    old_x = centroide_anterior[i][0]
    old_y = centroide_anterior[i][1]
    dx = (centroide[i][0] - centroide_anterior[i][0]) * 0.75
    dy = (centroide[i][1] - centroide_anterior[i][1]) * 0.75
    ax.arrow(old_x , old_y , dx , dy , head_width = 2 , head_length=3 , fc=colmap[i], ec=colmap[i])
    
print("GRAFICO DE LOS ANTIGUOS CENTROIDES PARA VER COMO CAMBIAN SU POSICION.")
plt.show()





# In[180]:


# REPETIR SELECCION DE CENTROIDE

df = asignar_centroide(df , centroide)


#RESULTADO DE LA NUEVA ELECCION 

print("GRAFICO DE LA NUEVA SELECCION DE CENTROIDE.")

fig = plt.figure(figsize=(15,10))
plt.scatter(df['x'],df['y'],color = df['color'] , alpha=0.5 ,  edgecolor ='k')
for i in centroide.keys():
    plt.scatter(*centroide[i] , color = colmap[i])


# In[ ]:


#CONTINUA MIENTRAS TODAS LAS ASIGNACIONES NO CAMBIEN MÁS

while True:
    centroide_cercano = df['cercania'].copy(deep=True)
    centroide = update(centroide)
    df = asignar_centroide(df , centroide)
    if centroide_cercano.equals(df['cercania']):
        break

print("EL GRAFICO FINAL LUEGO DE MULTIPLES ITERACCIONES")
        
fig = plt.figure(figsize=(15,10))
plt.scatter(df['x'],df['y'],color = df['color'] , alpha=0.5 ,  edgecolor ='k')
for i in centroide.keys():
    plt.scatter(*centroide[i] , color = colmap[i])   


# In[226]:


#MOSTAR LOS CLUSTERS A TRABAJAR 


#colmap = colmap = {1 : 'red' , 2 : 'blue' , 3: 'green' , 4 : 'purple' , 5 : 'brown' , 6 : 'pink' , 7 : 'gray' , 8 : 'olive' , 9 : 'cyan' , 10 : 'orange'}


cluster_rojo = df[df['color'] == "red"]

cluster_azul = df[df['color'] == "blue"]

cluster_verde = df[df['color'] == "green"]

cluster_morado = df[df['color'] == "purple"]

cluster_cafe = df[df['color'] == "brown"]

cluster_rosado = df[df['color'] == "pink"]

cluster_indigo = df[df['color'] == "indigo"]

cluster_amarillo = df[df['color'] == "yellow"]

cluster_celeste = df[df['color'] == "cyan"]

cluster_naranja = df[df['color'] == "orange"]

print("N°1: Agrupacion de rojos")

cluster_rojo


# In[178]:


print("N°2: Agrupacion de azules")

cluster_azul


# In[179]:


print("N°3: Agrupacion de verdes")

cluster_verde


# In[131]:


print("N°4: Agrupacion de morados")

cluster_morado


# In[132]:


print("N°5: Agrupacion de cafe")

cluster_cafe


# In[133]:


print("N°6: Agrupacion de rosados")

cluster_rosado


# In[134]:


print("N°7 :Agrupacion de celeste")

cluster_celeste


# In[135]:


print("N°8 Agrupacion de amarillo")

cluster_amarillo


# In[136]:


print("N°9 Agrupacion de naranjas")

cluster_naranja


# In[138]:


print("N°10: Agrupacion de grises")

cluster_indigo


# In[163]:



import matplotlib.pyplot as plt

import sklearn
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import scale

import sklearn.metrics as sm
from sklearn import datasets
from sklearn.metrics import confusion_matrix , classification_report







# In[164]:


get_ipython().run_line_magic('matplotlib', 'inline')
rcParams['figure.figsize'] = 7, 4


# In[ ]:




