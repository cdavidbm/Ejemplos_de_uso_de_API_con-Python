import discord
from discord.ext import commands
import random
import requests
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

# ----------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    
# ----------------------------------------------------------------------------------------

@bot.command()
async def saludar(ctx):
    await ctx.send('¡Hola!Soy un bot de prueba!')

# ----------------------------------------------------------------------------------------

def get_weather_info(city):
    base_url = f"https://wttr.in/{city}?format=%C+%t&lang=es"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "No se pudo obtener la información del clima. Por favor, inténtalo más tarde."
    
@bot.command()
async def weather(ctx, *, city):
    weather_info = get_weather_info(city)
    await ctx.send(f"Clima en {city}: {weather_info}")
    
# ----------------------------------------------------------------------------------------

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command()
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)
    
# ----------------------------------------------------------------------------------------

def dato_curioso():
    url = 'https://uselessfacts.jsph.pl/api/v2/facts/random'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['text']
    else:
        return "No se pudo obtener un dato curioso. Por favor, inténtalo más tarde."
    
@bot.command()
async def dato(ctx):
    dato = dato_curioso()
    await ctx.send(dato)

# ----------------------------------------------------------------------------------------

def imagen_gatos():
    http_status_codes = [
    200, 201, 202, 204, 301, 302, 304, 400, 401, 403, 404, 405, 408, 409, 410, 
    418, 429, 500, 501, 502, 503, 504
]
    numero = random.choice(http_status_codes)
    url = f'https://http.cat/{numero}.jpg'
    return url

@bot.command()
async def gato(ctx):
    dato = imagen_gatos()
    await ctx.send(dato)

bot.run('')