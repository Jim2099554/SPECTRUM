import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# --- Funciones auxiliares ---
def ask_folder(title, initialdir=None):
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title=title, initialdir=initialdir)
    root.destroy()
    return folder

def ask_file(title, initialdir=None):
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(title=title, initialdir=initialdir)
    root.destroy()
    return file

# --- Wizard gráfico ---
def run_wizard():
    root = tk.Tk()
    root.title("Asistente de configuración de SENTINELA")
    root.geometry("500x400")
    root.resizable(False, False)

    values = {}

    def step1():
        for widget in root.winfo_children(): widget.destroy()
        tk.Label(root, text="1. Selecciona la base de datos de PPL", font=("Arial", 12, "bold")).pack(pady=10)
        def select_db():
            db_path = ask_file("Selecciona el archivo de base de datos SQLite")
            if db_path:
                values["DATABASE_URL"] = f"sqlite:///{db_path}"
                step2()
        tk.Button(root, text="Seleccionar archivo .db", command=select_db).pack(pady=20)

    def step2():
        for widget in root.winfo_children(): widget.destroy()
        tk.Label(root, text="2. Selecciona la carpeta de fotos de PPL", font=("Arial", 12, "bold")).pack(pady=10)
        def select_photos():
            folder = ask_folder("Selecciona la carpeta de fotos")
            if folder:
                values["PHOTOS_DIR"] = folder
                step3()
        tk.Button(root, text="Seleccionar carpeta", command=select_photos).pack(pady=20)

    def step3():
        for widget in root.winfo_children(): widget.destroy()
        tk.Label(root, text="3. Selecciona la carpeta de audios de llamadas", font=("Arial", 12, "bold")).pack(pady=10)
        def select_audios():
            folder = ask_folder("Selecciona la carpeta de audios")
            if folder:
                values["AUDIO_UPLOAD_DIR"] = folder
                step4()
        tk.Button(root, text="Seleccionar carpeta", command=select_audios).pack(pady=20)

    def step4():
        for widget in root.winfo_children(): widget.destroy()
        tk.Label(root, text="4. Ingresa la clave secreta JWT", font=("Arial", 12, "bold")).pack(pady=10)
        entry = tk.Entry(root, show="*", width=40)
        entry.pack(pady=20)
        def next_step():
            val = entry.get()
            if val:
                values["JWT_SECRET"] = val
                step5()
            else:
                messagebox.showerror("Error", "Debes ingresar una clave JWT.")
        tk.Button(root, text="Siguiente", command=next_step).pack(pady=10)

    def step5():
        for widget in root.winfo_children(): widget.destroy()
        tk.Label(root, text="5. Ingresa la clave de cifrado", font=("Arial", 12, "bold")).pack(pady=10)
        entry = tk.Entry(root, show="*", width=40)
        entry.pack(pady=20)
        def next_step():
            val = entry.get()
            if val:
                values["ENCRYPTION_KEY"] = val
                step6()
            else:
                messagebox.showerror("Error", "Debes ingresar una clave de cifrado.")
        tk.Button(root, text="Siguiente", command=next_step).pack(pady=10)

    def step6():
        for widget in root.winfo_children(): widget.destroy()
        tk.Label(root, text="6. ¿Configurar correo para pruebas con MailHog?", font=("Arial", 12, "bold")).pack(pady=10)
        def set_mailhog():
            values["SMTP_HOST"] = "localhost"
            values["SMTP_PORT"] = "1025"
            step7()
        def skip_mailhog():
            step7()
        tk.Button(root, text="Sí, usar MailHog", command=set_mailhog).pack(pady=10)
        tk.Button(root, text="No configurar correo", command=skip_mailhog).pack(pady=10)

    def step7():
        for widget in root.winfo_children(): widget.destroy()
        tk.Label(root, text="7. ¿En qué formato deseas guardar la configuración?", font=("Arial", 12, "bold")).pack(pady=10)
        var = tk.StringVar(value="ambos")
        tk.Radiobutton(root, text=".env (variables de entorno)", variable=var, value="env").pack(anchor="w", padx=40)
        tk.Radiobutton(root, text="config.json (estructura avanzada)", variable=var, value="json").pack(anchor="w", padx=40)
        tk.Radiobutton(root, text="Ambos", variable=var, value="ambos").pack(anchor="w", padx=40)
        def finish():
            selected = var.get()
            env_lines = [f"{k}={v}" for k,v in values.items()]
            json_data = dict(values)
            if selected in ("env", "ambos"):
                with open(".env", "w", encoding="utf-8") as f:
                    f.write("\n".join(env_lines) + "\n")
            if selected in ("json", "ambos"):
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
            # --- Nueva sección: preguntar si quiere arrancar backend/frontend ---
            def launch_services():
                import subprocess, sys, platform
                cwd = os.path.dirname(os.path.abspath(__file__))
                venv_path = os.path.join(cwd, "venv311")
                backend_cmd = None
                frontend_cmd = None
                # Comandos multiplataforma
                if platform.system() == "Windows":
                    activate = f"{venv_path}\\Scripts\\activate.bat"
                    backend_cmd = f'start cmd /k "call {activate} && uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"'
                    frontend_cmd = f'start cmd /k "cd frontend && npm run dev"'
                else:
                    activate = f"source {venv_path}/bin/activate"
                    backend_cmd = f'gnome-terminal -- bash -c "cd {cwd} && {activate} && uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000; exec bash"'
                    frontend_cmd = f'gnome-terminal -- bash -c "cd {cwd}/frontend && npm run dev; exec bash"'
                # Preguntar opciones
                ops = tk.Toplevel(root)
                ops.title("¿Arrancar servicios?")
                tk.Label(ops, text="¿Deseas arrancar el backend, el frontend o ambos?", font=("Arial", 12, "bold")).pack(pady=10)
                sel = tk.StringVar(value="ambos")
                tk.Radiobutton(ops, text="Solo backend", variable=sel, value="backend").pack(anchor="w", padx=40)
                tk.Radiobutton(ops, text="Solo frontend", variable=sel, value="frontend").pack(anchor="w", padx=40)
                tk.Radiobutton(ops, text="Ambos", variable=sel, value="ambos").pack(anchor="w", padx=40)
                def launch_selected():
                    choice = sel.get()
                    try:
                        if choice in ("backend", "ambos"):
                            subprocess.Popen(backend_cmd, shell=True, cwd=cwd)
                        if choice in ("frontend", "ambos"):
                            subprocess.Popen(frontend_cmd, shell=True, cwd=cwd)
                        messagebox.showinfo("¡Listo!", "Servicios lanzados en nuevas terminales. Si ves errores, revisa la configuración o dependencias.")
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo lanzar los servicios: {e}")
                    ops.destroy()
                    root.destroy()
                tk.Button(ops, text="Lanzar", command=launch_selected).pack(pady=20)
            # Preguntar si quiere lanzar servicios
            if messagebox.askyesno("¿Lanzar servicios?", "¿Deseas arrancar el backend y/o frontend ahora?"):
                launch_services()
            else:
                messagebox.showinfo("¡Listo!", "La configuración ha sido guardada.")
                root.destroy()
        tk.Button(root, text="Finalizar y guardar", command=finish).pack(pady=20)

    step1()
    root.mainloop()

if __name__ == "__main__":
    run_wizard()
