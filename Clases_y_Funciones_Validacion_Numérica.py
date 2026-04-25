#Grupo 1- Informatica II.
#Integrantes:
# -Valentina Monterroza Salazar.
# -Miguel Angel Vásquez Arenas.
# Parcial II.

import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

class ProcesadorSIATA:
    def __init__(self, CalAir_VA_2019, CalAir_VA_2020, CalAir_VA_2021, CalAir_VA_2022, CalAir_VA_2023):
        self.df = pd.concat([pd.read_csv(f) for f in [CalAir_VA_2019, CalAir_VA_2020, CalAir_VA_2021, CalAir_VA_2022, CalAir_VA_2023]], ignore_index=True)
        self.preprocesar_fechas()

    def preprocesar_fechas(self):
        col_fecha = next((c for c in self.df.columns if 'fecha' in c.lower() or 'time' in c.lower()), None)
        if col_fecha:
            self.df[col_fecha] = pd.to_datetime(self.df[col_fecha])
            self.df.set_index(col_fecha, inplace=True)
            self.df.sort_index(inplace=True)
        else:
            print("Error: No se detectó columna de fecha para el índice.")

    def mostrar_info(self):
        print("\n--- INFO DEL ARCHIVO ---")
        self.df.info()
        print("\n--- DESCRIPCIÓN ESTADÍSTICA ---")
        print(self.df.describe(include='all'))

    def graficar_analisis(self, columna):
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        self.df[columna].plot(ax=axes[0], title=f"Línea: {columna}", color='teal')
        self.df.boxplot(column=columna, ax=axes[1])
        axes[1].set_title(f"Cajas: {columna}")
        self.df[columna].hist(ax=axes[2], color='skyblue', edgecolor='black')
        axes[2].set_title(f"Histograma: {columna}")
        
        plt.tight_layout()
        nombre_img = f"analisis_{columna}.png"
        plt.savefig(nombre_img)
        print(f"Gráfico guardado como: {nombre_img}")
        plt.show()

    def graficar_remuestreo(self, columna):
        
        diario = self.df[columna].resample('D').mean()
        mensual = self.df[columna].resample('ME').mean()
        trimestral = self.df[columna].resample('QE').mean()

        plt.figure(figsize=(12, 6))
        plt.plot(diario, label='Diario (Promedio)', alpha=0.5)
        plt.plot(mensual, label='Mensual', linewidth=2)
        plt.plot(trimestral, label='Trimestral', linewidth=3, marker='o')
        
        plt.title(f"Remuestreo Temporal de {columna}")
        plt.ylabel("Valor")
        plt.xlabel("Tiempo")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"remuestreo_{columna}.png")
        plt.show()

    def operaciones(self, col1, col2):

        max_val = self.df[col1].max()
        self.df[f'{col1}_norm'] = self.df[col1].map(lambda x: x / max_val if max_val != 0 else 0)
        
        umbral = self.df[col2].mean()
        self.df[f'{col2}_nivel'] = self.df[col2].apply(lambda x: 'Alto' if x > umbral else 'Bajo')
        
        self.df['suma_columnas'] = self.df[col1] + self.df[col2]
        
        print(f"Nuevas columnas creadas: {col1}_norm, {col2}_nivel, suma_columnas")
        print(self.df[[col1, col2, 'suma_columnas']].head())

class ProcesadorControl_Parqui:
    def __init__(self, control=None, parkinson=None):
        self.control_path = control
        self.parkinson_path = parkinson
        self.data_dict = {}
        
        if self.control_path:
            self.data_dict.update(sio.loadmat(self.control_path)) 
        if self.parkinson_path:
            self.data_dict.update(sio.loadmat(self.parkinson_path)) 
        
        self.fs = 1000

    def mostrar_llaves(self):
        llaves = [k for k in self.data_dict.keys() if not k.startswith('__')]
        print(f"Llaves encontradas: {llaves}")
        return llaves

    def suma_Canales2d(self, key_mat, chs, t_min, t_max):
        data = self.data_dict[key_mat]
    
        if data.ndim == 3:
            data = data.reshape(data.shape[0], -1)
        
        idx_ini, idx_fin = int(t_min * self.fs), int(t_max * self.fs)
        tiempo = np.arange(idx_ini, idx_fin) / self.fs
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        suma_total = np.zeros(idx_fin - idx_ini)

        for c in chs:
            señal = data[c, idx_ini:idx_fin]
            ax1.plot(tiempo, señal, label=f"Ch {c}")
            suma_total += señal
            
        ax1.set_title("Canales Individuales")
        ax1.set_ylabel("Microvoltios (uV)")
        ax1.legend()

        ax2.plot(tiempo, suma_total, color='red', label='Suma Resultante')
        ax2.set_title("Suma de Canales Seleccionados")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Microvoltios (uV)")
        ax2.legend()

        plt.tight_layout()
        plt.savefig("eeg_suma_canales.png")
        plt.show()

    def estadisticas_3d(self, key_mat):
        data = self.data_dict[key_mat]
        if data.ndim != 3:
            print("Error: La matriz no es 3D.")
            return
        
        promedio = np.mean(data, axis=0).flatten()
        desviacion = np.std(data, axis=0).flatten()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
        ax1.stem(promedio[:150])
        ax1.set_title("Promedio (Eje 0)")
        ax1.set_ylabel("uV")
        
        ax2.stem(desviacion[:150])
        ax2.set_title("Desviación Estándar (Eje 0)")
        ax2.set_ylabel("uV")
        
        plt.show()

class GestorObjetos:
    def __init__(self):
        self.almacenar = {}

    def guardar(self, nombre, obj):
        self.almacenar[nombre] = obj

    def buscar(self, nombre):
        return self.almacenar.get(nombre)