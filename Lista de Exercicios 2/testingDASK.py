import pandas as pd
import numpy as np
import math as mt
from tqdm import tqdm
import random
import time
import dask.dataframe as dd

def calFit(feromonio, dist, relevFero, relevDist):
    return mt.pow(feromonio, relevFero) * mt.pow(1/dist, relevDist)

def weighted_random_roulette(participantes_torneio):
    max_value = sum(participante[1] for participante in participantes_torneio)
    pick, current = random.uniform(0, max_value), 0
    for participante in participantes_torneio:
        current += participante[1]
        if current > pick:
            return participante[0], participante[2]

def deposFeromonio(city1, city2, distanceTable):
    pathIndex = distanceTable.query("c1 == @city1 and c2 == @city2 or c1 == @city2 and c2 == @city1").index[0]
    distanceTable.at[pathIndex, "fero"] += 1

def evap(distanceTable, evapIndice):
    distanceTable["fero"] = distanceTable["fero"].apply(lambda x: (1-evapIndice) * x)

citiesInfo = dd.read_csv("Luxemburgo.csv", delimiter="\t")
distanceTable = dd.read_csv("LuxemburgoDist.csv", delimiter=",", names=["c1", "c2", "dist"])
numCities = citiesInfo.shape[0]
print(distanceTable)
distanceTable["fero"] = np.ones(len(distanceTable.index))
possibilitiesVector = np.arange(1, numCities + 1)
relevDist, relevFero, evapIndice = 4, 1, .5
generationMax = 50
lastDist = 0
for g in range(generationMax):
    antPathDist = []
    pathList = np.zeros(numCities * numCities, dtype=np.int16).reshape((numCities, numCities))
    for i, antpath in enumerate(pathList): antpath[0] = i + 1
    for d, antpath in enumerate(tqdm(pathList, desc="Geração " + str(g), position=0, leave=True)):
        sumdist = 0
        for i, city in enumerate(antpath):
            if i < numCities - 1:
                possibilities = [city for city in possibilitiesVector if city not in antpath]
                citiesPos = distanceTable.query("c1 == @city or c2 == @city") # General possibilities
                cityPos = citiesPos.query("c1 in @possibilities or c2 in @possibilities") # On point possibilities
                possibilitiesProb = []
                for c in cityPos.to_numpy():
                    if c[0] == city:
                        possibilitiesProb += [[c[1], calFit(c[3], c[2], relevFero, relevDist), c[2]]]
                    elif c[1] == city:
                        possibilitiesProb += [[c[0], calFit(c[3], c[2], relevFero, relevDist), c[2]]]
                antpath[i + 1], dist = np.int16(weighted_random_roulette(possibilitiesProb))
                deposFeromonio(city, antpath[i + 1], distanceTable)
                sumdist += dist
        antPathDist += [[d + 1, sumdist]]
    a_min = min(x[1] for x in antPathDist)
    a_max = max(x[1] for x in antPathDist)
    bestDistMin = [i[0] for i in antPathDist if i[1] == a_min] + [a_min]
    bestDistMax = [i[0] for i in antPathDist if i[1] == a_max] + [a_max]
    print("Melhor: " + str(bestDistMin[-1]) + " Pior: " + str(bestDistMax[-1]))
    print("Diferença: " + str(bestDistMax[-1] - bestDistMin[-1]))
    if 0 < bestDistMax[-1] - bestDistMin[-1] < 1700:
        print(pathList[bestDistMin[0] - 1])
        break
    else: lastDist = bestDistMin[-1]
    evap(distanceTable, evapIndice)

