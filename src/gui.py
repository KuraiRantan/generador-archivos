import subprocess, os, threading
from generador_documentos import generar_archivos
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk


class Gui:
    # El garvage collector molesta con las imagenes(las elimina), por eso
    # se debe guardar la referencia para que exista en la solución informatica
    temp_image = []
    listado_datos = []
    dinamic_widgets = []

    def __init__(self):
        self.root = Tk()
        # Generar un frame que contendra todos los widgets
        self.main_frame = ttk.Frame(self.root, relief='solid', padding=5)

        # Generar un frame que contendra la info del desarrollador
        self.info_dev_frame = ttk.Frame(self.root)

        self.styl = ttk.Style()


    # Callbacks commands(eventos)
    def obtener_ruta_archivo(self, variable:StringVar, file_types:tuple, type_dialog:str='filename') -> str:
        path:str = None
        if type_dialog == 'filename':
            path = filedialog.askopenfilename(
                filetypes=(
                    file_types,
                )
            )
        elif type_dialog == 'directory':
            path = filedialog.askdirectory()
        variable.set(path if path else 'Seleccione un archivo...')
        return path


    def eliminar_sl_final(self, listado: list) -> list:
        partial1 = listado[:-1]
        partial2 = listado[-1].rstrip('\n')
        partial1.append(partial2)
        return partial1

    def select_datos(self, variable:StringVar, file_types:tuple, type_dialog:str='filename') -> None:
        path = self.obtener_ruta_archivo(variable, file_types, type_dialog)
        if path:
            self.btn_cargar_datos.config(state='normal')
        else:
            for widget in self.dinamic_widgets:
                widget['frame'].destroy()
            self.btn_cargar_datos.config(state='disabled')
            self.dinamic_widgets.clear()

    def cargar_datos(self) -> None:
        with open(self.path_datos_val.get(), 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) > 0 :
               
                for widget in self.dinamic_widgets:
                    widget['frame'].destroy()
                # Recorre los nombres de los campos y genera los respectivos widgets
                self.dinamic_widgets.clear()
                self.listado_datos.clear()
                nombre_campos = self.eliminar_sl_final(lines[0].split(';'))
                container_frame = ttk.Frame(self.root, padding='10', relief='ridge')
                container_frame.anchor('center')
                container_frame.grid(column=1, row=0, ipadx=10)
                for campo in nombre_campos:
                    new_frame = ttk.Frame(container_frame, borderwidth=2, relief="solid")
                    check_frame = ttk.Frame(new_frame)

                    lbl_campo = ttk.Label(new_frame, text=campo, justify="center", anchor='center')
                    
                    bold_val = BooleanVar(value=False)
                    check_bold = ttk.Checkbutton(check_frame, text="bold", variable=bold_val, name='bold_value')

                    italic_val = BooleanVar(value=False)
                    check_italic = ttk.Checkbutton(check_frame, text="italic", variable=italic_val)

                    lbl_campo.grid(column=0, row=0,columnspan=4,padx=50, sticky=(W,E))
                    check_bold.grid(column=0, row=1,sticky=(W, E))
                    check_italic.grid(column=1, row=1,sticky=(W, E))
                    
                    new_frame.grid(columnspan=4, pady=6, sticky=(W, E,))
                    new_frame.grid_columnconfigure(0, weight=1)
                    check_frame.anchor('center')
                    check_frame.grid( sticky=(E,W))



                    self.dinamic_widgets.append({
                        'frame':container_frame,
                        'lbl_campo': lbl_campo,
                        'check_bold': check_bold,
                        'bold_val': bold_val,
                        'check_italic': check_italic,
                        'italic_val': italic_val
                    })
                for campo in lines[1:]:
                    campos = campo.split(';')
                    self.listado_datos.append(self.eliminar_sl_final(campos))

    def generar_resultado(self)-> None:
        if (self.lbl_path_plantilla.cget('text') == 'Selecciona un archivo...' or self.lbl_path_datos.cget('text') == 'Selecciona un archivo...' 
        or self.lbl_path_salida.cget('text') == 'Selecciona un archivo...' or self.entry_formato_inicio.get().strip() == '' or self.entry_fotmato_fin.get().strip() == ''):
            messagebox.showwarning(title='WARNING', message='Todos los datos son obligatorios.')
            return
        self.btn_generar_resultado.config(state='disabled')
        self.progess_generate.grid(column=0, row=13, columnspan=4, pady=10)
        listado_valores = []
        for widget in self.dinamic_widgets:
            listado_valores.append((
                widget['lbl_campo'].cget('text'),
                widget['bold_val'].get(),
                widget['italic_val'].get()
            ))
        
        if len(listado_valores) == 0:
            messagebox.showerror(title='ERROR', message='Debes seleecionar el archivo de datos y dar click al boton "CARGAR DATOS"')
            self.progess_generate.grid_forget()
            self.btn_generar_resultado.config(state='normal')
            return
        
        # Se crea la funcion y se ejecuta en un hilo(thread) separado del principal
        # para que no crashee el programa mientras se realiza el procesamiento de la informacion
        def test_thread() -> None:
            generar_archivos(self.path_plantilla_val.get(), self.path_salida_val.get(), self.entry_formato_inicio.get().strip(), self.entry_fotmato_fin.get().strip(), self.selected_pdf_or_word.get(), listado_valores, self.listado_datos)
            self.progess_generate.grid_forget()
            open_path = messagebox.askyesno(title='SUCCESS', message='Se han generado los datos en la ruta:\n' + self.path_salida_val.get() + '\n¿Desea abrir el explorador de archivos?')
            if open_path:
                subprocess.Popen(fr'{"xdg-open " if os.name == "posix" else "start"} {os.path.normpath(os.path.join(self.path_salida_val.get(), "generated_files"))}', shell=True)
            self.btn_generar_resultado.config(state='normal')
            return
        t1 = threading.Thread(name='hilo_test', target=test_thread)
        t1.start()


    def configure_widgets(self):
        self.root.title('Generador de archivos mediante plantilla')
        self.root.config(padx=10, pady=10)
        self.root.resizable(0, 0)

        self.styl.configure('red.TSeparator', background='red')
        self.styl.configure('blue.TSeparator', background='blue')
        self.styl.configure('green.TSeparator', background='green')
        self.styl.configure('yellow.TSeparator', background='yellow')



        # Widget para seleccionar el archivo plantilla
        self.path_plantilla_val = StringVar(value='Selecciona un archivo...')
        self.lbl_path_plantilla = ttk.Label(self.main_frame, textvariable=self.path_plantilla_val)
        self.btn_seleccionar_plantilla = ttk.Button(self.main_frame, text='SELECCIONAR PLANTILLA',command=lambda: self.obtener_ruta_archivo(self.path_plantilla_val, ("Plantilla word", "*.docx")))

        # Widget para seleccionar el archivo de texto con los datos
        self.path_datos_val = StringVar(value='Selecciona un archivo...')
        self.lbl_path_datos = ttk.Label(self.main_frame, textvariable=self.path_datos_val)
        self.btn_seleccionar_datos = ttk.Button(self.main_frame, text='SELECCIONAR DATOS',command=lambda: self.select_datos(self.path_datos_val, ("Datos texto", "*.txt")))
        self.btn_cargar_datos = ttk.Button(self.main_frame, text='Cargar datos', command=self.cargar_datos, state='disabled')

        # Widget para seleccionar la ruta de salida donde se guardara el resultado
        self.path_salida_val = StringVar(value='Selecciona un archivo...')
        self.lbl_path_salida = ttk.Label(self.main_frame, textvariable=self.path_salida_val)
        self.btn_seleccionar_salida = ttk.Button(self.main_frame, text='SELECCIONAR CARPETA SALIDA',command=lambda: self.obtener_ruta_archivo(self.path_salida_val, ("Folder salida", "*.dir"), 'directory'))


        # Widget para definir el formato del template a reemplazar
        self.lbl_formato_reemplazo = ttk.Label(self.main_frame, text='Formato reemplazo: ')
        self.entry_formato_inicio = ttk.Entry(self.main_frame)
        self.lbl_valor = ttk.Label(self.main_frame, text=' VARIABLE_A_REEMPLAZAR ')
        self.entry_fotmato_fin = ttk.Entry(self.main_frame)

        # Radio pfd or word
        self.selected_pdf_or_word = StringVar(value='Word')
        self.radio_pdf = ttk.Radiobutton(self.main_frame, text='PDF', value='PDF', variable=self.selected_pdf_or_word)
        self.radio_word = ttk.Radiobutton(self.main_frame, text='Word', value='Word', variable=self.selected_pdf_or_word)

        # Widget para generar resultado
        self.btn_generar_resultado = ttk.Button(self.main_frame, text='GENERAR', command=self.generar_resultado)

        # Widget para evidenciar el trabajo de generacion del/los archivo/s
        self.progess_generate = ttk.Progressbar(self.main_frame, mode='indeterminate')
        self.progess_generate.start()

        # Widget que contendra la informacion del desarrollador
        self.lbl_info_dev = ttk.Label(self.info_dev_frame, text='Jorge Camargo - Tecnologo ADSI / jorgecamargo2012902@gmail.com')

    def place_widgets(self):
        # Posicionamiento de widgets en el frame padre
        self.main_frame.grid(column=0, row=0, sticky=(N,S,W,E))

        self.lbl_path_plantilla.grid(column=0, row=0, columnspan=4)
        self.btn_seleccionar_plantilla.grid(column=0, row=1, columnspan=4)

        # Separador
        ttk.Separator(self.main_frame, orient=HORIZONTAL).grid(row=2, column=0, columnspan=4, sticky="EW", pady=10)

        self.lbl_path_datos.grid(column=0, row=3, columnspan=4)
        self.btn_seleccionar_datos.grid(column=0, row=4, columnspan=2)
        self.btn_cargar_datos.grid(column=2, row=4, columnspan=2)

        # Separador
        ttk.Separator(self.main_frame, orient=HORIZONTAL).grid(row=5, column=0, columnspan=4, sticky="EW", pady=10)

        self.lbl_path_salida.grid(column=0, row=6, columnspan=4)
        self.btn_seleccionar_salida.grid(column=0, row=7, columnspan=4)

        # Separador
        ttk.Separator(self.main_frame, orient=HORIZONTAL).grid(row=8, column=0, columnspan=4, sticky="EW", pady=10)

        self.lbl_formato_reemplazo.grid(column=0, row=9)
        self.entry_formato_inicio.grid(column=1, row=9)
        self.lbl_valor.grid(column=2, row=9)
        self.entry_fotmato_fin.grid(column=3, row=9)

        # Separador
        ttk.Separator(self.main_frame, orient=HORIZONTAL).grid(row=10, column=0, columnspan=4, sticky="EW", pady=10)


        self.radio_word.grid(column=0, row=11, columnspan=2)
        self.radio_pdf.grid(column=2, row=11, columnspan=2)

        self.btn_generar_resultado.grid(column=0, row=12, columnspan=4)

        # Separador
        ttk.Separator(self.main_frame, orient=HORIZONTAL,style='yellow.TSeparator').grid(row=14, column=0, columnspan=4, sticky="EW", pady='10 0')
        ttk.Separator(self.main_frame, orient=HORIZONTAL,style='yellow.TSeparator').grid(row=15, column=0, columnspan=4, sticky="EW", pady=0)
        ttk.Separator(self.main_frame, orient=HORIZONTAL,style='blue.TSeparator').grid(row=16, column=0, columnspan=4, sticky="EW", pady=0)
        ttk.Separator(self.main_frame, orient=HORIZONTAL,style='red.TSeparator').grid(row=17, column=0, columnspan=4, sticky="EW", pady=0)

        # Info dev
        self.info_dev_frame.grid(columnspan=2)
        self.info_dev_frame.anchor('center')
        self.lbl_info_dev.grid(column=0, row=0, sticky='EW', pady='10 5')


    def start(self):
        # Lanzamiento de la app
        self.configure_widgets()
        self.place_widgets()
        self.root.mainloop()