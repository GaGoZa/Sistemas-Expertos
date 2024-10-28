import tkinter as tk
import random

class Personaje:
    def __init__(self, nombre):
        self.nombre = nombre

class Arma:
    def __init__(self, nombre):
        self.nombre = nombre

class Lugar:
    def __init__(self, nombre):
        self.nombre = nombre

class Caso:
    def __init__(self, personaje, arma, lugar):
        self.personaje = personaje
        self.arma = arma
        self.lugar = lugar

class JuegoAdivinaElAsesino:
    def __init__(self, master):
        self.master = master
        self.master.title("Adivina el Asesino")

        # Inicializa los casos
        self.casos = self.cargar_casos()
        self.caso_actual = random.choice(self.casos)

        # Contador de intentos
        self.intentos = 0
        self.max_intentos = 3

        # Configuración de la interfaz
        self.resultados_label = None  # Asegura que el label esté inicializado como None
        self.iniciar_juego()

    def cargar_casos(self):
        return [
            Caso(Personaje("La Marquesa de la Niebla"), Arma("Daga Envenenada"), Lugar("Biblioteca Encantada")),
            Caso(Personaje("El Duque Sombrío"), Arma("Bastón de Cristal Oscuro"), Lugar("Salón de los Espejos")),
            Caso(Personaje("La Condesa Carmesí"), Arma("Espada Rúnica"), Lugar("Jardín de las Sombras")),
            Caso(Personaje("El Espía Espectral"), Arma("Revolver de Bronce"), Lugar("Bóveda de los Secretos")),
            Caso(Personaje("La Viuda Negra"), Arma("Cuerda de Seda"), Lugar("Torre de la Luna")),
        ]

    def iniciar_juego(self):
        # Elimina widgets, excepto resultados_label si ya existe
        for widget in self.master.winfo_children():
            if widget != self.resultados_label:  
                widget.destroy()

        # Información inicial del caso
        self.info_label = tk.Label(self.master, text=f"Se encontró en el área {self.caso_actual.lugar.nombre} el arma {self.caso_actual.arma.nombre}.")
        self.info_label.pack()

        # Label para mostrar resultados
        if self.resultados_label is None:  # Solo crea el label si aún no existe
            self.resultados_label = tk.Label(self.master, text="")
            self.resultados_label.pack()

        # Botones de opciones
        self.boton_preguntar = tk.Button(self.master, text="Preguntar", command=self.mostrar_personajes)
        self.boton_preguntar.pack()

        self.boton_inspeccionar = tk.Button(self.master, text="Inspeccionar", command=self.mostrar_lugares)
        self.boton_inspeccionar.pack()

        self.boton_declarar = tk.Button(self.master, text="Declarar Asesino", command=self.mostrar_personajes_declarar)
        self.boton_declarar.pack()

        self.boton_salir = tk.Button(self.master, text="Salir", command=self.master.quit)
        self.boton_salir.pack()

    def mostrar_personajes(self):
        self.mostrar_opciones("personajes", [c.nombre for c in [caso.personaje for caso in self.casos]])

    def mostrar_lugares(self):
        self.mostrar_opciones("lugares", [c.nombre for c in [caso.lugar for caso in self.casos]])

    def mostrar_personajes_declarar(self):
        self.mostrar_opciones("declarar", [c.nombre for c in [caso.personaje for caso in self.casos]])

    def mostrar_opciones(self, tipo, opciones):
        for widget in self.master.winfo_children():
            if widget != self.resultados_label:  
                widget.destroy()

        for opcion in opciones:
            boton = tk.Button(self.master, text=opcion, command=lambda o=opcion: self.seleccionar_opcion(tipo, o))
            boton.pack()

        # Botón para volver a la pantalla principal
        boton_volver = tk.Button(self.master, text="Volver", command=self.iniciar_juego)
        boton_volver.pack()

    def seleccionar_opcion(self, tipo, opcion):
        if tipo == "personajes":
            if opcion == self.caso_actual.personaje.nombre:
                self.resultados_label.config(text=f"{opcion} dice: 'No recuerdo mucho, pero estaba cerca de la {self.caso_actual.lugar.nombre} cuando escuché ruidos extraños.'")
            else:
                self.resultados_label.config(text=f"{opcion} dice: 'Yo no fui, pero vi a {self.caso_actual.personaje.nombre} merodeando por allí, parecía un poco nervioso.'")
        elif tipo == "lugares":
            if opcion == self.caso_actual.lugar.nombre:
                self.resultados_label.config(text=f"Al inspeccionar {opcion}, encuentras un objeto que parece haber sido dejado apresuradamente. No sabes de quién es, pero tiene un olor extraño.")
            else:
                self.resultados_label.config(text=f"No encontré nada interesante en {opcion}.")
        elif tipo == "declarar":  # Caso para cuando se declara al asesino
            self.declarar(opcion)
        self.iniciar_juego()  # Regresa a la pantalla principal


    def declarar(self, personaje):
        if personaje == self.caso_actual.personaje.nombre:
            self.resultados_label.config(text="¡Correcto! Has adivinado al asesino.")
            self.caso_actual = random.choice(self.casos)
            self.intentos = 0
            self.max_intentos = 3
        else:
            self.intentos += 1
            self.resultados_label.config(text=f"Incorrecto. Te quedan {self.max_intentos - self.intentos} intentos.")
            if self.intentos >= self.max_intentos:
                self.resultados_label.config(text=f"Has agotado tus intentos. El asesino era {self.caso_actual.personaje.nombre}.")
                self.caso_actual = random.choice(self.casos)
                self.intentos = 0
                self.max_intentos = 3
        self.iniciar_juego()  # Regresar a la pantalla principal

# Ejecuta la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoAdivinaElAsesino(root)
    root.mainloop()
