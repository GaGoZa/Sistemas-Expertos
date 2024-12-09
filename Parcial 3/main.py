import tkinter as tk
import sqlite3

class MedicalExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Expert System")

        self.conn = sqlite3.connect("medical_expert_system.db")
        self.cursor = self.conn.cursor()

        self.symptoms = []
        self.current_symptom_index = 0
        self.selected_intensities = []

        self.create_widgets()

    def create_widgets(self):
        self.symptom_frame = tk.Frame(self.root)
        self.symptom_frame.pack(pady=10)

        self.symptom_label = tk.Label(self.symptom_frame, text="Select Symptom and Intensity:")
        self.symptom_label.pack()

        self.symptom_name_var = tk.StringVar()
        self.symptom_name_label = tk.Label(self.symptom_frame, textvariable=self.symptom_name_var)
        self.symptom_name_label.pack(pady=10)

        self.intensity_var = tk.StringVar(value="no")
        self.intensity_frame = tk.Frame(self.symptom_frame)
        self.intensity_frame.pack(pady=5, anchor=tk.W)

        tk.Radiobutton(self.intensity_frame, text="no", variable=self.intensity_var, value="no").pack(side=tk.LEFT)
        tk.Radiobutton(self.intensity_frame, text="medio", variable=self.intensity_var, value="medio").pack(side=tk.LEFT)
        tk.Radiobutton(self.intensity_frame, text="alto", variable=self.intensity_var, value="alto").pack(side=tk.LEFT)

        self.back_button = tk.Button(self.symptom_frame, text="Anterior", command=self.previous_symptom)
        self.back_button.pack(side=tk.LEFT, padx=10)
        self.back_button.config(state=tk.DISABLED)

        self.next_button = tk.Button(self.symptom_frame, text="Siguiente", command=self.next_symptom)
        self.next_button.pack(side=tk.LEFT, padx=10)
        self.next_button.config(state=tk.DISABLED)

        self.diagnose_button = tk.Button(self.symptom_frame, text="Diagnóstico", command=self.diagnose)
        self.diagnose_button.pack(pady=10)
        self.diagnose_button.config(state=tk.DISABLED)

        self.result_label = tk.Label(self.root, text="", wraplength=300, justify=tk.LEFT)
        self.result_label.pack(pady=10)

        self.load_symptoms()

    def load_symptoms(self):
        self.cursor.execute("SELECT name FROM symptoms")
        self.symptoms = self.cursor.fetchall()

        if self.symptoms:
            self.show_next_symptom()
        else:
            self.symptom_name_var.set("No se encontraron síntomas en la base de datos.")

    def show_next_symptom(self):
        if self.current_symptom_index < len(self.symptoms):
            symptom_name = self.symptoms[self.current_symptom_index][0]
            self.symptom_name_var.set(symptom_name)
            self.current_symptom_index += 1
            self.back_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL if self.current_symptom_index < len(self.symptoms) else tk.DISABLED)
            self.diagnose_button.config(state=tk.NORMAL if self.current_symptom_index == len(self.symptoms) else tk.DISABLED)
        else:
            self.symptom_name_var.set("Todos los síntomas respondidos.")
            self.next_button.config(state=tk.DISABLED)
            self.diagnose_button.config(state=tk.NORMAL)

    def next_symptom(self):
        intensity = self.intensity_var.get()
        self.selected_intensities.append(intensity)
        self.show_next_symptom()

    def previous_symptom(self):
        if self.current_symptom_index > 0:
            self.current_symptom_index -= 1
            self.symptom_name_var.set(self.symptoms[self.current_symptom_index][0])
            self.selected_intensities.pop()
            self.next_button.config(state=tk.NORMAL)
            self.diagnose_button.config(state=tk.DISABLED if self.current_symptom_index < len(self.symptoms) else tk.NORMAL)
        self.back_button.config(state=tk.DISABLED if self.current_symptom_index == 0 else tk.NORMAL)

    def diagnose(self):
        try:
            query = """
                SELECT DISTINCT d.name AS disease_name
                FROM diseases d
                JOIN disease_symptoms ds ON d.id = ds.disease_id
                JOIN symptoms s ON ds.symptom_id = s.id
                WHERE s.name = ? AND ds.intensity = ?
            """
            self.cursor.execute(query, (self.symptoms[0][0], self.selected_intensities[0]))
            diseases = self.cursor.fetchall()

            if diseases:
                self.result_label.config(text="Estas son las enfermedades asociadas con los sintomas seleccionados:\n" + "\n".join([row[0] for row in diseases]))
            else:
                self.result_label.config(text="No se encontraron enfermedades asociadas con los sintomas seleccionados.")

        except sqlite3.Error as e:
            print(e)
            self.result_label.config(text="Error occurred while querying the database.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalExpertSystem(root)
    root.mainloop()



