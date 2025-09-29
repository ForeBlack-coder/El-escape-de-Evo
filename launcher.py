import tkinter as tk
from tkinter import ttk
import subprocess
import webbrowser
import os
import sys
import threading
from PIL import Image, ImageTk

def resource_path(relative_path):
    """ Devuelve la ruta absoluta al recurso, funciona en dev y en PyInstaller """
    try:
        base_path = sys._MEIPASS  # cuando se ejecuta empaquetado
    except Exception:
        base_path = os.path.abspath(".")  # cuando se ejecuta en desarrollo
    return os.path.join(base_path, relative_path)


class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("1024x600")
        self.root.resizable(False, False)

        # Cargar imagen de fondo
        self.load_background()

        # Crear canvas principal
        self.canvas = tk.Canvas(root, width=1024, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Mostrar imagen de fondo
        if hasattr(self, 'bg_image'):
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Imagen clickeable en esquina superior izquierda
        self.load_clickable_image()

        # Texto "readme" en esquina inferior izquierda
        self.create_readme_link()

        # Botón de Créditos
        self.create_credits_button()

        # Botón Jugar
        self.create_play_button()

        # Barra de carga
        self.create_progress_bar()

    def load_background(self):
        try:
            bg_path = resource_path("resources/background.jpeg")
            if os.path.exists(bg_path):
                img = Image.open(bg_path)
                img = img.resize((1024, 600), Image.Resampling.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"No se pudo cargar la imagen de fondo: {e}")

    def load_clickable_image(self):
        try:
            img_path = resource_path("resources/player.png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)
                self.logo_btn = tk.Button(
                    self.root,
                    image=self.logo_image,
                    command=self.execute_camacho,
                    bd=0,
                    highlightthickness=0,
                    relief="flat",
                    cursor="hand2"
                )
                self.canvas.create_window(60, 60, window=self.logo_btn)
        except Exception as e:
            print(f"No se pudo cargar la imagen del logo: {e}")
            self.logo_btn = tk.Button(
                self.root,
                text="LOGO",
                command=self.execute_camacho,
                bg="#444",
                fg="white",
                font=("Arial", 12, "bold"),
                cursor="hand2"
            )
            self.canvas.create_window(60, 60, window=self.logo_btn)

    def create_readme_link(self):
        self.readme_label = tk.Label(
            self.root,
            text="readme",
            fg="cyan",
            bg="#222",
            font=("Arial", 14, "underline"),
            cursor="hand2"
        )
        self.readme_label.bind("<Button-1>", lambda e: self.open_readme())
        self.canvas.create_window(60, 565, window=self.readme_label)

    def create_credits_button(self):
        self.credits_btn = tk.Button(
            self.root,
            text="Créditos",
            command=self.show_credits,
            bg="#555",
            fg="white",
            font=("Arial", 14, "bold"),
            width=10,
            height=2,
            cursor="hand2",
            relief="raised",
            bd=3
        )
        self.canvas.create_window(520, 520, window=self.credits_btn)

    def create_play_button(self):
        self.play_btn = tk.Button(
            self.root,
            text="JUGAR",
            command=self.start_game,
            bg="#0003aa",
            fg="white",
            font=("Arial", 16, "bold"),
            width=10,
            height=2,
            cursor="hand2",
            relief="raised",
            bd=3
        )
        self.canvas.create_window(520, 440, window=self.play_btn)

    def create_progress_bar(self):
        style = ttk.Style()
        style.configure("blue.Horizontal.TProgressbar", troughcolor="white",
                        background="blue", thickness=10)

        self.progress = ttk.Progressbar(
            self.root,
            length=300,
            mode='indeterminate',
            style="blue.Horizontal.TProgressbar"
        )
        self.progress_window = self.canvas.create_window(
            520, 350,
            window=self.progress,
            state='hidden'
        )

    def execute_camacho(self):
        """Ejecuta Camacho.py y oculta el launcher hasta que termine"""
        try:
            # Cambiar de .exe a .py
            py_path = resource_path("modules/EasterEgg.py")
            if os.path.exists(py_path):
                self.root.withdraw()
                print("Ejecutando Camacho.py")

                # Ejecutar el archivo Python con el intérprete actual
                process = subprocess.Popen([sys.executable, py_path])

                def wait_and_show():
                    process.wait()
                    self.root.deiconify()
                    print("Camacho.py ha finalizado")

                threading.Thread(target=wait_and_show, daemon=True).start()
            else:
                print(f"Error: No se encontró {py_path}")
                # Intentar con la versión .exe como fallback
                exe_path = resource_path("modules/Camacho.exe")
                if os.path.exists(exe_path):
                    print("Archivo .py no encontrado, intentando con .exe")
                    self.root.withdraw()
                    process = subprocess.Popen([exe_path])
                    
                    def wait_and_show():
                        process.wait()
                        self.root.deiconify()
                    
                    threading.Thread(target=wait_and_show, daemon=True).start()
                else:
                    print("No se encontró ni el archivo .py ni el .exe")
        except Exception as e:
            print(f"Error al ejecutar Camacho: {e}")
            self.root.deiconify()

    def open_readme(self):
        url = "https://github.com/ForeBlack-coder/Juego-de-turtle-simple/blob/0a8cc8171515af592cc46096ba01b9e865f6d199/readme.md"
        webbrowser.open(url)
        print("Abriendo README en el navegador")

    def show_credits(self):
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Créditos")
        credits_window.geometry("600x600")
        credits_window.resizable(False, False)

        credits_text = """
        CRÉDITOS

        Desarrollado por: Jhonatan Mendoza Justiniano & Claude Ai
        Diseño: Jhonatan Mendoza
        Música: Llorando se fue (zampoña)
        Música2: NEW BOLIVIA BAND - Camba que viva el camba

        Agradecimientos especiales:
        - Ing. Jaime Zambrana Chacon (Docente de programación II)
        - Msc. Wilmer Campos Saavedra (Decano de la facultad de ingeniería)
        - Python Software Foundation
        - Claude Sonnet 4.1

        © 2025 Todos los derechos reservados
        """

        label = tk.Label(
            credits_window,
            text=credits_text,
            font=("Arial", 12),
            justify="center",
            bg="#222",
            fg="white"
        )
        label.pack(expand=True, fill="both")

        close_btn = tk.Button(
            credits_window,
            text="Cerrar",
            command=credits_window.destroy,
            bg="#555",
            fg="white",
            font=("Arial", 12, "bold")
        )
        close_btn.pack(pady=10)

    def start_game(self):
        self.canvas.itemconfig(self.progress_window, state='normal')
        self.progress.start(5)
        self.root.after(2000, self.execute_game)

    def execute_game(self):
        """Ejecuta ElEscapeDeEvo.py y oculta el launcher hasta que termine"""
        try:
            # Cambiar de .exe a .py
            py_path = resource_path("modules/ElEscapeDeEvo.py")
            if os.path.exists(py_path):
                self.root.withdraw()
                print("Ejecutando ElEscapeDeEvo.py")

                # Ejecutar el archivo Python con el intérprete actual
                process = subprocess.Popen([sys.executable, py_path])

                def wait_and_show():
                    process.wait()
                    self.progress.stop()
                    self.canvas.itemconfig(self.progress_window, state='hidden')
                    self.root.deiconify()
                    print("ElEscapeDeEvo.py ha finalizado")

                threading.Thread(target=wait_and_show, daemon=True).start()
            else:
                print(f"Error: No se encontró {py_path}")
                # Intentar con la versión .exe como fallback
                exe_path = resource_path("modules/ElEscapeDeEvo.exe")
                if os.path.exists(exe_path):
                    print("Archivo .py no encontrado, intentando con .exe")
                    self.root.withdraw()
                    process = subprocess.Popen([exe_path])
                    
                    def wait_and_show():
                        process.wait()
                        self.progress.stop()
                        self.canvas.itemconfig(self.progress_window, state='hidden')
                        self.root.deiconify()
                    
                    threading.Thread(target=wait_and_show, daemon=True).start()
                else:
                    print("No se encontró ni el archivo .py ni el .exe")
                    self.progress.stop()
                    self.canvas.itemconfig(self.progress_window, state='hidden')
        except Exception as e:
            print(f"Error al ejecutar el juego: {e}")
            self.progress.stop()
            self.canvas.itemconfig(self.progress_window, state='hidden')
            self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
