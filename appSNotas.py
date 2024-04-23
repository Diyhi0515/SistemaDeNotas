import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
import psycopg2

class ConexionBD:
    def __init__(self, dbname, user, password, host):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=5432
        )
        self.cursor = self.conn.cursor()

    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()

    def ejecutar_consulta(self, consulta, parametros=None):
        if parametros:
            self.cursor.execute(consulta, parametros)
        else:
            self.cursor.execute(consulta)
        return self.cursor.fetchall()

    def ejecutar_actualizacion(self, consulta, parametros=None):
        if parametros:
            self.cursor.execute(consulta, parametros)
        else:
            self.cursor.execute(consulta)
        self.conn.commit()




class LoginApp:
    def __init__(self, root, conexion):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x400")
        self.conexion = conexion

        self.usuarios = self.obtener_usuarios()

        self.usuario_seleccionado = tk.StringVar(root)
        self.usuario_seleccionado.set(self.usuarios[0] if self.usuarios else "")

        tk.Label(root, text="Usuario:").pack()
        self.menu_usuario = tk.OptionMenu(root, self.usuario_seleccionado, *self.usuarios)
        self.menu_usuario.pack()

        tk.Label(root, text="Contraseña:").pack()
        self.entry_contrasena = tk.Entry(root, show="*")
        self.entry_contrasena.pack()

        tk.Button(root, text="Iniciar sesión", command=self.iniciar_sesion).pack()

    def obtener_usuarios(self):
        usuarios = self.conexion.ejecutar_consulta("SELECT nombre_user FROM usuario")
        return [usuario[0] for usuario in usuarios]

    def iniciar_sesion(self):
        usuario = self.usuario_seleccionado.get()
        contrasena = self.entry_contrasena.get()

        resultado = self.conexion.ejecutar_consulta("SELECT contrasena FROM usuario WHERE nombre_user = %s", (usuario,))

        if resultado and resultado[0][0] == contrasena:
            messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso")
            self.root.destroy()
            ventana_principal = tk.Tk()
            VentanaPrincipal(ventana_principal, conexion, Estudiante(), Materia(), Nota())
        else:
            messagebox.showerror("Inicio de sesión", "Nombre de usuario o contraseña incorrectos")





class VentanaPrincipal:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota):
        self.root = root
        self.root.title("Ventana Principal")
        self.root.geometry("500x600")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota

        tk.Button(root, text="Registrar Estudiante Y sus Notas", command=self.registrar_estudiante).pack(pady=10)
        tk.Button(root, text="Ver Estudiantes Registrados", command=self.ver_estudiantes_Registrados).pack(pady=10)
        tk.Button(root, text="Ver Materias de Estudiante", command=self.ver_materia_de_Estudiante).pack(pady=10)
        tk.Button(root, text="Ver Notas de Estudiante", command=self.ver_notas).pack(pady=10)
        tk.Button(root, text="Ver Promedio", command=self.ver_promedio).pack(pady=10)
        tk.Button(root, text="Actualizar Información de Estudiante", command=self.actualizar_info).pack(pady=10)
        tk.Button(root, text="Eliminar Estudiante", command=self.eliminar_alumno).pack(pady=10)
        tk.Button(root, text="Registrar Materia", command=self.reg_materia).pack(pady=10)
        tk.Button(root, text="Actualizar Información de Materia", command=self.actualizar_mat).pack(pady=10)
        tk.Button(root, text="Eliminar Materia", command=self.eliminar_mat).pack(pady=10)

        tk.Button(root, text="Salir", command=self.root.destroy).pack(pady=10)


    def registrar_estudiante(self):
        self.root.withdraw()
        self.ventana_registro_estudiante = tk.Toplevel(self.root)
        self.app_registro_estudiante = RegistroEstudianteApp(self.ventana_registro_estudiante, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def ver_estudiantes_Registrados(self):
        self.root.withdraw()
        self.ventana_ver_estudiantes = tk.Toplevel(self.root)
        self.app_ver_estudiantes = VerEstudiantesApp(self.ventana_ver_estudiantes, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def ver_materia_de_Estudiante(self):
        self.root.withdraw()
        self.ventana_ver_materias = tk.Toplevel(self.root)
        self.app_ver_materias = Ver_materia_de_Estudiante(self.ventana_ver_materias, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def ver_notas(self):
        self.root.withdraw()
        self.ventana_ver_notas = tk.Toplevel(self.root)
        self.app_ver_notas = VerNotasApp(self.ventana_ver_notas, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def ver_promedio(self):
        self.root.withdraw()
        self.ventana_ver_promedio = tk.Toplevel(self.root)
        self.app_ver_promedio = VerPromedioApp(self.ventana_ver_promedio, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def actualizar_info(self):
        self.root.withdraw()
        self.ventana_actualizar_informacion = tk.Toplevel(self.root)
        self.app_actualizar_informacion = ActualizarInformacionApp(self.ventana_actualizar_informacion, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def eliminar_alumno(self):
        nombre_estudiante = simpledialog.askstring("Eliminar Estudiante", "Ingrese el nombre del estudiante a eliminar")
        if nombre_estudiante:
            nombre, *apellidos = nombre_estudiante.split()
            nombre = ''.join(filter(str.isalpha, nombre))
            apellido_paterno = ''.join(filter(str.isalpha, apellidos[0] if apellidos else ""))
            apellido_materno = ''.join(filter(str.isalpha, apellidos[1] if len(apellidos) > 1 else ""))
            self.clase_estudiante.eliminar_estudiante(self.conexion, nombre, apellido_paterno, apellido_materno)
            messagebox.showinfo("Estudiante eliminado", f"El estudiante {nombre_estudiante} ha sido eliminado")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de estudiante válido")
    def reg_materia(self):
        self.root.withdraw()
        self.ventana_registro_materia = tk.Toplevel(self.root)
        self.app_registro_materia = RegistroMateriaApp(self.ventana_registro_materia, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def actualizar_mat(self):
        self.root.withdraw()
        self.ventana_actualizar_materia = tk.Toplevel(self.root)
        self.app_actualizar_materia = ActualizarMateriaApp(self.ventana_actualizar_materia, self.conexion, self.clase_estudiante, self.clase_materia, self.clase_nota, self.root)

    def eliminar_mat(self):
        nombre_materia = simpledialog.askstring("Eliminar Materia", "Ingrese el nombre de la materia a eliminar")
        if nombre_materia:
            self.clase_materia.eliminar_materia(self.conexion, nombre_materia)
            messagebox.showinfo("Materia eliminada", f"La materia {nombre_materia} ha sido eliminada")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de materia válido")

class RegistroEstudianteApp:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Registro de Estudiante")
        self.root.geometry("600x400")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.estudiante = None

        self.ventana_principal = ventana_principal

        self.mostrar_formulario()

    def mostrar_formulario(self):
        self.frame_formulario = tk.Frame(self.root)
        self.frame_formulario.pack(padx=10, pady=10)

        tk.Label(self.frame_formulario, text="Nombre:").grid(row=0, column=0)
        self.nombre_entry = tk.Entry(self.frame_formulario)
        self.nombre_entry.grid(row=0, column=1)

        tk.Label(self.frame_formulario, text="Apellido Paterno:").grid(row=1, column=0)
        self.apaterno_entry = tk.Entry(self.frame_formulario)
        self.apaterno_entry.grid(row=1, column=1)

        tk.Label(self.frame_formulario, text="Apellido Materno:").grid(row=2, column=0)
        self.amaterno_entry = tk.Entry(self.frame_formulario)
        self.amaterno_entry.grid(row=2, column=1)

        tk.Label(self.frame_formulario, text="Fecha de Nacimiento:").grid(row=3, column=0)
        self.fecha_entry = tk.Entry(self.frame_formulario)
        self.fecha_entry.grid(row=3, column=1)

        tk.Label(self.frame_formulario, text="Carrera:").grid(row=4, column=0)
        self.carrera_var = tk.StringVar()
        carreras = self.clase_estudiante.obtener_carreras(self.conexion)
        self.carrera_optionmenu = tk.OptionMenu(self.frame_formulario, self.carrera_var, *carreras)
        self.carrera_optionmenu.grid(row=4, column=1)


        tk.Button(self.frame_formulario, text="Siguiente", command=self.siguiente).grid(row=5, columnspan=2, pady=10)
        tk.Button(self.frame_formulario, text="Atras", command=self.atras).grid(row=6, columnspan=2, pady=10)

    def siguiente(self):
        nombre = self.nombre_entry.get()
        apaterno = self.apaterno_entry.get()
        amaterno = self.amaterno_entry.get()
        fecha_nacimiento = self.fecha_entry.get()
        carrera = self.carrera_var.get()

        if nombre and apaterno and amaterno and fecha_nacimiento and carrera:
            self.estudiante = {
                'nombre': nombre,
                'apaterno': apaterno,
                'amaterno': amaterno,
                'fecha_nacimiento': fecha_nacimiento,
                'carrera': carrera,
                'materias': {}
            }
            self.frame_formulario.destroy()
            self.mostrar_formulario_notas()
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")

    def mostrar_formulario_notas(self):
        self.frame_notas = tk.Frame(self.root)
        self.frame_notas.pack(padx=10, pady=10)

        tk.Label(self.frame_notas, text="Seleccione la materia:").pack()
        self.materia_var = tk.StringVar()
        materias = self.clase_materia.obtener_materias(self.conexion)
        self.materia_optionmenu = tk.OptionMenu(self.frame_notas, self.materia_var, *materias)
        self.materia_optionmenu.pack()

        tk.Label(self.frame_notas, text="Ingrese las notas:").pack()

        tipos_notas = [
            ("Practicos", "Prácticos"),
            ("Control de Lectura", "Control de Lectura"),
            ("Primer parcial", "Primer Parcial"),
            ("Segundo Parcial", "Segundo Parcial"),
            ("Examen Final", "Examen Final")
        ]

        self.notas_entries = {}
        for tipo_nota, nombre_db in tipos_notas:
            nota_label = tk.Label(self.frame_notas, text=f"{tipo_nota}:")
            nota_label.pack()
            nota_entry = tk.Entry(self.frame_notas)
            nota_entry.pack()
            self.notas_entries[nombre_db] = nota_entry

        tk.Button(self.frame_notas, text="Registrar Nota", command=self.registrar_notas).pack()
        tk.Button(self.frame_notas, text="Siguiente Materia", command=self.agregar_otra_materia).pack()
        tk.Button(self.frame_notas, text="Atras", command=self.atras).pack()
        tk.Button(self.frame_notas, text="Finalizar Registro", command=self.finalizar_registro).pack()

    def obtener_carreras_from(self):
        try:
            carreras = self.clase_estudiante.obtener_carreras(conexion)
            return carreras
        except Exception as e:
            print(f"No se pudieron obtener las carreras: {e}, from")
            return []

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def registrar_notas(self):
        notas = {}
        materia_actual = self.materia_var.get()
        if materia_actual:
            for nombre_db, entry in self.notas_entries.items():
                try:
                    nota = float(entry.get())
                    if nota > 100:
                        messagebox.showerror("Error", "La nota no puede ser mayor a 100")
                        entry.delete(0, tk.END)
                        return
                    notas[nombre_db] = nota
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese un número válido para la nota")
                    entry.delete(0, tk.END)
                    return

            notas_obligatorias = ["Practicos", "Control de Lectura", "Per parcialrim", "Segundo Parcial",
                                  "Examen Final"]
            notas_presentes = all(nota in notas for nota in notas_obligatorias)
            if notas_presentes:
                print("Notas registradas:")
                for nombre_db, nota in notas.items():
                    print(f"{nombre_db}: {nota}")
                self.estudiante['materias'][materia_actual] = notas
                print(self.estudiante['materias'])
                messagebox.showinfo("Notas Registradas", "Las notas han sido registradas correctamente")
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todas las notas obligatorias")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una materia antes de registrar notas")

    def agregar_otra_materia(self):
        materia = self.materia_var.get()
        if materia:
            self.materia_var.set("")
            for entry in self.notas_entries.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una materia antes de continuar")


    def finalizar_registro(self):
        if self.estudiante:
            try:
                for materia, notas in self.estudiante['materias'].items():
                    for tipo_nota, valor_nota in notas.items():
                        if not valor_nota:
                            messagebox.showwarning("Advertencia",
                                                   "Por favor, complete todas las notas antes de finalizar el registro")
                            return

                estudiante = Estudiante()
                estudiante.registrar_estudiante(
                    self.conexion,
                    self.estudiante['nombre'],
                    self.estudiante['apaterno'],
                    self.estudiante['amaterno'],
                    self.estudiante['fecha_nacimiento'],
                    self.estudiante['carrera'],
                    self.estudiante['materias']
                )

                self.root.destroy()
                self.ventana_principal.deiconify()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el estudiante: {e}")
        else:
            messagebox.showerror("Error", "No se ha registrado al estudiante")

class VerEstudiantesApp:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Ver Estudiantes Registrados")
        self.root.geometry("600x600")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.ventana_principal = ventana_principal

        self.mostrar_estudiantes()



        tk.Button(self.root, text="Atras", command=self.atras).pack(pady=10)

    def mostrar_estudiantes(self):
        self.frame_estudiantes = tk.Frame(self.root)
        self.frame_estudiantes.pack(padx=10, pady=10)

        tk.Label(self.frame_estudiantes, text="Estudiantes Registrados").pack()

        self.lista_estudiantes = ttk.Treeview(self.frame_estudiantes, columns=("Nombre", "Apellido Paterno", "Apellido Materno", "Fecha de Nacimiento", "Carrera"))
        self.lista_estudiantes.heading("#0", text="ID")
        self.lista_estudiantes.heading("Nombre", text="Nombre")
        self.lista_estudiantes.heading("Apellido Paterno", text="Apellido Paterno")
        self.lista_estudiantes.heading("Apellido Materno", text="Apellido Materno")
        self.lista_estudiantes.heading("Fecha de Nacimiento", text="Fecha de Nacimiento")
        self.lista_estudiantes.heading("Carrera", text="Carrera")

        self.lista_estudiantes.column("#0", width=50)
        self.lista_estudiantes.column("Nombre", anchor=tk.W, width=100)
        self.lista_estudiantes.column("Apellido Paterno", anchor=tk.W, width=100)
        self.lista_estudiantes.column("Apellido Materno", anchor=tk.W, width=100)
        self.lista_estudiantes.column("Fecha de Nacimiento", anchor=tk.W, width=100)
        self.lista_estudiantes.column("Carrera", anchor=tk.W, width=200)

        self.lista_estudiantes.pack()

        self.cargar_estudiantes()

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def cargar_estudiantes(self):
        try:
            estudiantes = self.clase_estudiante.ver_lista_estudiantes_con_carrera(self.conexion)
            for estudiante in estudiantes:
                self.lista_estudiantes.insert("", "end", text=estudiante[0], values=(estudiante[1], estudiante[2], estudiante[3], estudiante[4], estudiante[5]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los estudiantes: {e}")

class Ver_materia_de_Estudiante:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Ver Materias de Estudiante")
        self.root.geometry("600x600")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.ventana_principal = ventana_principal

        self.mostrar_materias()


        tk.Button(self.root, text="Atras", command=self.atras).pack(pady=10)

    def mostrar_materias(self):
        self.frame_materias = tk.Frame(self.root)
        self.frame_materias.pack(padx=10, pady=10)

        tk.Label(self.frame_materias, text="Seleccione un Estudiante:").pack()
        nombres_estudiantes = self.clase_estudiante.obtener_nombres_completos_estudiantes(self.conexion)
        self.combo_estudiantes = ttk.Combobox(self.frame_materias, values=nombres_estudiantes)
        self.combo_estudiantes.pack(pady=5)
        self.combo_estudiantes.bind("<<ComboboxSelected>>", self.cargar_materias)

        tk.Label(self.frame_materias, text="Materias de Estudiante").pack()

        self.lista_materias = ttk.Treeview(self.frame_materias, columns=("Materia"), show="headings")
        self.lista_materias.heading("Materia", text="Materia")
        self.lista_materias.pack()

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def cargar_materias(self, event):
        try:
            nombre_estudiante = self.combo_estudiantes.get()
            if nombre_estudiante:
                nombre, *apellidos = nombre_estudiante.split()
                nombre = ''.join(filter(str.isalpha, nombre))
                apellido_paterno = ''.join(filter(str.isalpha, apellidos[0] if apellidos else ""))
                apellido_materno = ''.join(filter(str.isalpha, apellidos[1] if len(apellidos) > 1 else ""))
                materias = self.clase_estudiante.materias_de_estudiante(self.conexion, nombre, apellido_paterno,
                                                                        apellido_materno)
                self.lista_materias.delete(*self.lista_materias.get_children())
                for materia in materias:
                    self.lista_materias.insert("", "end", values=(materia[0],))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las materias: {e}")

class VerNotasApp:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Ver Notas de Estudiante")
        self.root.geometry("600x600")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.ventana_principal = ventana_principal

        self.mostrar_notas()

        tk.Button(self.root, text="Atras", command=self.atras).pack(pady=10)

    def mostrar_notas(self):
        self.frame_notas = tk.Frame(self.root)
        self.frame_notas.pack(padx=10, pady=10)

        tk.Label(self.frame_notas, text="Seleccione un Estudiante:").pack()
        nombres_estudiantes = self.clase_estudiante.obtener_nombres_completos_estudiantes(self.conexion)
        self.combo_estudiantes = ttk.Combobox(self.frame_notas, values=nombres_estudiantes)
        self.combo_estudiantes.pack(pady=5)

        def cargar_materias(event):
            nombre_estudiante = self.combo_estudiantes.get()
            if nombre_estudiante:
                nombre, *apellidos = nombre_estudiante.split()
                nombre = ''.join(filter(str.isalpha, nombre))
                apellido_paterno = ''.join(filter(str.isalpha, apellidos[0] if apellidos else ""))
                apellido_materno = ''.join(filter(str.isalpha, apellidos[1] if len(apellidos) > 1 else ""))
                materias = self.clase_estudiante.materias_de_estudiante(self.conexion, nombre, apellido_paterno,
                                                                        apellido_materno)
                materias_clean = [materia[0] for materia in materias]  # Eliminar corchetes
                self.combo_materias['values'] = materias_clean

        self.combo_estudiantes.bind("<<ComboboxSelected>>", cargar_materias)

        tk.Label(self.frame_notas, text="Seleccione Materia:").pack()
        self.combo_materias = ttk.Combobox(self.frame_notas)
        self.combo_materias.pack(pady=5)
        self.combo_materias.bind("<<ComboboxSelected>>", self.cargar_notas)

        tk.Label(self.frame_notas, text="Notas de Estudiante").pack()

        self.lista_notas = ttk.Treeview(self.frame_notas, columns=("Nota", "Tipo de Nota"), show="headings")
        self.lista_notas.heading("Nota", text="Nota")
        self.lista_notas.heading("Tipo de Nota", text="Tipo de Nota")
        self.lista_notas.pack()

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def cargar_notas(self, event):
        try:
            nombre_estudiante = self.combo_estudiantes.get()
            nombre_materia = self.combo_materias.get()
            if nombre_estudiante and nombre_materia:
                nombre, *apellidos = nombre_estudiante.split()
                nombre = ''.join(filter(str.isalpha, nombre))
                apellido_paterno = ''.join(filter(str.isalpha, apellidos[0] if apellidos else ""))
                apellido_materno = ''.join(filter(str.isalpha, apellidos[1] if len(apellidos) > 1 else ""))
                notas = self.clase_materia.obtener_notas(self.conexion, nombre_materia, nombre, apellido_paterno,
                                                         apellido_materno)
                self.lista_notas.delete(*self.lista_notas.get_children())
                for nota, nombre_nota in notas:
                    self.lista_notas.insert("", "end", values=(nota, nombre_nota))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las notas: {e}")

class VerPromedioApp:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Ver Promedio de Materia")
        self.root.geometry("600x600")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.ventana_principal = ventana_principal

        self.mostrar_promedio()

        tk.Button(self.root, text="Atras", command=self.atras).pack(pady=10)

    def mostrar_promedio(self):
        self.frame_promedio = tk.Frame(self.root)
        self.frame_promedio.pack(padx=10, pady=10)

        tk.Label(self.frame_promedio, text="Seleccione un Estudiante:").pack()
        nombres_estudiantes = self.clase_estudiante.obtener_nombres_completos_estudiantes(self.conexion)
        self.combo_estudiantes = ttk.Combobox(self.frame_promedio, values=nombres_estudiantes)
        self.combo_estudiantes.pack(pady=5)

        def cargar_materias(event):
            nombre_estudiante = self.combo_estudiantes.get()
            if nombre_estudiante:
                nombre, *apellidos = nombre_estudiante.split()
                nombre = ''.join(filter(str.isalpha, nombre))
                apellido_paterno = ''.join(filter(str.isalpha, apellidos[0] if apellidos else ""))
                apellido_materno = ''.join(filter(str.isalpha, apellidos[1] if len(apellidos) > 1 else ""))
                materias = self.clase_estudiante.materias_de_estudiante(self.conexion, nombre, apellido_paterno,
                                                                        apellido_materno)
                materias_clean = [materia[0] for materia in materias]
                self.combo_materias['values'] = materias_clean

        self.combo_estudiantes.bind("<<ComboboxSelected>>", cargar_materias)

        tk.Label(self.frame_promedio, text="Seleccione Materia:").pack()
        self.combo_materias = ttk.Combobox(self.frame_promedio)
        self.combo_materias.pack(pady=5)
        self.combo_materias.bind("<<ComboboxSelected>>", self.cargar_promedio)

        self.label_promedio = tk.Label(self.frame_promedio, text="")
        self.label_promedio.pack()

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def cargar_promedio(self, event):
        nombre_estudiante = self.combo_estudiantes.get()
        nombre_materia = self.combo_materias.get()
        if nombre_estudiante and nombre_materia:
            nombre, *apellidos = nombre_estudiante.split()
            nombre = ''.join(filter(str.isalpha, nombre))
            apellido_paterno = ''.join(filter(str.isalpha, apellidos[0] if apellidos else ""))
            apellido_materno = ''.join(filter(str.isalpha, apellidos[1] if len(apellidos) > 1 else ""))
            promedio = self.clase_estudiante.obtener_promedio_materia(self.conexion, nombre, apellido_paterno,
                                                                      apellido_materno, nombre_materia)
            if promedio is not None:
                self.label_promedio.config(text=f"Promedio:\n{promedio[0][0]:.2f}")
            else:
                self.label_promedio.config(text="No se pudo obtener el promedio.")

class ActualizarInformacionApp:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Actualizar Información de Estudiante")
        self.root.geometry("600x400")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.ventana_principal = ventana_principal

        self.mostrar_formulario()

        self.id_estudiante= None

    def mostrar_formulario(self):
        self.frame_formulario = tk.Frame(self.root)
        self.frame_formulario.pack(padx=10, pady=10)

        tk.Label(self.frame_formulario, text="Seleccione un Estudiante:").pack()
        nombres_estudiantes = self.clase_estudiante.obtener_nombres_completos_estudiantes(self.conexion)
        self.combo_estudiantes = ttk.Combobox(self.frame_formulario, values=nombres_estudiantes)
        self.combo_estudiantes.pack(pady=5)
        self.combo_estudiantes.bind("<<ComboboxSelected>>", self.cargar_datos_estudiante)

        tk.Label(self.frame_formulario, text="Nombre:").pack()
        self.nombre_entry = tk.Entry(self.frame_formulario)
        self.nombre_entry.pack()

        tk.Label(self.frame_formulario, text="Apellido Paterno:").pack()
        self.apaterno_entry = tk.Entry(self.frame_formulario)
        self.apaterno_entry.pack()

        tk.Label(self.frame_formulario, text="Apellido Materno:").pack()
        self.amaterno_entry = tk.Entry(self.frame_formulario)
        self.amaterno_entry.pack()

        tk.Label(self.frame_formulario, text="Fecha de Nacimiento:").pack()
        self.fecha_entry = tk.Entry(self.frame_formulario)
        self.fecha_entry.pack()

        tk.Label(self.frame_formulario, text="Carrera:").pack()
        self.carrera_var = tk.StringVar()
        carreras = self.clase_estudiante.obtener_carreras(self.conexion)
        self.carrera_optionmenu = tk.OptionMenu(self.frame_formulario, self.carrera_var, *carreras)
        self.carrera_optionmenu.pack()


        tk.Button(self.frame_formulario, text="Actualizar Información", command=self.actualizar_info).pack()
        tk.Button(self.frame_formulario, text="Atras", command=self.atras).pack()

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def actualizar_info(self):
        nombre = self.nombre_entry.get()
        apaterno = self.apaterno_entry.get()
        amaterno = self.amaterno_entry.get()
        fecha_nacimiento = self.fecha_entry.get()
        carrera = self.carrera_var.get()

        if nombre and apaterno and amaterno and fecha_nacimiento and carrera:
            self.clase_estudiante.actualizar_informacion(
                self.conexion,
                nombre,
                apaterno,
                amaterno,
                fecha_nacimiento,
                carrera,
                self.id_estudiante,
            )
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")

    def cargar_datos_estudiante(self, event):
        nombre_estudiante = self.combo_estudiantes.get()
        if nombre_estudiante:
            nombre, *apellidos = nombre_estudiante.split()
            nombre = ''.join(filter(str.isalpha, nombre))
            apellido_paterno = ''.join(filter(str.isalpha, apellidos[0] if apellidos else ""))
            apellido_materno = ''.join(filter(str.isalpha, apellidos[1] if len(apellidos) > 1 else ""))
            datos_estudiante = self.clase_estudiante.obtener_datos_estudiante(self.conexion, nombre, apellido_paterno,
                                                                              apellido_materno)
            self.id_estudiante = Estudiante().obtener_id_estudiante_por_nombre(self.conexion, nombre, apellido_paterno, apellido_materno)
            if datos_estudiante:
                self.nombre_entry.delete(0, tk.END)
                self.nombre_entry.insert(0, datos_estudiante[0][0])
                self.apaterno_entry.delete(0, tk.END)
                self.apaterno_entry.insert(0, datos_estudiante[0][1])
                self.amaterno_entry.delete(0, tk.END)
                self.amaterno_entry.insert(0, datos_estudiante[0][2])
                self.fecha_entry.delete(0, tk.END)
                self.fecha_entry.insert(0, datos_estudiante[0][3])
                self.carrera_var.set(datos_estudiante[0][4])

class RegistroMateriaApp:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Registro de Materia")
        self.root.geometry("600x400")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.ventana_principal = ventana_principal

        self.mostrar_formulario()

    def mostrar_formulario(self):
        self.frame_formulario = tk.Frame(self.root)
        self.frame_formulario.pack(padx=10, pady=10)

        tk.Label(self.frame_formulario, text="Nombre de la Materia:").grid(row=0, column=0)
        self.nombre_entry = tk.Entry(self.frame_formulario)
        self.nombre_entry.grid(row=0, column=1)

        tk.Label(self.frame_formulario, text="Créditos").grid(row=1, column=0)
        self.creditos_entry = tk.Entry(self.frame_formulario)
        self.creditos_entry.grid(row=1, column=1)

        tk.Button(self.frame_formulario, text="Registrar Materia", command=self.insertar_materia).grid(row=3, columnspan=2, pady=10)
        tk.Button(self.frame_formulario, text="Atras", command=self.atras).grid(row=4, columnspan=2, pady=10)

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def insertar_materia(self):
        nombre = self.nombre_entry.get()
        creditos = self.creditos_entry.get()
        try:
            if nombre and creditos:
                self.clase_materia.insert_materia(self.conexion, nombre, creditos)
                messagebox.showinfo("Éxito", "Materia registrada correctamente")
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la materia: {e}")

class ActualizarMateriaApp:
    def __init__(self, root, conexion, clase_estudiante, clase_materia, clase_nota, ventana_principal):
        self.root = root
        self.root.title("Actualizar Materia")
        self.root.geometry("600x400")
        self.conexion = conexion
        self.clase_estudiante = clase_estudiante
        self.clase_materia = clase_materia
        self.clase_nota = clase_nota
        self.ventana_principal = ventana_principal

        self.mostrar_formulario()

    def mostrar_formulario(self):
        self.frame_formulario = tk.Frame(self.root)
        self.frame_formulario.pack(padx=10, pady=10)

        tk.Label(self.frame_formulario, text="Seleccione una Materia:").pack()
        nombres_materias = self.clase_materia.obtener_materias(self.conexion)
        self.combo_materias = ttk.Combobox(self.frame_formulario, values=nombres_materias)
        self.combo_materias.pack(pady=5)
        self.combo_materias.bind("<<ComboboxSelected>>", self.cargar_datos_materia)

        tk.Label(self.frame_formulario, text="Nombre de la Materia:").pack()
        self.nombre_entry = tk.Entry(self.frame_formulario)
        self.nombre_entry.pack()

        tk.Label(self.frame_formulario, text="Créditos").pack()
        self.creditos_entry = tk.Entry(self.frame_formulario)
        self.creditos_entry.pack()

        tk.Button(self.frame_formulario, text="Actualizar Materia", command=self.actualizar_materia).pack()
        tk.Button(self.frame_formulario, text="Atras", command=self.atras).pack()

    def atras(self):
        self.root.destroy()
        self.ventana_principal.deiconify()

    def cargar_datos_materia(self, event):
        nombre_materia = self.combo_materias.get()
        if nombre_materia:
            datos_materia = self.clase_materia.obtener_datos_materia(self.conexion, nombre_materia)
            if datos_materia:
                self.nombre_entry.delete(0, tk.END)
                self.nombre_entry.insert(0, datos_materia[0][0])
                self.creditos_entry.delete(0, tk.END)
                self.creditos_entry.insert(0, datos_materia[0][1])

    def actualizar_materia(self):
        nombre= self.nombre_entry.get()
        creditos= self.creditos_entry.get()
        nombre_mat=self.combo_materias.get()
        id_materia = self.clase_materia.obtener_cod_materia_por_nombre(self.conexion, nombre_mat)
        try:
            if nombre and creditos:
                self.clase_materia.actualizar_materia(self.conexion,id_materia, nombre, creditos)
                print("Materia actualizada correctamente")
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
        except Exception as e:
            print( f"No se pudo actualizar la materia: {e}")

class Estudiante:
    def __init__(self):
        self.nombre = ""
        self.apaterno = ""
        self.amaterno = ""
        self.fecha_nacimiento = ""
        self.carrera = ""
        self.materias = {}

    def registrar_estudiante(self, conexion, nombre, apaterno, amaterno, fecha_nacimiento, carrera, materias):
        self.nombre = nombre
        self.apaterno = apaterno
        self.amaterno = amaterno
        self.fecha_nacimiento = fecha_nacimiento
        self.carrera = carrera
        self.materias = materias

        #print(self.materias)

        try:
            id_carrera = conexion.ejecutar_consulta("SELECT id_C FROM Carrera WHERE nombre_C=%s", (carrera,))
            id_carrera = id_carrera[0][0] if id_carrera else None

            if id_carrera is not None:
                conexion.ejecutar_actualizacion(
                    "INSERT INTO Estudiante (enombre, eapaterno, eamaterno, fechaNacimiento, ecarrera) "
                    "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (self.nombre, self.apaterno, self.amaterno, self.fecha_nacimiento, id_carrera))
                id_estudiante = self.obtener_id_estudiante_por_nombre(conexion, nombre, apaterno, amaterno)

                codigos_materia = {}
                for materia, notas in self.materias.items():
                    m = Materia()
                    cod_materia = m.obtener_cod_materia_por_nombre(conexion, materia)
                    codigos_materia[materia] = cod_materia
                    nom_materia = codigos_materia[materia]

                for materia, notas in self.materias.items():
                    cod_materia = codigos_materia[materia]
                    conexion.ejecutar_actualizacion("INSERT INTO Notas (id_estudiante, cod_materia) "
                                                    "VALUES (%s, %s)", (id_estudiante, cod_materia))
                    for nombre_nota, nota in notas.items():
                        conexion.ejecutar_actualizacion("INSERT INTO Nota (id_e, cod_mat, nota, nombre_nota) "
                                                        "VALUES (%s, %s, %s, %s)",
                                                        (id_estudiante, cod_materia, nota, nombre_nota))
                        #print("nota registrada "+ nombre_nota)
                print("Estudiante registrado correctamente con sus materias y notas")
            else:
                messagebox.showerror("Error", "La carrera especificada no existe")
        except Exception as e:
            print(f"No se pudo registrar el estudiante: {e}")

    def obtener_id_estudiante_por_nombre(self, conexion, nombre, apellido_paterno, apellido_materno):
        query = "SELECT id FROM Estudiante WHERE enombre = %s and eapaterno = %s and eamaterno = %s"
        parametros = (nombre, apellido_paterno, apellido_materno)
        resultado = conexion.ejecutar_consulta(query, parametros)
        id_estudiante = resultado[0][0] if resultado else None
        return id_estudiante

    def ver_lista_estudiantes(self, conexion):
        try:
            estudiantes = conexion.ejecutar_consulta("SELECT * FROM Estudiante")
            return estudiantes
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de estudiantes: {e}")

    def ver_lista_estudiantes_con_carrera(self, conexion):
        try:
            estudiantes = conexion.ejecutar_consulta(
                "SELECT id, enombre, eapaterno, eamaterno, fechaNacimiento, nombre_C AS carrera "
                "FROM Estudiante e JOIN Carrera c ON e.ecarrera = c.id_C;")
            return estudiantes
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de estudiantes: {e}")

    def actualizar_informacion(self,conexion, nombre, apaterno, amaterno, fecha_nacimiento, carrera, id_e):
        id_c = self.obtener_id_carrera_por_nombre(conexion, carrera)

        print(id_c)
        print(nombre)
        print(apaterno)
        try:
            conexion.ejecutar_actualizacion("UPDATE Estudiante SET enombre=%s, eapaterno=%s, eamaterno=%s, fechaNacimiento=%s, ecarrera=%s WHERE id=%s", (nombre, apaterno, amaterno, fecha_nacimiento, id_c,id_e))
            messagebox.showinfo("Éxito", "Información de estudiante actualizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la información del estudiante: {e}")

    def eliminar_registro(self, conexion, id_estudiante):
        try:

            codigos_materias = conexion.ejecutar_consulta("SELECT cod_materia FROM Notas WHERE id_estudiante=%s",
                                                               (id_estudiante,))
            for codigo_materia in codigos_materias:
                conexion.ejecutar_actualizacion("DELETE FROM Nota WHERE id_e=%s AND cod_mat=%s",
                                                     (id_estudiante, codigo_materia[0]))
            conexion.ejecutar_actualizacion("DELETE FROM Notas WHERE id_estudiante=%s", (id_estudiante,))
            conexion.ejecutar_actualizacion("DELETE FROM Estudiante WHERE id=%s", (id_estudiante,))
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar al estudiante: {e}")

    def validar_carrera(self, conexion, carrera):
        carreras_disponibles = self.obtener_carreras(conexion)
        return carrera in carreras_disponibles

    def obtener_carreras(self, conexion):
        self.conexion = conexion
        try:
            carreras = self.conexion.ejecutar_consulta("SELECT nombre_C FROM Carrera")
            #print(carreras)
            return [carrera[0] for carrera in carreras]

        except Exception as e:
            print(f"No se pudieron obtener las carreras: {e}")
            return []

    def obtener_nombres_completos_estudiantes(self, conexion):
        try:
            query = "SELECT CONCAT(enombre, ' ', eapaterno, ' ', eamaterno) AS nombre_completo FROM Estudiante;"
            nombres_completos = conexion.ejecutar_consulta(query)
            return nombres_completos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener los nombres completos de los estudiantes: {e}")

    def materias_de_estudiante(self, conexion, nombre, apellido_paterno, apellido_materno):
        try:
            print(nombre)
            id_estudiante = self.obtener_id_estudiante_por_nombre(conexion, nombre, apellido_paterno, apellido_materno)
            query = """
            SELECT m.mnombre AS materia
            FROM Notas n
            JOIN Materia m ON n.cod_materia = m.cod_m
            WHERE n.id_estudiante = %s;
            """
            materias = conexion.ejecutar_consulta(query, (id_estudiante,))
            print(id_estudiante)
            print(materias)
            return materias

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener las materias del estudiante: {e}")

    def obtener_promedio_materia(self, conexion, nombre_e, apellido_p, apellido_m, nom_materia):
        try:
            id_estudiante = self.obtener_id_estudiante_por_nombre(conexion, nombre_e, apellido_p, apellido_m)
            codigo_materia = Materia().obtener_cod_materia_por_nombre(conexion, nom_materia)

            consulta = """
                SELECT AVG(nota) AS promedio
                FROM Nota
                WHERE id_e = %s AND cod_mat = %s;
            """

            promedio = conexion.ejecutar_consulta(consulta, (id_estudiante, codigo_materia))
            print(promedio)
            return promedio

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error al obtener el promedio:", error)
            return None
    def obtener_datos_estudiante(self, conexion, nombre, apellido_paterno, apellido_materno):
        try:
            query = """
            SELECT enombre, eapaterno, eamaterno, fechaNacimiento, ecarrera
            FROM Estudiante
            WHERE enombre = %s AND eapaterno = %s AND eamaterno = %s;
            """
            datos_estudiante = conexion.ejecutar_consulta(query, (nombre, apellido_paterno, apellido_materno))
            return datos_estudiante
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener los datos del estudiante: {e}")
            return None
    def obtener_id_carrera_por_nombre(self, conexion, nombre_carrera):
        try:
            query = """
            SELECT id_C
            FROM Carrera
            WHERE nombre_C = %s;
            """
            resultado = conexion.ejecutar_consulta(query, (nombre_carrera,))
            if resultado:
                return resultado[0][0]
            else:
                return None
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener el ID de la carrera: {e}")
            return None

class Materia:
    def __init__(self):
        self.nombre = None
        self.creditos = None
        self.codigo = ""
        self.estudiantes_inscritos = []

    def insert_materia(self, conexion, nombre, creditos):
        self.nombre = nombre
        self.creditos = creditos
        self.conexion = conexion
        try:
            self.conexion.ejecutar_actualizacion("INSERT INTO Materia (mnombre, creditos) VALUES (%s, %s)", (self.nombre, self.creditos))
            messagebox.showinfo("Éxitor","Materia insertada correctamente.")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo insertar la materia: {e}")


    def obtener_materias(self,conexion):
        self.conexion = conexion
        try:
            materias_disponibles = self.conexion.ejecutar_consulta("SELECT mnombre FROM Materia")
            return [materia[0] for materia in materias_disponibles]

        except Exception as e:
            messagebox.showerror(f"No se pudieron obtener las materias disponibles: {e}")
            return []

    def obtener_estudiantes_inscritos(self, conexion):
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT Estudiante.enombre, Estudiante.eapaterno,Estudiante.eamaterno "
                           "FROM Estudiante I"
                           "NNER JOIN Notas ON Estudiante.id = Notas.id_estudiante WHERE Notas.cod_materia = %s",
                           (self.id_materia,))
            estudiantes = cursor.fetchall()
            for estudiante in estudiantes:
                nombre_completo = " ".join(estudiante)
                self.estudiantes_inscritos.append(nombre_completo)
        except Exception as e:
            messagebox.showerror(f"No se pudieron obtener los estudiantes inscritos en la materia: {e}")

    def obtener_cod_materia_por_nombre(self, conexion, nombre_materia):
        query = "SELECT cod_m FROM Materia WHERE mnombre = %s"
        parametros = (nombre_materia,)
        resultado = conexion.ejecutar_consulta(query, parametros)
        id_materia = resultado[0][0] if resultado else None
        return id_materia

    def obtener_notas(self, conexion, nombre_materia, nombre_estudiante, apellido_paterno, apellido_materno):
        id_estudiante = Estudiante().obtener_id_estudiante_por_nombre(conexion, nombre_estudiante, apellido_paterno, apellido_materno)
        cod_m = self.obtener_cod_materia_por_nombre(conexion, nombre_materia)
        print(id_estudiante, cod_m)
        try:
            query = """
            SELECT nota, nombre_nota
            FROM Nota
            WHERE id_e = %s AND cod_mat = %s;
            """
            notas = conexion.ejecutar_consulta(query, (id_estudiante, cod_m))
            return notas
        except Exception as e:
            raise e

    def actualizar_materia(sel, conexion, cod_materia, nuevo_nombre, nuevos_creditos):
        print(cod_materia, nuevo_nombre, nuevos_creditos)
        try:
            conexion.ejecutar_actualizacion("UPDATE Materia SET mnombre=%s, creditos=%s WHERE cod_m=%s",
                           (nuevo_nombre, nuevos_creditos, cod_materia))
            messagebox.showinfo("Éxito", "Materia actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo actualizar la materia: {e}")

    def eliminar_Materia(self, conexion, nombre_materia):
        cod_materia= self.obtener_cod_materia_por_nombre(conexion, nombre_materia)
        try:
            conexion.ejecutar_actualizacion("DELETE FROM Materia WHERE cod_m=%s", (cod_materia,))
            messagebox.showinfo("Éxito", "Materia eliminada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la materia: {e}")

    def obtener_datos_materia(self, conexion, nombre_materia):
        cod_materia= self.obtener_cod_materia_por_nombre(conexion, nombre_materia)
        try:
            datos_materia = conexion.ejecutar_consulta("SELECT mnombre, creditos FROM Materia WHERE cod_m=%s", (cod_materia,))
            return datos_materia
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la materia: {e}")



class Nota:
    pass



conexion = ConexionBD("Registro_De_Estudiantes", "postgres", "150503", "localhost")
root = tk.Tk()
app = LoginApp(root, conexion)
root.mainloop()
conexion.cerrar_conexion()
