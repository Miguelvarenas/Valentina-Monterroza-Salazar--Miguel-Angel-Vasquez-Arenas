#Grupo 1- Informatica II.
#Integrantes:
# -Valentina Monterroza Salazar.
# -Miguel Angel Vásquez Arenas.
# Parcial II.

from Clases_y_Funciones_Validacion_Numérica import (
    ProcesadorSIATA,
    ProcesadorControl_Parqui,
    GestorObjetos
)

def validar_entero(msg):
    while True:
        try:
            return int(input(msg))
        except:
            print("Ingrese un número entero válido.")

def validar_float(msg):
    while True:
        try:
            return float(input(msg))
        except:
            print("Ingrese un número válido.")

def menu_Principal():
    print("\n--------------------------------------")
    print(" SISTEMA DE EXPLORACIÓN NEUROAMBIENTAL ")
    print("--------------------------------------")
    print("1. Cargar archivos CSV SIATA")
    print("2. Procesar archivos CSV")
    print("3. Cargar archivo EEG (.mat)")
    print("4. Procesar archivo EEG")
    print("5. Buscar objeto guardado")
    print("0. Salir")

def menu_csv():
    print("\n--------------- MENÚ CSV ---------------")
    print("1. Mostrar info() y describe()")
    print("2. Graficar columna")
    print("3. Operaciones apply/map/suma")
    print("4. Remuestreo")
    print("0. Volver")

def menu_mat():
    print("\n--------------- MENÚ EEG ---------------")
    print("1. Mostrar llaves")
    print("2. Sumar 3 canales")
    print("3. Promedio y desviación estándar")
    print("0. Volver")

def trabajo_csv(obj):
    while True:
        menu_csv()
        op = validar_entero("Seleccione opción: ")

        if op == 1:
            obj.mostrar_info()

        elif op == 2:
            print("\nColumnas disponibles:")
            cols = obj.df.columns.tolist()
            print(cols)

            while True:
                col = input("Ingrese columna numérica: ")
                if col in cols:
                    obj.graficar_analisis(col)
                    break
                else:
                    print(f"La columna '{col}' no existe. Intente de nuevo.")

        elif op == 3:
            cols = obj.df.columns.tolist()
            print(cols)

            while True:
                ch1 = input("Primera columna: ")
                if ch1 in cols: break
                print(f"La columna '{ch1}' no existe.")
            
            while True:
                c2 = input("Segunda columna: ")
                if c2 in cols: break
                print(f"La columna '{c2}' no existe.")

            obj.operaciones(ch1, c2)

        elif op == 4:
            cols = obj.df.columns.tolist()
            print(cols)

            while True:
                col = input("Columna numérica: ")
                if col in cols:
                    obj.graficar_remuestreo(col)
                    break
                else:
                    print(f"La columna '{col}' no existe.")

        elif op == 0:
            break
        else:
            print("Opción inválida")

def trabajo_mat(obj):
    while True:
        menu_mat()
        op = validar_entero("Seleccione opción: ")

        if op == 1:
            obj.mostrar_llaves()

        elif op == 2:
            while True:
                key = input("Nombre llave matriz: ")
                if key in obj.data_dict: 
                    break
                else:
                    print(f"La llave '{key}' no existe en el archivo.")

            ch1 = validar_entero("Canal 1: ")
            ch2 = validar_entero("Canal 2: ")
            ch3 = validar_entero("Canal 3: ")

            tm1 = validar_float("Tiempo inicial (seg): ")
            tm2 = validar_float("Tiempo final (seg): ")

            obj.suma_Canales2d(key, [ch1, ch2, ch3], tm1, tm2)

        elif op == 3:
            while True:
                key = input("Nombre llave matriz: ")
                if key in obj.data_dict:
                    obj.estadisticas_3d(key)
                    break
                else:
                    print(f"La llave '{key}' no existe.")

        elif op == 0:
            break
        else:
            print("Opción inválida")

def main():
    gestor = GestorObjetos()
    csv_actual = None
    mat_actual = None

    while True:
        menu_Principal()
        opcion = validar_entero("Seleccione opción: ")

        if opcion == 1:
            try:
                csv_actual = ProcesadorSIATA(
                    "CalAir_VA_2019.csv",
                    "CalAir_VA_2020.csv",
                    "CalAir_VA_2021.csv",
                    "CalAir_VA_2022.csv",
                    "CalAir_VA_2023.csv"
                )
                gestor.guardar("csv_siata", csv_actual)
                print("Archivos CSV cargados correctamente.")
            except Exception as e:
                print("Error:", e)

        elif opcion == 2:
            if csv_actual:
                trabajo_csv(csv_actual)
            else:
                print("Primero cargue los archivos CSV.")

        elif opcion == 3:
            ruta = input("Ingrese ruta archivo: ")
            try:
                mat_actual = ProcesadorControl_Parqui(control=ruta, parkinson=ruta)
                                                        
                gestor.guardar("archivo_mat", mat_actual)
                print("Archivo MAT cargado correctamente.")
            except Exception as e:
                print("Error:", e)

        elif opcion == 4:
            if mat_actual:
                trabajo_mat(mat_actual)
            else:
                print("Primero cargue archivo MAT.")

        elif opcion == 5:
            nombre = input("Nombre objeto guardado: ")
            encontrado = gestor.buscar(nombre)
            if encontrado:
                print("Objeto encontrado.")
            else:
                print("No existe.")

        elif opcion == 0:
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()