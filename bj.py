import random

import discord
import pyttsx3
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
engine = pyttsx3.init()


def hablar(text: str):
    engine.say(text)
    engine.runAndWait()


@bot.event
async def on_ready():
    print(f"Hemos iniciado sesión como {bot.user}")


@bot.event
async def respuesta_ante_comando_inexistente(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "¡Comando no encontrado! Usa `$ayuda` para ver la lista de comandos disponibles."
        )


@bot.command()
async def hola(ctx):
    await ctx.send(f"Hola, soy un bot {bot.user}!")


@bot.command()
async def ayuda(ctx):
    ayuda_texto = """Comandos disponibles:
    $jugar - Iniciar una nueva partida de Blackjack
    $pedir - Pedir una carta adicional
    $quedarse - Mantener tus cartas actuales
    $abandonar - Abandonar la partida actual
    $reglas - Ver las reglas del juego"""
    await ctx.send(ayuda_texto)


@bot.command()
async def reglas(ctx):
    reglas_texto = """Reglas de BlackJack
    Blackjack es un juego de cartas que consiste en recibir 2 cartas, e seguir cogiendo cartas para acercarse lo mas que uno puede a 21, sin pasarse."""
    await ctx.send(reglas_texto)


# Variables de blackjack
# -----------------------------
# Reemplazar variables globales por un diccionario de juegos activos
juegos_activos = {}


class JuegoBlackjack:
    def __init__(self):
        self.barajaCartas = [
            11,
            11,
            11,
            11,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            9,
            9,
            9,
            9,
            8,
            8,
            8,
            8,
            7,
            7,
            7,
            7,
            6,
            6,
            6,
            6,
            5,
            5,
            5,
            5,
            4,
            4,
            4,
            4,
            3,
            3,
            3,
            3,
            2,
            2,
            2,
            2,
            1,
            1,
            1,
            1,
        ]
        self.deck = []
        self.deckDealer = []
        self.isPlaying = True
        self.dealerPasado = False


def MezclarCartas(barajaCartas):
    # Añadiendo lista
    # barajaCartas = barajaCartas TEMPORAL --------------------
    barajaMezclada = []

    # Usando algoritmo Fisher-Yates para mezclar
    # Mientras que la baraja de cartas tenga mas que 0 cartas
    while len(barajaCartas) > 0:

        # Se escoge un numero random entre 0 y el tamaño de la lista original
        numeroRandom = random.randint(0, len(barajaCartas) - 1)

        # El valor en la posicion escogida, se quita de la lista original y se coloca en la nueva
        barajaMezclada.append(barajaCartas[numeroRandom])
        barajaCartas.remove(barajaCartas[numeroRandom])

    return barajaMezclada


# Metodo que da una carta de una baraja a otra
def DarCarta(Baraja1, Baraja2):
    # Tomar primera carta de la baraja y ponerla en un deck
    Baraja1.append(Baraja2[0])
    Baraja2.remove(Baraja2[0])
    return Baraja1


# Metodo para imprimir lista
def ImprimirCartas(Cartas):
    for carta in Cartas:
        print(carta)


# Metodo que evalua las cartas y calcula cuantos puntos tienes
def EvaluarPuntos(deck):
    puntos = 0
    for carta in deck:
        puntos += carta
    return puntos


# Codigo del dealer
def Dealer(deckDealer, baraja, puntosDealer, dealerPasado):
    dealerPasado = False
    puntosDealer = EvaluarPuntos(deckDealer)

    print(f"Cartas del dealer: {deckDealer}")

    # Si el dealer tiene 15 o menos puntos, pedira una carta
    while puntosDealer <= 15:

        DarCarta(deckDealer, baraja)
        puntosDealer = EvaluarPuntos(deckDealer)

        print("El dealer coje una carta")
        print(f"El dealer tiene {puntosDealer} puntos")

    # Si el dealer se pasa
    if puntosDealer > 21:

        dealerPasado = True
        print(f"El dealer se paso, con {puntosDealer} puntos")
    else:

        print(f"El dealer se queda, con {puntosDealer} puntos")


# ---------------------------------
# Jugar Blackjack
@bot.command()
async def jugar(ctx):
    if ctx.author.id in juegos_activos:
        await ctx.send("¡Ya tienes una partida en curso!")
        return

    juego = JuegoBlackjack()
    juegos_activos[ctx.author.id] = juego

    # Iniciar juego
    juego.barajaCartas = MezclarCartas(juego.barajaCartas)
    DarCarta(juego.deck, juego.barajaCartas)
    DarCarta(juego.deck, juego.barajaCartas)
    DarCarta(juego.deckDealer, juego.barajaCartas)
    DarCarta(juego.deckDealer, juego.barajaCartas)

    puntos = EvaluarPuntos(juego.deck)
    await ctx.send(f"Tus cartas: {juego.deck} (Total: {puntos})")
    await ctx.send(f"Carta visible del dealer: {juego.deckDealer[0]}")
    await ctx.send(
        "¿Qué deseas hacer?\n`$pedir` para otra carta\n`$quedarse` para mantener"
    )


@bot.command()
async def pedir(ctx):
    if ctx.author.id not in juegos_activos:
        await ctx.send("No tienes una partida activa. Usa `$jugar` para comenzar.")
        return

    juego = juegos_activos[ctx.author.id]
    DarCarta(juego.deck, juego.barajaCartas)
    puntos = EvaluarPuntos(juego.deck)

    await ctx.send(f"Tus cartas: {juego.deck} (Total: {puntos})")

    if puntos > 21:
        await ctx.send(f"¡Te has pasado con {puntos} puntos! ¡Perdiste!")
        del juegos_activos[ctx.author.id]
    elif puntos == 21:
        await ctx.send("¡BlackJack! ¡Has ganado!")
        del juegos_activos[ctx.author.id]


@bot.command()
async def quedarse(ctx):
    if ctx.author.id not in juegos_activos:
        await ctx.send("No tienes una partida activa. Usa `$jugar` para comenzar.")
        return

    juego = juegos_activos[ctx.author.id]
    puntos_jugador = EvaluarPuntos(juego.deck)

    # Turno del dealer
    puntos_dealer = EvaluarPuntos(juego.deckDealer)
    while puntos_dealer <= 15:
        DarCarta(juego.deckDealer, juego.barajaCartas)
        puntos_dealer = EvaluarPuntos(juego.deckDealer)

    await ctx.send(f"Tus cartas finales: {juego.deck} (Total: {puntos_jugador})")
    await ctx.send(f"Cartas del dealer: {juego.deckDealer} (Total: {puntos_dealer})")

    # Determinar ganador
    if puntos_dealer > 21:
        await ctx.send("¡El dealer se pasó! ¡Has ganado!")
    elif puntos_dealer > puntos_jugador:
        await ctx.send("¡El dealer gana!")
    elif puntos_dealer < puntos_jugador:
        await ctx.send("¡Has ganado!")
    else:
        await ctx.send("¡Empate!")

    del juegos_activos[ctx.author.id]


@bot.command()
async def abandonar(ctx):
    if ctx.author.id in juegos_activos:
        del juegos_activos[ctx.author.id]
        await ctx.send("Has abandonado la partida.")
    else:
        await ctx.send("No tienes ninguna partida activa.")


bot.run("TOKEN")
