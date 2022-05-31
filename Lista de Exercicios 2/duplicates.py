import pandas as pd
import numpy as np
import math as mt
from tqdm import tqdm
import time

coordenadas = pd.read_csv("OmaDist.csv", delimiter=",", names=["C1", "C2", "DIST"])
duplicates = coordenadas[coordenadas.DIST == 0] # General possibilities
print(coordenadas)
print(duplicates)
