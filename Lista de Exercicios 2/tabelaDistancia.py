import pandas as pd
import numpy as np
import math as mt
from tqdm import tqdm
import time

coordenadas = pd.read_csv("Luxemburgo.csv", delimiter="\t")
coordenadas.drop("ID", axis=1, inplace=True)
coordenadas.drop_duplicates(inplace=True)
coordenadas = coordenadas.to_numpy()
citiesDist = np.array([[.0, .0, .0]])
rowsOut = ((coordenadas.shape[0] * coordenadas.shape[0]) / 2) - coordenadas.shape[0]
print(rowsOut)
with tqdm(total=rowsOut) as barra_progresso:
    for i, city1 in enumerate(coordenadas):
        for j, city2 in enumerate(coordenadas):
            if i < j and i != j:
                barra_progresso.update(1)
                citiesDist = np.append(citiesDist, [[i+1, j+1, mt.dist(city1, city2)]], axis=0)
citiesDist = np.delete(citiesDist, 0, axis=0)
np.savetxt("LuxemburgoDist.csv", citiesDist, fmt=["%d", "%d", "%.2f"], delimiter=",")