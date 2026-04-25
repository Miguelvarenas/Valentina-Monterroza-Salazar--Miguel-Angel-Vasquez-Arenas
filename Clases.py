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
    def __init__(self, con ):
        self.df = pd.read_csv()
        self.preprocesar_fechas()