import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

class Personaje:
    def __init__(self, nombre, generacion, magia, gremio):
        self.nombre = nombre
        self.generacion = generacion
        self.magia = magia
        self.gremio = gremio

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "generacion": self.generacion,
            "magia": self.magia,
            "gremio": self.gremio
        }

def cargar_personajes():
    if os.path.exists("personajes.json"):
        with open("personajes.json", "r") as f:
            personajes_data = json.load(f)
            return [Personaje(**data) for data in personajes_data]
    else:
        return [
            Personaje("Natsu Dragneel", "Primera", "Dragon Slayer de Fuego", "Fairy Tail"),
            Personaje("Gajeel Redfox", "Primera", "Dragon Slayer de Hierro", "Fairy Tail"),
            Personaje("Wendy Marvell", "Primera", "Dragon Slayer de Cielo", "Fairy Tail"),
            Personaje("Laxus Dreyar", "Segunda", "Dragon Slayer de Rayo", "Fairy Tail"),
            Personaje("Cobra", "Segunda", "Dragon Slayer de Veneno", "Oración Seis"),
            Personaje("Sting Eucliffe", "Tercera", "Dragon Slayer de Luz", "Sabertooth"),
            Personaje("Rogue Cheney", "Tercera", "Dragon Slayer de Sombras", "Sabertooth"),
            Personaje("Lucy Heartfilia", None, "Magia Estelar", "Fairy Tail"),
            Personaje("Gray Fullbuster", None, "Magia de Hielo", "Fairy Tail"),
            Personaje("Erza Scarlet", None, "Caballero de Armadura", "Fairy Tail"),
            Personaje("Juvia Lockser", None, "Magia de Agua", "Fairy Tail"),
            Personaje("Sherria Blendy", None, "Dios Slayer de Cielo", "Lamia Scale"),
            Personaje("Kagura Mikazuchi", None, "Magia de Gravedad", "Mermaid Heel"),
            Personaje("Ichiya Vandalay Kotobuki", None, "Magia de Perfume", "Blue Pegasus")
        ]

def guardar_personajes(personajes):
    with open("personajes.json", "w") as f:
        json.dump([p.to_dict() for p in personajes], f)

def filtrar_pregunta(personajes, atributo, valor, negacion=False):
    if negacion:
        return [p for p in personajes if getattr(p, atributo) != valor]
    else:
        return [p for p in personajes if getattr(p, atributo) == valor]

def aprender_personaje(personajes):
    nombre = simpledialog.askstring("Nuevo Personaje", "No pude adivinar. ¿En quién pensabas?")
    generacion = None if simpledialog.askstring("Generación", "¿Cuál es su generación (si aplica)?") == '' else simpledialog.askstring("Generación", "¿Cuál es su generación (si aplica)?")
    magia = simpledialog.askstring("Magia", "¿Qué tipo de magia usa?")
    gremio = simpledialog.askstring("Gremio", "¿A qué gremio pertenece?")

    nuevo_personaje = Personaje(nombre, generacion, magia, gremio)
    personajes.append(nuevo_personaje)
    guardar_personajes(personajes)
    messagebox.showinfo("Gracias", f"¡Gracias! He aprendido sobre {nombre}.")

def juego_akinator():
    personajes = cargar_personajes()
    personajes_restantes = personajes

    # Pregunta si es Dragon Slayer
    respuesta = simpledialog.askstring("Pregunta", "¿Es un Dragon Slayer? (Sí/No):").strip().lower()
    if respuesta == "sí":
        personajes_restantes = filtrar_pregunta(personajes_restantes, "generacion", None, negacion=True)

        # Pregunta por generación
        respuesta = simpledialog.askstring("Pregunta", "¿Es de primera generación? (Sí/No):").strip().lower()
        if respuesta == "sí":
            personajes_restantes = filtrar_pregunta(personajes_restantes, "generacion", "Primera")
        else:
            respuesta = simpledialog.askstring("Pregunta", "¿Es de segunda generación? (Sí/No):").strip().lower()
            if respuesta == "sí":
                personajes_restantes = filtrar_pregunta(personajes_restantes, "generacion", "Segunda")
            else:
                personajes_restantes = filtrar_pregunta(personajes_restantes, "generacion", "Tercera")

        # Pregunta por gremio
        gremios = set(p.gremio for p in personajes_restantes)
        for gremio in gremios:
            respuesta = simpledialog.askstring("Pregunta", f"¿Pertenece al gremio {gremio}? (Sí/No):").strip().lower()
            if respuesta == "sí":
                personajes_restantes = filtrar_pregunta(personajes_restantes, "gremio", gremio)
            else:
                personajes_restantes = filtrar_pregunta(personajes_restantes, "gremio", gremio, negacion=True)
    
    else:
        # Filtra personajes que no son Dragon Slayers
        personajes_restantes = filtrar_pregunta(personajes_restantes, "generacion", None)

        # Pregunta por gremio
        gremios = set(p.gremio for p in personajes_restantes)
        for gremio in gremios:
            respuesta = simpledialog.askstring("Pregunta", f"¿Pertenece al gremio {gremio}? (Sí/No):").strip().lower()
            if respuesta == "sí":
                personajes_restantes = filtrar_pregunta(personajes_restantes, "gremio", gremio)
                break
            else:
                personajes_restantes = filtrar_pregunta(personajes_restantes, "gremio", gremio, negacion=True)

        # Pregunta por tipo de magia
        magias = set(p.magia for p in personajes_restantes)
        for magia in magias:
            respuesta = simpledialog.askstring("Pregunta", f"¿Usa magia de {magia}? (Sí/No):").strip().lower()
            if respuesta == "sí":
                personajes_restantes = filtrar_pregunta(personajes_restantes, "magia", magia)
                break
            else:
                personajes_restantes = filtrar_pregunta(personajes_restantes, "magia", magia, negacion=True)

    # Resultado final
    if len(personajes_restantes) == 1:
        messagebox.showinfo("Resultado", f"Creo que estás pensando en: {personajes_restantes[0].nombre}")
        # Preguntar si es correcto
        respuesta = simpledialog.askstring("Pregunta", "¿Es correcto? (Sí/No):").strip().lower()
        if respuesta != "sí":
            aprender_personaje(personajes)
    else:
        aprender_personaje(personajes)

# Crear la ventana principal
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal
juego_akinator()
root.mainloop()
