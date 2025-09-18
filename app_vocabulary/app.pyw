import tkinter as tk
import random
import openpyxl

class JuegoVocabulario:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Vocabulario")
        self.root.geometry("600x500")

        self.label_superior = tk.Label(self.root, text="", font=("Arial", 16))
        self.label_superior.pack(pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.boton_reiniciar = tk.Button(self.root, text="🔄 Reiniciar", command=self.iniciar_juego, font=("Arial", 12))
        self.boton_reiniciar.pack(pady=10)

        self.iniciar_juego()

    def iniciar_juego(self):
        self.puntos = 0
        self.errores_consecutivos = 0
        self.indice_actual = 0
        self.tamano_lote = 5
        self.tiempo_restante = 180  # 3 minutos

        self.vocabulario_completo = self.cargar_vocabulario_excel("vocabulary.xlsx")
        random.shuffle(self.vocabulario_completo)

        self.botones_es = []
        self.botones_en = []
        self.palabra_seleccionada = None

        self.actualizar_tiempo()
        self.cargar_siguiente_lote()

    def cargar_vocabulario_excel(self, archivo):
        wb = openpyxl.load_workbook(archivo)
        hoja = wb.active
        vocabulario = []

        for fila in hoja.iter_rows(min_row=2, values_only=True):
            palabra_en = fila[1]
            palabra_es = fila[2]
            if palabra_en and palabra_es:
                vocabulario.append((palabra_es.strip(), palabra_en.strip()))
        return vocabulario

    def cargar_siguiente_lote(self):
        self.limpiar_pantalla()

        self.botones_es = []
        self.botones_en = []
        self.palabra_seleccionada = None

        lote = self.vocabulario_completo[self.indice_actual:self.indice_actual + self.tamano_lote]
        if not lote:
            self.mostrar_mensaje("¡Fin del juego!", "¡Completaste todas las palabras!")
            return

        self.indice_actual += self.tamano_lote

        self.palabras_es = [pair[0] for pair in lote]
        self.palabras_en = [pair[1] for pair in lote]
        self.vocabulario_actual = dict(lote)

        random.shuffle(self.palabras_es)
        random.shuffle(self.palabras_en)

        # Columna Español
        self.frame_es = tk.Frame(self.frame)
        self.frame_es.pack(side="left", padx=20)
        tk.Label(self.frame_es, text="Español", font=("Arial", 14)).pack()
        for palabra in self.palabras_es:
            btn = tk.Button(self.frame_es, text=palabra, font=("Arial", 12), bg="white",
                            relief="groove", width=20, command=lambda p=palabra: self.seleccionar_es(p))
            btn.pack(pady=6)
            self.botones_es.append(btn)

        # Columna Inglés
        self.frame_en = tk.Frame(self.frame)
        self.frame_en.pack(side="right", padx=20)
        tk.Label(self.frame_en, text="Inglés", font=("Arial", 14)).pack()
        for palabra in self.palabras_en:
            btn = tk.Button(self.frame_en, text=palabra, font=("Arial", 12), bg="white",
                            relief="groove", width=20, command=lambda p=palabra: self.seleccionar_en(p))
            btn.pack(pady=6)
            self.botones_en.append(btn)

    def seleccionar_es(self, palabra):
        self.palabra_seleccionada = palabra

    def seleccionar_en(self, palabra):
        if self.palabra_seleccionada:
            correcto = self.vocabulario_actual.get(self.palabra_seleccionada) == palabra
            if correcto:
                self.puntos += 10
                self.errores_consecutivos = 0
                self.deshabilitar_pares(self.palabra_seleccionada, palabra)
            else:
                self.puntos -= 10
                if self.puntos <= 0:
                    self.errores_consecutivos += 1
                else:
                    self.errores_consecutivos = 0

            self.actualizar_superior()
            self.palabra_seleccionada = None

            if self.puntos >= 200:
                self.mostrar_mensaje("¡Ganaste!", "Has alcanzado 200 puntos.")
            elif self.puntos <= 0 and self.errores_consecutivos >= 3:
                self.mostrar_mensaje("¡Perdiste!", "Cometiste 3 errores seguidos con 0 puntos.")
            elif all(btn['state'] == "disabled" for btn in self.botones_es):
                self.cargar_siguiente_lote()

    def deshabilitar_pares(self, palabra_es, palabra_en):
        for btn in self.botones_es:
            if btn['text'] == palabra_es:
                btn.configure(bg="#add8e6", state="disabled")  # celeste
        for btn in self.botones_en:
            if btn['text'] == palabra_en:
                btn.configure(bg="#add8e6", state="disabled")

    def limpiar_pantalla(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def mostrar_mensaje(self, titulo, mensaje):
        msg = tk.Toplevel()
        msg.title(titulo)
        tk.Label(msg, text=mensaje, font=("Arial", 14)).pack(padx=20, pady=20)
        tk.Button(msg, text="Salir", command=self.root.quit).pack(pady=10)

    def actualizar_superior(self):
        minutos = self.tiempo_restante // 60
        segundos = self.tiempo_restante % 60
        tiempo_formateado = f"{minutos}:{segundos:02d}"
        self.label_superior.config(text=f"Puntos: {self.puntos} | Tiempo: {tiempo_formateado}")

    def actualizar_tiempo(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.actualizar_superior()
            self.root.after(1000, self.actualizar_tiempo)
        else:
            self.mostrar_mensaje("¡Tiempo agotado!", "Se acabó el tiempo. ¡Inténtalo de nuevo!")

# Ejecutar juego
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoVocabulario(root)
    root.mainloop()
#hola