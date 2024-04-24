import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
from forms.form_master import MasterPanel

class RegistroUsuario:
    
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        
        self.ventana_registro = tk.Toplevel(ventana_principal)
        self.ventana_registro.title('Registro de Usuario')
        self.ventana_registro.geometry('300x300')
        self.ventana_registro.config(bg='#fcfcfc')
        self.ventana_registro.resizable(width=0, height=0)    
        
        self.usuario_label = tk.Label(self.ventana_registro, text="Usuario", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.usuario_label.pack(fill=tk.X, padx=20, pady=5)
        self.usuario_entry = ttk.Entry(self.ventana_registro, font=('Times', 14))
        self.usuario_entry.pack(fill=tk.X, padx=20, pady=5)

        self.contraseña_label = tk.Label(self.ventana_registro, text="Contraseña", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.contraseña_label.pack(fill=tk.X, padx=20, pady=5)
        self.contraseña_entry = ttk.Entry(self.ventana_registro, font=('Times', 14), show="*")
        self.contraseña_entry.pack(fill=tk.X, padx=20, pady=5)

        self.confirmar_contraseña_label = tk.Label(self.ventana_registro, text="Confirmar Contraseña", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        self.confirmar_contraseña_label.pack(fill=tk.X, padx=20, pady=5)
        self.confirmar_contraseña_entry = ttk.Entry(self.ventana_registro, font=('Times', 14), show="*")
        self.confirmar_contraseña_entry.pack(fill=tk.X, padx=20, pady=5)

        self.registrar_button = tk.Button(self.ventana_registro, text="Registrar", font=('Times', 15), bg='#3a7ff6', bd=0, fg="#fff", command=self.registrar_usuario)
        self.registrar_button.pack(fill=tk.X, padx=20, pady=20)
        
    def registrar_usuario(self):
        usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()
        confirmar_contraseña = self.confirmar_contraseña_entry.get()

        if not usuario or not contraseña or not confirmar_contraseña:
            messagebox.showerror(message="Por favor complete todos los campos", title="Error")
            return

        if contraseña != confirmar_contraseña:
            messagebox.showerror(message="Las contraseñas no coinciden", title="Error")
            return

        try:
            with open("usuarios.txt", "r") as file:
                for line in file:
                    existing_user, _ = line.strip().split(",")
                    if existing_user == usuario:
                        messagebox.showerror(message="El usuario ya existe", title="Error")
                        return
                        
            with open("usuarios.txt", "a") as file:
                file.write(f"{usuario},{contraseña}\n")
            messagebox.showinfo(message="Usuario registrado correctamente", title="Registro")
            self.ventana_registro.destroy()
            return
            # Enviar el nombre de usuario a la clase MasterPanel
            MasterPanel(usuario)
        except Exception as e:
            messagebox.showerror(message=f"No se pudo registrar el usuario: {e}", title="Error")

class App:
    
    def verificar(self):
        usu = self.usuario.get()
        password = self.password.get()        
        try:
            with open("usuarios.txt", "r") as file:
                # Lee las líneas del archivo
                for line in file:
                    # Separa la línea en usuario y contraseña
                    user, pwd = line.strip().split(',')
                    # Verifica si el usuario y la contraseña coinciden
                    if usu == user and password == pwd:
                        self.ventana.destroy()
                        # Enviar el nombre de usuario a la clase MasterPanel
                        MasterPanel()
                        return
            # Si no encuentra un usuario válido, muestra un mensaje de error
            messagebox.showerror(message="::::La contraseña no es correcta o El Usuario no Existe::::", title="Mensaje")
        except FileNotFoundError:
            # Maneja el caso en el que el archivo no existe
            messagebox.showerror(message="Servicio no Encontrado, intentalo más tarde", title="Error")
   
                      
    def __init__(self):        
        self.ventana = tk.Tk()                             
        self.ventana.title('Inicio de sesion')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)    
        utl.centrar_ventana(self.ventana,800,500)
        
        logo =utl.leer_imagen("./img/bot1.png", (200, 200))
        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='#3a7ff6')
        frame_logo.pack(side="left",expand=tk.YES,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=logo,bg='#3a7ff6' )
        label.place(x=0,y=0,relwidth=1, relheight=1)
        
        #frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form
        
        #frame_form_top
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion",font=('Times', 30), fg="#666a88",bg='#fcfcfc',pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Times', 14) ,fg="#666a88",bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 14),fg="#666a88",bg='#fcfcfc' , anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20,pady=10)
        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill,text="Iniciar sesión",font=('Times', 15,BOLD),bg='#3a7ff6', bd=0,fg="#fff",command=self.verificar)
        inicio.pack(fill=tk.X, padx=20,pady=10)        
        inicio.bind("<Return>", (lambda event: self.verificar()))
        
        registro = tk.Button(frame_form_fill,text="Registrar Usuario",font=('Times', 15,BOLD),bg='#fff', bd=0,fg="#3a7ff6",command=self.registrar_usuario)
        registro.pack(fill=tk.X, padx=20,pady=10)        
        registro.bind("<Return>", (lambda event: self.registrar_usuario()))
        #end frame_form_fill
        self.ventana.mainloop()
        
    def registrar_usuario(self):
        RegistroUsuario(self.ventana)
        
if __name__ == "__main__":
    App()