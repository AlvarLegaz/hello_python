# -*- coding: utf-8 -*-
"""
WebScraping: obtener datos de páginas webs

Librerias necesarias:
   pip install bs4 (beautifulsoup4)

Created on Tue Aug  3 14:48:30 2021

@author: ALegaz
"""

import urllib.request,unicodedata
from bs4 import BeautifulSoup

datos = urllib.request.urlopen('https://demanda.ree.es/visiona/peninsula/demanda/total').read()
soup = BeautifulSoup(datos)

table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="ctl00_Contenido_tblAcciones") 

#!rows = table.findAll(lambda tag: tag.name=='tr')
column = table.findAll(lambda tag: tag.name=='td')


def getCellDataValue(cell):
    ini=cell.find(">")
    fin=cell.find("</td>")
    return cell[ini+1:fin]

def getCellDataName(cell):
    fin=cell.find("</td>")
    return cell[96:fin-4]

paso = 9
for i in range(0,len(column),paso):
    print("pos "+getCellDataName(str(column[i+0]))+" = "+getCellDataValue(str(column[i+2]))+"\n")

