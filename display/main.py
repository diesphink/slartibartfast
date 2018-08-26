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
import os


COLORED = 1
UNCOLORED = 0

API_TOKEN = '5CB95DC15E4D4BAEB770F304A3987196'
API_URL_BASE = 'http://localhost/'
API_PRINTER_URL = 'api/printer'
API_JOB_URL = 'api/job'


class Display(object):
    """ Class for the printer/environment info """

    STATUS_DISCONNECTED = 0
    STATUS_READY = 1
    STATUS_PRINTING = 2

    def __init__(self):

        # EPD
        self.epd = epd2in7b.EPD()
        self.epd.init()

        self.last_drawn = None
        self.big_change = False
        self._status = None
        self._status_text = None
        self._progress = None

        # Fonts
        self.fporc = ImageFont.truetype('fonts/UbuntuMono-B.ttf', 26)
        self.fporc2 = ImageFont.truetype('fonts/Ubuntu-B.ttf', 10)
        self.fval = ImageFont.truetype('fonts/UbuntuMono-R.ttf', 11)
        self.fvalsm = ImageFont.truetype('fonts/UbuntuMono-R.ttf', 10)
        self.fcapt = ImageFont.truetype('fonts/Ubuntu-B.ttf', 8)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if (value != self._status):
            self.big_change = True
            self._status = value
            self.log('** Status changed')

    @property
    def status_text(self):
        return self._status_text

    @status_text.setter
    def status_text(self, value):
        if (value != self._status_text):
            self.big_change = True
            self._status_text = value
            self.log('** Status Text changed')

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if (self._progress == None or int(round(value)) != int(round(self._progress))):
            self.big_change = True
            self.log('** Progress changed')
        self._progress = value

    def refresh(self):
        self.log('Refreshing...')
        self.refreshSensors()
        self.refreshPrinterStatus()
        self.draw()

    def refreshSensors(self):
        self.log('  - Sensors')
        # Efetua a leitura do sensor
        self.umidity, self.temperature = Adafruit_DHT.read_retry(11, 21);

    def refreshPrinterStatus(self):
        self.log('  - Printer Status')
        printer_status = self.octoprintGet(API_PRINTER_URL)
        
        if printer_status == None:
            self.status = Display.STATUS_DISCONNECTED
            self.extruder = None
            self.bed = None
        else:
            self.extruder = printer_status['temperature']['tool0']['actual']
            self.bed = printer_status['temperature']['bed']['actual']
            self.status_text = printer_status['state']['text']

            if (not printer_status['state']['flags']['printing']):
                self.status = Display.STATUS_READY
            else:
                self.status = Display.STATUS_PRINTING
                self.refreshJobStatus()

    def refreshJobStatus(self):
        self.log('  - Job Status')
        job_info = self.octoprintGet(API_JOB_URL)

        self.progress = job_info['progress']['completion']
        self.step = int(self.progress/11)
        self.file = job_info['job']['file']['display'][:28]
        self.printTime = job_info['progress']['printTime']
        self.printTimeLeft = job_info['progress']['printTimeLeft']
        self.eta = datetime.datetime.now() + datetime.timedelta(seconds=self.printTimeLeft)

    def draw(self):
        # Vai desenhar se um dos seguintes:

        # 1) Nunca desenhou
        will_draw = self.last_drawn == None

        # 2) Tem alteração grande
        will_draw = will_draw or self.big_change

        # 3) Já faz 1 minuto que desenhou da última vez e está imprimindo
        will_draw = will_draw or ((datetime.datetime.now() - self.last_drawn).seconds > 60 and self.status == Display.STATUS_PRINTING)

        # 4) Já faz 30 minutos que desenhou da última vez
        will_draw = will_draw or (datetime.datetime.now() - self.last_drawn).seconds > 30 * 60

        if (not will_draw):
            self.log('Skipping drawing...')         
            return

        self.log('Drawing...')
        self.last_drawn = datetime.datetime.now()
        self.big_change = False

        if (self.status == Display.STATUS_DISCONNECTED):
            self.drawImages('desconectada')
        elif (self.status == Display.STATUS_READY):
            self.drawImages('pronta')
        else:
            self.drawImages('imprimindo-{}'.format(self.step))
            self.drawProgressInfo()
        self.drawSensors()
        
        # Envia para a tela
        self.epd.display_frame(self.frame_black, self.frame_red)
    
    def drawPair(self, x, y, caption, value, x2 = None, y2 = None, font = None):
        if (x2 == None):
            x2 = x
        if (y2 == None):
            y2 = y + 12
        if (font == None):
            font = self.fval

        self.epd.draw_string_at(self.frame_black, x, y, value, font, COLORED)
        self.epd.draw_string_at(self.frame_red, x2, y2, caption, self.fcapt, COLORED)

    def drawSensors(self):
        if (self.extruder == None):
            self.drawPair(223, 48, "EXTRUS.", "N/A")
        else:
            self.drawPair(223, 48, "EXTRUS.", u"{0:0.0f}° C".format(self.extruder))

        if (self.bed == None):
            self.drawPair(223, 82, "SUPERF.", "N/A")
        else:
            self.drawPair(223, 82, "SUPERF.", u"{0:0.0f}° C".format(self.bed))
        
        self.drawPair(223, 116, "GERAL", u"{0:0.0f}° C".format(self.temperature))
        self.drawPair(223, 150, "UMIDADE", "{0:0.0f}%".format(self.umidity))
        

    def drawImages(self, prefix):

        # Zera o rotacionamento
        self.epd.set_rotate(epd2in7b.ROTATE_0);

        # Exibe as imagens
        self.frame_black = self.epd.get_frame_buffer(Image.open('images/{}-black.bmp'.format(prefix)))
        self.frame_red = self.epd.get_frame_buffer(Image.open('images/{}-red.bmp'.format(prefix)))

        # Rotaciona o frame buffer igual as imagens
        self.epd.set_rotate(epd2in7b.ROTATE_270);

        # Exibe o título SLARTIBARTFAST
        ftitle = ImageFont.truetype('fonts/Ubuntu-B.ttf', 24)
        self.epd.draw_string_at(self.frame_black, 30, 6, "SLARTIBARTFAST", ftitle, UNCOLORED)

    def drawProgressInfo(self):

        self.drawPair(28, 48, "STATUS", self.status_text)
        self.drawPair(28, 82, "ETA", self.eta.strftime("%H:%M"))
        self.drawPair(28, 116, "ARQUIVO", self.file, font=self.fvalsm)
        self.drawPair(28, 150, "TRANSCORRIDO", self.formatTime(self.printTime))
        self.drawPair(105, 150, "RESTANTE", self.formatTime(self.printTimeLeft).rjust(10), x2=117)

        self.epd.draw_string_at(self.frame_black, 120, 64, "{0:0.0f}".format(self.progress).rjust(2, '0'), self.fporc, COLORED)
        self.epd.draw_string_at(self.frame_red, 145, 74, "%", self.fporc2, COLORED)

    def octoprintGet(self, url):
        api_url = '{}{}'.format(API_URL_BASE, url)

        headers = {'Content-Type': 'application/json', 'X-Api-Key': API_TOKEN}

        response = requests.get(api_url, headers=headers)

        if (response.status_code == 200):
            return response.json()
        else:
            return None

    def formatTime(self, seconds):
        ret = ''
        minutos, segundos = divmod(seconds, 60)
        horas, minutos = divmod(minutos, 60)
        if (horas > 0):
            ret = "{0:0.0f}h ".format(horas)
        if (minutos > 0):
            ret += "{0:0.0f}m ".format(minutos)
        return ret

    def log(self, text):
        print "[{}] {}".format(datetime.datetime.now().strftime("%H:%M:%S"), text)

def main():
    # Altera o diretório atual para o diretório do script
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    display = Display()

    while True:
        display.refresh()
        time.sleep(5)

if __name__ == '__main__':
    main()

