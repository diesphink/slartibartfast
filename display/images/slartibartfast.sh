#!/bin/bash

IMAGEM="imprimindo-8"

sed 's/#ffffff/#000000/g' slartibartfast.svg > slartibartfast-red.svg
inkscape slartibartfast-red.svg --export-png=slartibartfast-red.png
convert +dither -type bilevel slartibartfast-red.png slartibartfast.bmp
convert -negate -rotate "270" slartibartfast.bmp ${IMAGEM}-red.bmp

sed 's/#ffffff/#ff0000/g' slartibartfast.svg > slartibartfast-black.svg
inkscape slartibartfast-black.svg --export-png=slartibartfast-black.png
convert +dither -type bilevel slartibartfast-black.png slartibartfast.bmp
convert -negate -rotate "270" slartibartfast.bmp ${IMAGEM}-black.bmp

scp ${IMAGEM}*.bmp pi@192.168.0.6:slartibartfast/
#ssh pi@192.168.0.6 "cd slartibartfast;python main.py"
