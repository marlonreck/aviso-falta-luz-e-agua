#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:38:02 2019

@author: Marlon Reck
e-mail: marlonreck@gmail.com
Linkedin: https://br.linkedin.com/in/marlonreck

Versão:2
Desdescription:
    Coleta avisos de falta de luz na celesc por município e bairro.
    Coleta avisos de falta de água na casan por município e envia para um 
    grupo do telegram.

Requires: simplejson pyTelegramBotAPI beautifulsoup4
"""

import os
import time
import requests
from bs4 import BeautifulSoup
import telebot
from dotenv import load_dotenv

load_dotenv(override=True)
CHAVE_BOOT = os.getenv("CHAVE_BOOT")
CHAVE_GRUPO = os.getenv("IDGRUPO_TELEGRAM")

bot = telebot.TeleBot(CHAVE_BOOT)
IDGRUPO = CHAVE_GRUPO

def split_mensagem(text, max_length=4095):
    "Divide mensagens respeitando espaços ou quebras de linha."
    parts = []
    while len(text) > max_length:
        split_at = text.rfind('\n', 0, max_length)
        if split_at == -1:
            split_at = text.rfind(' ', 0, max_length)
        if split_at == -1:
            split_at = max_length
        parts.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text:
        parts.append(text)
    return parts

def celesc(url, municipio):
    "Pesquisa falta de luz por município."
    pesquisa = {"munic": municipio}
    try:
        resposta = requests.post(url, data=pesquisa, timeout=10, verify=False)
    except Exception as erro:
        print(erro)
        return []
    if resposta.status_code != 200:
        print(f"Erro Celesc: {resposta.status_code}")
        return []
    soup = BeautifulSoup(resposta.text, "html.parser")
    tag = (soup.find('pre')).get_text()
    return tag.split('Bairro :')

def casan(url, municipio):
    "Pesquisa falta de água por município."
    lista = []
    try:
        resposta = requests.get(url, timeout=10, verify=False)
    except Exception as erro:
        print(erro)
        return []
    if resposta.status_code != 200:
        print(f"Erro Casan: {resposta.status_code}")
        return []
    soup = BeautifulSoup(resposta.text, "html.parser")
    for item in soup.find_all("item"):
        texto = item.get_text()
        if municipio.upper() in texto.upper():
            lista.append(texto)
    return lista

def enviar_mensagem(texto, prefixo=""):
    "Envia mensagem para o Telegram, quebrando se necessário, já considerando prefixo e contagem."
    texto_seguro = texto
    # Primeiro, simular prefixo para cálculo correto
    prefixo_simples = f"{prefixo}: "
    max_prefixo_len = len(prefixo_simples)

    # Se precisar quebrar, precisa considerar também (x/y) adicional
    max_length = 4096 - max_prefixo_len - 7  # 7 é a margem para (x/y): 
    partes = split_mensagem(texto_seguro, max_length=max_length)
    total = len(partes)
    for idx, parte in enumerate(partes, start=1):
        time.sleep(3)
        cabecalho = f"{prefixo} ({idx}/{total}): " if total > 1 else f"{prefixo}: "
        bot.send_message(IDGRUPO, cabecalho + parte)

def pesquisa_celesc(cidade, bairro):
    "Pesquisa e envia avisos da Celesc."
    url = "https://avisodesligamento.celesc.com.br/index.php"
    celesc_retorno = celesc(url, cidade)
    if celesc_retorno:
        for iretorno in celesc_retorno:
            if bairro.upper() in iretorno.upper():
                enviar_mensagem(iretorno, prefixo="CELESC")

def pesquisa_casan(cidade):
    "Pesquisa e envia avisos da Casan."
    url = "https://e.casan.com.br/avisos/rssfeed"
    casan_retorno = casan(url, cidade)
    if casan_retorno:
        for aviso in casan_retorno:
            enviar_mensagem(aviso, prefixo="CASAN")

if __name__ == "__main__":
    pesquisa_celesc("SAO JOSE", "FORQUILHAS")
    pesquisa_casan("SÃO JOSÉ")
    
