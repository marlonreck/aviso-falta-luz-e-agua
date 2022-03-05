#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:38:02 2019

@author: Marlon V. Reck
e-mail: marlonreck@gmail.com
Linkedin: https://br.linkedin.com/in/marlonreck

Versão:1
Desdescription:
    Coleta avisos de falta de luz na celesc e falta de água na casan e envia 
    para o grupo do telegram

Requires: simplejson pyTelegramBotAPI beautifulsoup4
"""

# python3-simplejson python3-pytelegrambotapi python3-ujson
import requests
from bs4 import BeautifulSoup
import telebot

bot = telebot.TeleBot("INCLUIR A CHAVE DO BOT AQUI")
idgrupo = "INCLUIR O ID DO GRUPO DO TELEGRAM AQUI"

def celesc(url, municipio):
    pesquisa = {"munic": municipio}
    try:
        resposta = requests.post(url, data=pesquisa)
    except Exception as erro:
        print(erro)
    if resposta.status_code != 200:
        return ("Site com erro: ", resposta.status_code)
    else:
        soup = BeautifulSoup(resposta.text, "html.parser")
        tag = (soup.find('pre')).get_text()
        tag = (tag.split('Bairro :'))
        return tag

def casan(url, municipio):
    i = 0
    lista = []
    try:
        resposta = requests.get(url)
    except Exception as erro:
        print(erro)
    if resposta.status_code != 200:
        return ("Site com erro: ", str(resposta.status_code))
    else:
        soup = BeautifulSoup(resposta.text, "html.parser")
        while i < len(soup.find_all("item")):
            texto = str(soup.find_all("item")[i].get_text())
            if texto.find("- "+municipio) != -1:
                lista.append(soup.find_all("item")[i].get_text())
            i += 1
    return lista

celesc_retorno = celesc("https://avisodesligamento.celesc.com.br/index.php", "SAO JOSE")
for iretorno in celesc_retorno:
    bot.send_message(idgrupo, "CELESC: "+iretorno)

casan_retornoSJ = casan("https://e.casan.com.br/avisos/rssfeed", "SÃO JOSÉ")
if len(casan_retornoSJ) > 0:
    for isjretorno in casan_retornoSJ:
        bot.send_message(idgrupo, isjretorno)
