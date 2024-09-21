import json

# Base de datos inicial de conocimiento
conocimiento = {
    "Hola": "¡Hola! ¿Cómo estás?",
    "¿Cómo estás?": "Estoy bien, gracias. ¿Y tú?",
    "¿De qué te gustaría hablar?": "Me gusta hablar de personajes de anime, ¿a ti qué te gustaría saber?"
}

# Cargar la base de datos desde un archivo JSON
def cargar_conocimiento():
    try:
        with open('Practica2/conocimiento_anime.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return conocimiento

# Guardar el conocimiento en un archivo JSON
def guardar_conocimiento(data):
    with open('Practica2/conocimiento_anime.json', 'w') as file:
        json.dump(data, file, indent=4)

# Función para chatear y agregar nuevo conocimiento
def chat():
    base_conocimiento = cargar_conocimiento()
    
    print("Bienvenido al chat de personajes de anime.")
    print("Escribe 'salir' para terminar la conversación.")
    
    while True:
        entrada_usuario = input("Tú: ")
        
        if entrada_usuario.lower() == 'salir':
            print("¡Hasta luego!")
            break
        
        # Buscar la respuesta en la base de conocimiento
        respuesta = base_conocimiento.get(entrada_usuario)
        
        if respuesta:
            print(f"Chatbot: {respuesta}")
        else:
            print("Chatbot: No tengo una respuesta para eso.")
            nueva_respuesta = input("¿Qué debería responder la próxima vez que me preguntes eso?: ")
            # Agregar nuevo conocimiento
            base_conocimiento[entrada_usuario] = nueva_respuesta
            guardar_conocimiento(base_conocimiento)
            print("Chatbot: ¡Gracias! Ahora lo recordaré.")

# Ejecutar el chat
if __name__ == "__main__":
    chat()
