import argparse

parser = argparse.ArgumentParser(
    description="Un script que imprime un mensaje."
    )

parser.add_argument("-m", "--mensaje", type=str, help="El mensaje a imprimir")

args = parser.parse_args()

if args.mensaje:
    print(args.mensaje)
else:
    print("Hola mundo")
