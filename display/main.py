#!/usr/bin/python
# -*- coding: utf-8 -*-

import epd2in7b
import Image
import ImageFont
import ImageDraw
import Adafruit_DHT
import time
import requests
import json
import datetime

COLORED = 1
UNCOLORED = 0

API_TOKEN = '5CB95DC15E4D4BAEB770F304A3987196'
API_URL_BASE = 'http://localhost/'

def getPrinterStatus():
    api_url = '{}{}'.format(API_URL_BASE, 'api/printer')

    headers = {
         'Content-Type': 'application/json',
         'X-Api-Key': API_TOKEN 
          }
    response = requests.get(api_url, headers=headers)

    if (response.status_code == 200):
        return response.json()
    else:
        return None

def getJobInfo():
    api_url = '{}{}'.format(API_URL_BASE, 'api/job')
    headers = {
         'Content-Type': 'application/json',
         'X-Api-Key': API_TOKEN 
          }
    response = requests.get(api_url, headers=headers)

    if (response.status_code == 200):
        return response.json()
    else:
        return None



def drawPair(x, y, caption, value, x2 = None, y2 = None, font = None):
    if (x2 == None):
        x2 = x
    if (y2 == None):
        y2 = y + 12
    if (font == None):
        font = fval

    epd.draw_string_at(frame_black, x, y, value, font, COLORED)
    epd.draw_string_at(frame_red, x2, y2, caption, fcapt, COLORED)

def drawSensors1(printer_status = None):
    if (printer_status == None):
        drawPair(223, 48, "EXTRUS.", "N/A")
        drawPair(223, 82, "SUPERF.", "N/A")
    else:
        drawPair(223, 48, "EXTRUS.", "{0:0.0f} C".format(printer_status['temperature']['tool0']['actual']))
        drawPair(223, 82, "SUPERF.", "{0:0.0f} C".format(printer_status['temperature']['bed']['actual']))

def drawSensors2():
    # Define o tipo de sensor
    sensor = Adafruit_DHT.DHT11

    # Define a GPIO conectada ao pino de dados do sensor
    pino_sensor = 21

    # Efetua a leitura do sensor
    umid, temp = Adafruit_DHT.read_retry(11, 21);
    umid = umid

    drawPair(223, 116, "GERAL", "{0:0.0f} C".format(temp))
    drawPair(223, 150, "UMIDADE", "{0:0.0f} %".format(umid))
    
def drawImages(prefix):
    global frame_black
    global frame_red

    # Exibe as imagens
    frame_black = epd.get_frame_buffer(Image.open('images/' + prefix + '-black.bmp'))
    frame_red = epd.get_frame_buffer(Image.open('images/' + prefix + '-red.bmp'))

    # Rotaciona o frame buffer igual as imagens
    epd.set_rotate(epd2in7b.ROTATE_270);

    ftitle = ImageFont.truetype('fonts/Ubuntu-B.ttf', 24)
    epd.draw_string_at(frame_black, 30, 6, "SLARTIBARTFAST", ftitle, UNCOLORED)

    
def main():
    global epd
    global fval
    global fvalsm
    global fcapt

    # EPD
    epd = epd2in7b.EPD()
    epd.init()

    # Fonts
    fval = ImageFont.truetype('fonts/UbuntuMono-R.ttf', 11)
    fvalsm = ImageFont.truetype('fonts/UbuntuMono-R.ttf', 10)
    fcapt = ImageFont.truetype('fonts/Ubuntu-B.ttf', 8)


    printer_status = getPrinterStatus()

    if (printer_status == None):
        desconectada()
    elif (printer_status['state']['flags']['printing']):
        imprimindo(printer_status)
    else:
        pronta(printer_status)

    # Envia para a tela
    epd.display_frame(frame_black, frame_red)


def desconectada():
    drawImages('desconectada')
    drawSensors1()
    drawSensors2()

def pronta(printer_status):
    drawImages('pronta')
    drawSensors1(printer_status)
    drawSensors2()

def formatTime(seconds):
    ret = ''
    minutos, segundos = divmod(seconds, 60)
    horas, minutos = divmod(minutos, 60)
    if (horas > 0):
        ret = "{0:0.0f}h ".format(horas)
    if (minutos > 0):
        ret += "{0:0.0f}m ".format(minutos)
    return ret

def imprimindo(printer_status):

    fporc = ImageFont.truetype('fonts/UbuntuMono-B.ttf', 26)
    fporc2 = ImageFont.truetype('fonts/Ubuntu-B.ttf', 10)

    job_info = getJobInfo()

    status = printer_status['state']['text']
    progress = job_info['progress']['completion']
    step = int(round(progress/11))
    arquivo = job_info['job']['file']['display'][:28]
    transcorrido = job_info['progress']['printTime']
    restante = job_info['progress']['printTimeLeft']
    eta = datetime.datetime.now() + datetime.timedelta(seconds=restante)

    drawImages('imprimindo-{}'.format(step))
    drawPair(28, 48, "STATUS", status)
    drawPair(28, 82, "ETA", eta.strftime("%H:%M"))
    drawPair(28, 116, "ARQUIVO", arquivo, font=fvalsm)
    drawPair(28, 150, "TRANSCORRIDO", formatTime(transcorrido))
    drawPair(105, 150, "RESTANTE", formatTime(restante).rjust(10), x2=117)

    epd.draw_string_at(frame_black, 120, 64, "{0:0.0f}".format(progress).rjust(2, '0'), fporc, COLORED)
    epd.draw_string_at(frame_red, 145, 74, "%", fporc2, COLORED)

    drawSensors1(printer_status)
    drawSensors2()


if __name__ == '__main__':
    main()
