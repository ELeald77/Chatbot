import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
import util.generic as utl
import webbrowser
import subprocess
import random
import json
import time

def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))

class MasterPanel:
    
    def __init__(self):
        self.use_google = 0
        self.ventana = tk.Tk()                           
        self.ventana.title('Asistente Principal')
        self.ventana.config(bg='#fcfcfc')

        self.ventana.attributes('-fullscreen', True)  # Establecer la ventana en modo de pantalla completa

        logo = leer_imagen("./img/bot1.png", (400, 400))
        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, padx=10, pady=10, bg='#3a7ff6')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#3a7ff6')
        label.pack(fill=tk.BOTH, expand=tk.YES)

        # frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # Chat Display
        self.chat_display = tk.Text(frame_form, bg='white', fg='black', font=('Arial', 14), wrap=tk.WORD)
        self.chat_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        mensaje_bienvenida = "Hola de nuevo, ¿Cómo puedo ayudarte hoy?\n"
        for i, letra in enumerate(mensaje_bienvenida):
            self.chat_display.insert(tk.INSERT, letra)
            self.ventana.update()  # Actualiza la ventana para mostrar la nueva letra
            time.sleep(0.05)  # Espera 0.05 segundos antes de mostrar la siguiente letra
        self.chat_display.config(state=tk.DISABLED)

        # Message Entry
        self.message_entry = tk.Text(frame_form, bg='#f0f0f0', fg='black', font=('Arial', 16), relief=tk.FLAT, height=3)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=(10,10))
        self.message_entry.bind("<Return>", self.send_message)

        # Send Button
        send_icon = leer_imagen("./img/envio.png", (50, 70))  # Ajusta el tamaño del ícono según tus necesidades
        send_button = tk.Button(frame_form, command=self.send_message, bg='#007bff', fg='white', font=('Arial', 12), relief=tk.FLAT, width=send_icon.width() + 10, height=send_icon.height() + 10, compound=tk.LEFT, image=send_icon)
        send_button.place(relx=1, rely=1, x=-10, y=-10, anchor="se")


        salir_icon = leer_imagen("./img/salir.png", (50, 50))  # Ajusta el tamaño del ícono según tus necesidades
        salir_button = tk.Button(frame_form, command=self.ventana.destroy, bg='#FFF', fg='white', font=('Arial', 12), relief=tk.FLAT, width=salir_icon.width() + 20, height=salir_icon.height() + 10, compound=tk.LEFT, image=salir_icon)
        salir_button.place(relx=1, x=-10, y=10, anchor="ne")


        self.ventana.mainloop()

    
    def send_message(self, event=None):
        message = self.message_entry.get("1.0", tk.END).strip()
         
        if message:
            self.message_entry.delete("1.0", tk.END)
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "Tú: " + message + "\n", "right")
            
            if "google" in message.lower() or "Google" in message.lower():
                self.use_google = 1
                self.chat_display.insert(tk.END, "Asistente: Okey, ahora todas las consultas se harán en Google.\n")
            elif "youtube" in message.lower() or "Youtube" in message.lower():
                self.use_google = 2
                self.chat_display.insert(tk.END, "Asistente: Okey, ahora todas las consultas se harán en YouTube.\n")
            elif "wikipedia" in message.lower() or "Wikipedia" in message.lower():
                self.use_google = 3
                self.chat_display.insert(tk.END, "Asistente: Okey, ahora todas las consultas se harán en Wikipedia.\n")
            elif "apps" in message.lower() or "Aplicaciones" in message.lower():
                self.use_google = 4
                self.chat_display.insert(tk.END, "Asistente: Okey, ahora se abrirán las aplicaciones que digas.\n")
            elif "chistes" in message.lower() or "cuentame un chiste" in message.lower():
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.delete('1.0', tk.END)
                self.chat_display.insert(tk.END, "Asistente: Preparate para reirte fuerte JAJAJAJA\n")
                self.use_google = 0
                self.ver_chiste(message)
            elif "otro" in message.lower():
                self.ver_chiste(message)
            elif any(word in message.lower() for word in ["hola", "buenos dias", "buenas tardes", "buenas noches"]):
                self.chat_display.insert(tk.END, "Asistente: ¡Hola! ¿En qué puedo ayudarte hoy?\n")
            elif any(word in message.lower() for word in ["como estas", "como te encuentras", "como va todo"]):
                self.chat_display.insert(tk.END, "Asistente: Estoy bien, gracias por preguntar. ¿Y tú?\n")
            elif any(word in message.lower() for word in ["cómo funciona esto", "qué puedo hacer aquí"]):
                self.chat_display.insert(tk.END, "Asistente: Puedes pedirme que busque en Google, YouTube o Wikipedia, contarte un chiste o jugar adivinar el número. ¡Pruébalo!\n")
            elif any(word in message.lower() for word in ["gracias", "agradecido", "te lo agradezco"]):
                self.chat_display.insert(tk.END, "Asistente: De nada, estoy aquí para ayudarte.\n")
            elif any(word in message.lower() for word in ["adiós", "hasta luego", "nos vemos"]):
                self.chat_display.insert(tk.END, "Asistente: ¡Hasta luego! Que tengas un buen día.\n")
            elif any(word in message.lower() for word in ["qué hora es", "hora actual", "hora del sistema"]):
                self.chat_display.insert(tk.END, "Asistente: Lo siento, no puedo darte la hora en este momento.\n")
            elif any(word in message.lower() for word in ["qué tiempo hace", "clima actual", "pronóstico del tiempo"]):
                self.chat_display.insert(tk.END, "Asistente: Lamentablemente, no puedo proporcionar información sobre el clima en este momento.\n")
            elif any(word in message.lower() for word in ["cómo te llamas", "cuál es tu nombre", "quién eres"]):
                self.chat_display.insert(tk.END, "Asistente: Soy un asistente virtual creado para ayudarte. Aún no tengo nombre, ¿tienes alguna sugerencia?\n")
            elif any(word in message.lower() for word in ["cuál es tu función", "qué puedes hacer"]):
                self.chat_display.insert(tk.END, "Asistente: Mi función es asistirte en tus tareas diarias y proporcionarte información útil. Puedo realizar búsquedas en línea, contar chistes, entre otras cosas.\n")
            elif any(word in message.lower() for word in ["dónde estás", "cuál es tu ubicación", "en qué lugar estás"]):
                self.chat_display.insert(tk.END, "Asistente: Soy un asistente virtual, no tengo una ubicación física.\n")
            elif any(word in message.lower() for word in ["me puedes ayudar", "necesito ayuda", "ayúdame por favor"]):
                self.chat_display.insert(tk.END, "Asistente: Por supuesto, ¿en qué puedo ayudarte?\n")
            elif any(word in message.lower() for word in ["no entiendo", "no comprendo", "me confunde"]):
                self.chat_display.insert(tk.END, "Asistente: ¿Necesitas ayuda para entender algo en particular?\n")
            
                                
            
            elif self.use_google==1:
                self.search_on_google(message)
            elif self.use_google==2:
                self.search_on_youtube(message)    
            elif self.use_google==3:
                self.search_on_wikipedia(message)  
            elif self.use_google == 4:
                self.search_on_app(message)
            
            
            else:
                self.chat_display.insert(tk.END, "Asistente: No entiendo eso, pero puedes probar escribiendo:\n")
                self.chat_display.insert(tk.END, "- Google\n")
                self.chat_display.insert(tk.END, "- Youtube\n")
                self.chat_display.insert(tk.END, "- Apps\n")
                self.chat_display.insert(tk.END, "- Cuentame un chiste\n")
            
            self.chat_display.config(state=tk.DISABLED)


    
    def search_on_google(self, query):
        self.chat_display.insert(tk.END, "Asistente: Redirigiendo a Google...\n")
        self.chat_display.see(tk.END)
        self.ventana.after(2000, lambda: webbrowser.open(f"https://www.google.com/search?q={query}"))
        
    def search_on_youtube(self, query):
        self.chat_display.insert(tk.END, "Asistente: Redirigiendo a YouTube...\n")
        self.chat_display.see(tk.END)
        self.ventana.after(2000, lambda: webbrowser.open(f"https://www.youtube.com/results?search_query={query}"))
        
    def search_on_wikipedia(self, query):
        self.chat_display.insert(tk.END, "Asistente: Redirigiendo a Wikipedia...\n")
        self.chat_display.see(tk.END)
        self.ventana.after(2000, lambda: webbrowser.open(f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"))

    def search_on_app(self, app_name):
        rutas_ejecutables = {
            "calculadora": r"C:\Windows\System32\calc.exe",
            "explorador": r"C:\Windows\explorer.exe",
            "notepad": r"C:\Windows\System32\notepad.exe",
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
            "power point": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
            "cmd": r"C:\Windows\system32\cmd.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "access": r"C:\Program Files\Microsoft Office\root\Office16\MSACCESS.EXE",
            "publisher": r"C:\Program Files\Microsoft Office\root\Office16\MSPUB.EXE"
        }
        

        app_name = app_name.lower()
        if app_name in rutas_ejecutables:
            subprocess.Popen([rutas_ejecutables[app_name]])
        else:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "No se reconoce la aplicación: {}\n".format(app_name))
            self.chat_display.insert(tk.END, "Asistente: Pero puedes probar escribiendo:\n")
            self.chat_display.insert(tk.END, "- Word\n")
            self.chat_display.insert(tk.END, "- Excel\n")
            self.chat_display.insert(tk.END, "- Chrome\n")
            self.chat_display.insert(tk.END, "- Access\n")
            self.chat_display.config(state=tk.DISABLED)
            

    def load_chistes(self):
        # Carga los chistes desde el JSON
        chistes_json = '''
        {
            "chistes": [
                "¿Qué hace una abeja en el gimnasio?|¡Zum-ba!|¡Jajaja!",
                "¿Cuál es el colmo de un electricista?|Tener mala corriente.|¡Ja, ja, ja!",
                "¿Qué le dice una iguana a su hermana gemela?|Somos iguanitas.|¡Jajajaj!",
                "¿Cuál es el animal más antiguo?|La cebra, ¡porque está en blanco y negro!|¡Hahaha!",
                "¿Por qué el libro de matemáticas está triste?|Porque tiene demasiados problemas.|¡Jajajaja!",
                "¿Cuál es el vino más fuerte?|¡El vino-tinto!|¡Jejeje!",
                "¿Qué es un pez en el agua?|¡Sushi!|¡Jijiji!",
                "¿Qué hace una impresora en el cine?|¡Imprimiendo película!|¡Jajajaja!",
                "¿Cuál es el lápiz más popular?|¡El lápiz de labios!|¡Jajajaj!",
                "¿Qué le dice una iguana a su hermana gemela?|Somos iguanitas.|¡Jajajaja!",
                "¿Qué le dice un jardinero a otro?|Nos vemos cuando podamos|XD",
                "¿Cómo maldice un pollito a otro pollito?|¡Caldito seas!|JAJAJAJA",
                "¿Qué le pasa a Papá Noel cuando pierde un reno?|Sufre de insuficiencia renal|JAJAJAJA",
                "¿Cómo va tu vida amorosa?|Como la Coca-Cola: Primero normal, después light y ahora zero|No es divertido es triste",
                "Doctor, un paciente ciego desea verlo|Digale que no hago milagros|Se paso de lanza jajjaa",
                "Jaimito, si tengo 40 manzanas en una mano y en la otra 50, ¿qué tengo?|Las manos muy grandes|Quien lo manda a comprar bastantes manzanas",
                "¿Cuál es el animal que mas dientes tiene?|El raton Pérez|Puesi que no?",
                "¿Qué árbol es el mas valiente?|La palmera, porque duerme con el coco|Deberia retirarme",
                "Mamá, mamá. Es clase sol el más alto y el que más sabe.|Claro, cariño...eres el profesor|asi hasta yo jajaja"                
            ]
        }
        '''
        chistes_data = json.loads(chistes_json)
        return chistes_data['chistes']

    def ver_chiste(self, message):
        # Obtener un chiste aleatorio
        chistes_data = self.load_chistes()
        chiste = random.choice(chistes_data)

        # Mostrar el chiste y la respuesta juntos
        primera_parte, segunda_parte, carcajadas = chiste.split('|')
        mensaje_completo = f"{primera_parte}\n{segunda_parte}\n{carcajadas}\n"
        self.chat_display.insert(tk.END, mensaje_completo)
