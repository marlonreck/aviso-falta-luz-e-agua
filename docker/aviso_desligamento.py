#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:38:02 2019

@author: Marlon Reck
e-mail: marlonreck@gmail.com
Linkedin: https://br.linkedin.com/in/marlonreck

Versão:1
Desdescription:
    Coleta avisos de falta de luz na celesc por município e bairro,
    coleta avisos de falta de água na casan por município e envia para um 
    grupo do telegram

Requires: simplejson pyTelegramBotAPI beautifulsoup4
"""

# python3-simplejson python3-ujson
import warnings
import time
import requests
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import telebot

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
bot = telebot.TeleBot("CHAVE_BOOT")
IDGRUPO = "IDGRUPO_TELEGRAM"

def celesc(url, municipio):
    "Pesquisa falta de luz por município"
    pesquisa = {"munic": municipio}
    try:
        resposta = requests.post(url, data=pesquisa, timeout=10)
    except Exception as erro:
        print(erro)
    if resposta.status_code != 200:
        return ("Site com erro: ", resposta.status_code)
    soup = BeautifulSoup(resposta.text, "html.parser")
    tag = (soup.find('pre')).get_text()
    return tag.split('Bairro :')

def casan(url, municipio):
    "Pesquisa falta de água por município"
    i = 0
    lista = []
    try:
        resposta = requests.get(url, timeout=10)
    except Exception as erro:
        print(erro)
    if resposta.status_code != 200:
        return ("Site com erro: ", str(resposta.status_code))
    soup = BeautifulSoup(resposta.text, "html.parser")
    while i < len(soup.find_all("item")):
        texto = str(soup.find_all("item")[i].get_text())
        if texto.find(municipio) != -1:
            lista.append(soup.find_all("item")[i].get_text())
        i += 1
    return lista

def pesquisa_celesc(cidade, bairro):
    "Pesquisa e envia para o bot telegram"
    url = "https://avisodesligamento.celesc.com.br/index.php"
    celesc_retorno = celesc(url, cidade)
    if len(celesc_retorno) > 0:
        for iretorno in celesc_retorno:
            if iretorno.find(bairro) != -1:
                if len(iretorno) > 4095:
                    for iquebra in range(0, len(iretorno), 4095):
                        time.sleep(3)
                        bot.reply_to(IDGRUPO, "CELESC: "+iretorno, iretorno[iquebra:iquebra+4095])
                else:
                    time.sleep(3)
                    bot.send_message(IDGRUPO, "CELESC: "+iretorno)

def pesquisa_casan(casan_cidade):
    "Pesquisa e envia para o bot telegram"
    c_url = "https://e.casan.com.br/avisos/rssfeed"
    casan_retorno = casan(c_url, casan_cidade)
    if len(casan_retorno) > 0:
        for isjretorno in casan_retorno:
            if len(isjretorno) > 4095:
                for isjquebra in range(0, len(isjretorno), 4095):
                    time.sleep(3)
                    bot.reply_to(IDGRUPO, "CELESC: "+isjretorno, isjretorno[isjquebra:isjquebra+4095])
            else:
                time.sleep(3)
                bot.send_message(IDGRUPO, isjretorno)

if __name__ == "__main__":
    pesquisa_celesc("SAO JOSE", "FORQUILHAS")
    pesquisa_casan("SÃO JOSÉ")
