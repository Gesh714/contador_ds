from tkinter import ttk
from tkinter import *
from datetime import datetime

import sqlite3

fecha_actual = datetime.now()
fecha_ajustada = fecha_actual.strftime('%Y-%m-%d')
hora_ajustada =  fecha_actual.strftime('%H:%M')

class Contador:
    # conexión con la dirección de la propiedad
    db_name = 'database.db'

    def __init__(self,window):
        #iniciadores
        self.wind = window
        self.wind.title('Contador declaraciones de salud')
        #hijo de window
        self.main_frame = ttk.Frame(self.wind, padding=10, width=360, height=240)
        #empaqueta el frame en la raiz
        self.main_frame.pack(padx=20, pady=20, expand=True)
        #
        self.frame = Frame(self.main_frame, bg='#F79DD9')
        self.frame.pack()
        
        #crear marco para viualizar datos 
        self.boton_contar = ttk.Button(self.frame, text="Contar declaraciones de salud", command=self.conteo_diario)
        self.boton_contar.pack(padx=10,pady=10)
        self.contador_diario = Label(self.frame,text="El día de hoy llevas: ", bg='#F79DD9', font=('Calibri',24))
        self.contador_diario.pack(padx=10,pady=10)
        self.texto_contador = Label(self.frame , text="")
        self.texto_contador.config(bg='#F79DD9', font=('Calibri',24))
        self.texto_contador.pack(padx=10,pady=10)
        #crear boton
        self.boton_agregar = ttk.Button(self.frame, text="Agregar declaración de salud", command=self.agregarDs)
        self.boton_agregar.pack(pady=50)

        
    def run_query(self, query, parameters = ()):
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query, parameters)
                conn.commit()
            return result
    
    def agregarDs(self):
        fecha_actual = datetime.now()
        fecha_ajustada = fecha_actual.strftime('%Y-%m-%d')
        hora_ajustada =  fecha_actual.strftime('%H:%M')
        query = 'INSERT INTO Contador VALUES(NULL, ?, ?)'
        parametros = (fecha_ajustada,hora_ajustada)
        self.run_query(query, parametros)

    def conteo_diario(self):
        query = "SELECT COUNT(*) AS conteo_diario FROM Contador WHERE DATE(fecha) = ?"
        fecha_actual = datetime.now()
        fecha_ajustada = fecha_actual.strftime('%Y-%m-%d')
        parametros = (fecha_ajustada,)  # Asegúrate de pasar los parámetros como tupla
        result = self.run_query(query, parametros)
        conteo = result.fetchone()[0] # Obtiene el valor del conteo del resultado
        self.texto_contador['text'] = f"{conteo} declaraciones"


if __name__ == '__main__':
    window = Tk()
    application = Contador(window)
    window.mainloop()
