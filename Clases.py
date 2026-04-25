#Grupo 1- Informatica II.
#Integrantes:
# -Valentina Monterroza Salazar.
# -Miguel Angel Vásquez Arenas.
# Parcial II.

import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

class Procesador_SIATA():
    def __init__(self, ruta_archivo):
        self.df = pd.read_csv(ruta_archivo)
        self.preprocesar_fechas()