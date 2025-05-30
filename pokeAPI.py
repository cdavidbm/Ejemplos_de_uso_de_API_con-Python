import requests


def obtener_pokemon(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return {
            "nombre": datos["name"],
            "id": datos["id"],
            "tipos": [tipo["type"]["name"] for tipo in datos["types"]],
            "altura": datos["height"] / 10,  # convertir a metros
            "peso": datos["weight"] / 10,  # convertir a kg
        }


# EJEMPLO DE USO
pokemon_nombre = input("Introduce el nombre de un Pokemon: ")
pokemon = obtener_pokemon(pokemon_nombre)

if pokemon:
    print("\nInformación del Pokemon:")
    print(f"Nombre: {pokemon['nombre'].capitalize()}")
    print(f"ID: {pokemon['id']}")
    print(f"Tipos: {', '.join(pokemon['tipos'])}")
    print(f"Altura: {pokemon['altura']} m")
    print(f"Peso: {pokemon['peso']} kg")

else:
    print("No se encontró el Pokemon o hubo un error en la búsqueda.")
