# -*- coding: utf-8 -*-
"""
Botanik Discord Bot

@author: batiste
"""
from discord.ext import commands
from discord import utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from keep_alive import keep_alive
from PIL import Image

import n_letter
import any_letter
import time
import discord
import os
import urllib

TEST_MSG = '-' + 'test'
SHUTDOWN_MSG = '-' + 'shutdown'

client = commands.Bot(command_prefix="-")

emoji = '\N{THUMBS UP SIGN}'

def scrap_meteo(ville) :

  file_name = 'screen_meteo_' + ville + '.png'
  url = 'https://www.google.fr/search?q=meteo ' + ville

  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  chrome = webdriver.Chrome(options=chrome_options)

  chrome.get(url)
  chrome.maximize_window()

  """"
  cookies_button = chrome.find_element_by_xpath(
      '/html/body/div[3]/div[3]/span/div/div/div[3]/button[2]/div')
  cookies_button.click()
  """

  time.sleep(1)

  try:

    unite_temp = chrome.find_element_by_xpath('/html/body/div[8]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/a[2]/span')
    unite_temp.click()

    time.sleep(0.5)

    chrome.save_screenshot(file_name)

    """
    # Create an Image object from an Image
    imageObject = Image.open(file_name)

    # Crop the iceberg portion
    cropped = imageObject.crop((100,100,100,100))

    # Display the cropped portion
    cropped.save(file_name)"""

    chrome.quit()

    return file_name
  except :

    chrome.quit()
    return '18878.png'

def DCDL(lettres):

    a = n_letter.analyse(lettres)

    if a == False:

        a = any_letter.analyse(lettres)

    return a


def scrap_stock(stock_name):
    url = 'https://www.google.com/search?q=cours+action+' + stock_name

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome = webdriver.Chrome(options=chrome_options)

    chrome.get(url)
    chrome.maximize_window()

    time.sleep(2)

    try:
        """cookies_button = chrome.find_element_by_xpath(
            '/html/body/div[3]/div[3]/span/div/div/div[3]/button[2]/div')
        cookies_button.click()

        time.sleep(0.5)"""

        stock_value = chrome.find_element_by_xpath(
            '//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/div[2]/div[1]/span[1]/span/span[1]'
        ).text

        stock_evolution = chrome.find_element_by_xpath('//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/div[2]/div[1]/span[2]/span[1]').text + \
            ' ' + chrome.find_element_by_xpath(
                '//*[@id="knowledge-finance-wholepage__entity-summary"]/div/g-card-section/div/g-card-section/div[2]/div[1]/span[2]/span[2]/span[1]').text

        time.sleep(2)

        chrome.quit()

    except:
        chrome.quit()

        return 'Erreur, veuillez essayer une autre action...'

    return stock_value + " [ " + stock_evolution + " ]"


def scrap_covid():

    url = 'https://www.santepubliquefrance.fr/dossiers/coronavirus-covid-19/coronavirus-chiffres-cles-et-evolution-de-la-covid-19-en-france-et-dans-le-monde'

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome = webdriver.Chrome(options=chrome_options)

    chrome.get(url)

    # chrome.maximize_window()

    time.sleep(2)

    image_url = chrome.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/img')

    urllib.request.urlretrieve(image_url.get_attribute('src'),
                               "covid_stats.jpg")

    texte_date = chrome.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]').text

    chrome.quit()

    return texte_date


@client.event
async def on_ready():
    print("We have logged in as " + str(client))
    await client.change_presence(activity=discord.Game(
        name="-help : Liste de commandes dispos"))


# A discord bot is listening to event in channels


@client.event
async def on_message(message):

    print(str(message.author) + ' : ' + message.content + '\n')

    if message.author == client.user:
        return

    if message.content.startswith('-help'):
        await message.add_reaction(emoji)
        f_command_list = open('Ressources/command_list.txt', 'r')
        await message.channel.send(
            '    Liste des commandes disponibles du [b0t]an1k :\n' +
            f_command_list.read())
        f_command_list.close()

    if message.content.startswith(SHUTDOWN_MSG):
        await message.add_reaction(emoji)
        await message.channel.send('Extinction...')
        print('\nTHE BOT HAS BEEN SHUTDOWN')
        exit()

    if message.content.startswith(TEST_MSG):
        await message.add_reaction(emoji)
        await message.channel.send('Ceci est un test ')

    if message.content.startswith('-dcdl'):
        await message.add_reaction(emoji)
        await message.channel.send(
            'Recherche en cours, Veuillez attendre un instant...')
        await message.channel.send(
            'Liste des mots disponibles avec les lettres [' +
            message.content.strip('-dcdl ') + '] : ' +
            DCDL(message.content.strip('-dcdl ')))
    
    if message.content.startswith('-meteo'):
      await message.add_reaction(emoji)
      await message.channel.send(
            'Recherche en cours, Veuillez attendre un instant...')

      ville_strip = message.content
      ville_strip = ville_strip[7:]

      texte = scrap_meteo(ville_strip)

      await message.channel.send(file = discord.File(texte))

    if message.content.startswith('-covid'):
        await message.add_reaction(emoji)
        await message.channel.send(
            'Recherche des chiffres COVID du jour en cours, Veuillez attendre un instant...'
        )
        texte = scrap_covid()
        await message.channel.send('**'+texte+'**')
        await message.channel.send(file=discord.File('covid_stats.jpg'))

    if message.content.startswith('-bourse'):

        action = message.content
        action = action[8:]
        # print(action)

        await message.add_reaction(emoji)
        await message.channel.send(
            "Recherche de la valeur de l'action, Veuillez attendre un instant..."
        )
        await message.channel.send("Valeur de l'action de " + action.upper() +
                                   ' : ' + scrap_stock(action))

keep_alive()
client.run(os.getenv('TOKEN'))
