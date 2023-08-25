import tkinter as tk
from tkinter import ttk
from modules import database_module
from datetime import datetime

class GUI:
    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%d-%m-%Y')
    hora = fecha_actual.strftime('%H:%M')

    def __init__(self,root):
        self.root = root
        self.root.title('Registro declaraciones de salud')
        self.database = database_module.Database()
        #Primer bloque: marco informativo
            #Frame
        self.frame_contador = tk.LabelFrame(self.root, text='Información',font=('Courier',16))
        self.frame_contador.pack(anchor='nw', fill='x',pady=10)
            #txt
        self.label_texto = tk.Label(self.frame_contador,text="Declaraciones de salud", font=('Courier',20))
        self.label_texto.pack(anchor='nw', fill='x')
            #txt_fecha
        self.label_fecha = tk.Label(self.frame_contador,text=f"Fecha: {self.fecha}", font=('Courier',18)) 
        self.label_fecha.pack(anchor='nw', fill='x')
            #propiedad de conteo_diario
        conteo = self.conteoDiario()
            #txt_conteo
        self.label_conteo = tk.Label(self.frame_contador, text=f"Llevas {conteo}",font=('Courier',18))
        self.label_conteo.pack(anchor='nw', fill='x')
        #Segundo bloque: botones
            #frame
        self.frame_bloque_2 = tk.LabelFrame(self.root,text="Has click en la opción que quieres seleccionar:")
        self.frame_bloque_2.pack(anchor='nw',fill='x',pady=10)
            #btn agregar ds
        self.boton_agregar_ds = tk.Button(self.frame_bloque_2, text='Agregar declaración\nde salud', command=self.agregarDs)
        self.boton_agregar_ds.pack(anchor='nw', fill='x')
            #btn actualizar conteo
        self.boton_actualizar = tk.Button(self.frame_bloque_2, text='Actualizar conteo', command=self.actualizar_conteo)
        self.boton_actualizar.pack(anchor='nw', fill='x')
            #btn abrir ventana registros
        self.boton_registros = tk.Button(self.frame_bloque_2, text='Abrir registros', command=self.Crear_ventana_registro)
        self.boton_registros.pack(anchor='nw', fill='x')
            #btn descargar registros
        self.boton_descargar = tk.Button(self.frame_bloque_2, text='Descargar registros', command=self.descargarRegistros)
        self.boton_descargar.pack(anchor='nw', fill='x')
        #Tercer bloque: Respuesta
            #frame
        self.frame_respuesta = tk.LabelFrame(self.root,text='Respuesta:')
        self.frame_respuesta.pack(anchor='nw', fill='x')
            #txt_respuesta
        self.texto_respuesta = tk.Label(self.frame_respuesta,text='Esperando...')
        self.texto_respuesta.pack(anchor='nw', fill='x',pady=10)

    def Crear_ventana_registro(self):
        v_registro = tk.Toplevel(self.root)
        v_registro.title('Registro de declaraciones de salud')

        #Marco de botones
        frame_registro = tk.LabelFrame(v_registro)
        frame_registro.pack(anchor='nw', fill='x')

        #bloque de botones para editar,actualizar y eliminar registros
        boton_actualizar = tk.Button(frame_registro,text="Actualizar registro",command=lambda: self.ActualizarRegistro(mensaje_respuesta))
        boton_actualizar.grid(row=0,column=0)
                               
        boton_eliminar = tk.Button(frame_registro,text="Eliminar registro",command=lambda: self.EliminarRegistro(mensaje_respuesta))
        boton_eliminar.grid(row=0,column=1)

        mensaje_respuesta = tk.Label(frame_registro,text='',fg='red')
        mensaje_respuesta.grid(row=1,column=0)

        #tabla de registros
        self.tree = ttk.Treeview(v_registro, height=10, columns=2)
        self.tree.pack()
        self.tree.heading('#0', text='fecha',anchor='center')
        self.tree.heading('#1', text='hora',anchor='center')

        self.ObtenerRegistros()

    def actualizar_conteo(self):
        conteo = self.conteoDiario()
        self.label_conteo.config(text=f"Llevas {conteo}")
        self.texto_respuesta.config(text='\nSe ha actualizado con éxito el conteo\n')

    def agregarDs(self):
        self.database.agregarDs()
        self.texto_respuesta.config(text='Se agrego con exito.\nRecuerda actualizar el conteo.')
    
    def conteoDiario(self):
        return self.database.conteo_diario()
    
    def descargarRegistros(self):
        self.database.descargar_registros()
        self.texto_respuesta.config(text='Se descargo el registro de declaraciones\nde salud exitosamente.')
    
    def ActualizarRegistro(self, mensaje_respuesta):
        self.ObtenerRegistros()
        mensaje_respuesta.config(text='Se actualizó el registro') 
        
    def ObtenerRegistros(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        db_rows = self.database.Obtener_registros()
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])
    
    def EliminarRegistro(self,mensaje_respuesta):
        mensaje_respuesta.config(text='')
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            mensaje_respuesta.config(text='Selecciona un registro')
            return
        mensaje_respuesta.config(text='')
        fecha = self.tree.item(self.tree.selection())['text']
        hora = self.tree.item(self.tree.selection())['values'][0]
        self.database.Eliminar_registro(fecha,hora)
        mensaje_respuesta.config(text='Registro {} eliminado'.format(fecha)) 
        self.ObtenerRegistros()