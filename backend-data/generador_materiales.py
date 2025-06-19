import json

materiales = [
    {"nombre": "Cartón", "peso": 150},
    {"nombre": "Plástico duro", "peso": 60},
    {"nombre": "Rafia", "peso": 45}
]

with open("materiales.json", "w") as archivo:
    json.dump(materiales, archivo, indent=4)

print("Archivo JSON creado: materiales.json")
