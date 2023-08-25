import pandas as pd
import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        self.db_name = os.path.join(os.path.dirname(__file__), '..', 'database.db')

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def agregarDs(self):
        fecha_actual = datetime.now()
        fecha = fecha_actual.strftime('%d-%m-%Y')
        hora = fecha_actual.strftime('%H:%M')
        query = 'INSERT INTO Contador VALUES(NULL, ?, ?)'
        parametros = (fecha, hora)
        self.run_query(query, parametros)

    def conteo_diario(self):
        fecha_actual = datetime.now()
        fecha = fecha_actual.strftime('%d-%m-%Y')
        query = "SELECT COUNT(*) AS conteo_diario FROM Contador WHERE fecha = ?"
        parametros = (fecha,)
        result = self.run_query(query, parametros)
        conteo = result.fetchone()[0]
        return conteo

    def Obtener_registros(self):
        query = "SELECT * FROM Contador ORDER BY fecha ASC"
        db_rows = self.run_query(query)
        return db_rows

    def descargar_registros(self):
        query = "SELECT * FROM Contador"
        db_connection = sqlite3.connect(self.db_name)
        df = pd.read_sql(query, db_connection)
        download_folder = os.path.expanduser("~")
        download_path = os.path.join(download_folder, "Downloads")
        output_file = os.path.join(download_path, 'registro_ds.xlsx')
        df.to_excel(output_file,index=False, engine='openpyxl', if_exists='replace')

    def Eliminar_registro(self,fecha,hora):
        query = 'DELETE FROM Contador WHERE fecha = ? AND hora = ?'
        db_connection = sqlite3.connect(self.db_name) 
        cursor = db_connection.cursor()
        cursor.execute(query,(fecha,hora))
        db_connection.commit()
