import sirope
from models.animal import Animal

srp = sirope.Sirope()

perros = [
    Animal("Max", "Perro", "Labrador", "3 años", "Max es un labrador muy juguetón y cariñoso, ideal para familias con niños.", foto="max.jpg"),
    Animal("Luna", "Perro", "Beagle", "2 años", "Luna es una beagle curiosa y activa. Le encanta explorar y jugar al aire libre.", foto="luna.jpg"),
    Animal("Rocky", "Perro", "Pastor Alemán", "5 años", "Rocky es un pastor alemán noble y leal. Está bien entrenado y es muy obediente.", estado="en tratamiento", foto="rocky.jpg"),
    Animal("Nala", "Perro", "Golden Retriever", "1 año", "Nala es una cachorra golden muy cariñosa. Busca una familia que le dé mucho amor.", foto="nala.jpg"),
    Animal("Bruno", "Perro", "Bulldog Francés", "4 años", "Bruno es un bulldog tranquilo y sociable. Perfecto para pisos pequeños.", estado="adoptado", foto="bruno.jpg"),
    Animal("Cleo", "Perro", "Husky Siberiano", "2 años", "Cleo es una husky llena de energía. Necesita ejercicio diario y espacio.", foto="cleo.jpg"),
]

for p in perros:
    srp.save(p)

print("Datos de prueba insertados correctamente.")