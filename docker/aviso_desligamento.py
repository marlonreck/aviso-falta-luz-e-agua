#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:38:02 2019

@author: marlon
"""

# python3-simplejson python3-pytelegrambotapi python3-ujson
import requests
from bs4 import BeautifulSoup
import telebot


bot = telebot.TeleBot("734308366:AAGW6Pw5PwHNjj0LIvtGDkGedPhDuFNSxA8")
# grupo aviso
# idgrupo = "-325650074"
# grupo teste
idgrupo = "-350862650"


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


# celesc_retorno = celesc("http://site.celesc.com.br/aplicativos/aviso_desligamento/index.php", "SAO JOSE")
celesc_retorno = celesc("https://avisodesligamento.celesc.com.br/index.php", "SAO JOSE")
for iretorno in celesc_retorno:
    bot.send_message(idgrupo, "CELESC: "+iretorno)

casan_retornoSJ = casan("https://e.casan.com.br/avisos/rssfeed", "SÃO JOSÉ")
if len(casan_retornoSJ) > 0:
    for isjretorno in casan_retornoSJ:
        bot.send_message(idgrupo, isjretorno)

casan_retorno = casan("https://e.casan.com.br/avisos/rssfeed", "FORQUILHINHA")
if len(casan_retorno) > 0:
    for iforquilhasretorno in casan_retorno:
        bot.send_message(idgrupo, iforquilhasretorno)
