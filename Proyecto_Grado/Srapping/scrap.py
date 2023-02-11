from bs4 import BeautifulSoup
import requests
import pandas as pd
from random import randint
from time import sleep

def escribir_archivo(denom, lista, categoria):
    df = pd.DataFrame()
    nueva_linea = list()
    columnas = list()
    columnas.append(["codigo_cuoc_2022", categoria])
    for i in lista:
        nueva_linea.append([denom, i])
        df = pd.DataFrame(nueva_linea)
    df.columns = columnas
    df.to_csv(categoria+'.csv', mode='a', sep=';',index=False, header=False, encoding="utf-8")

df = pd.read_csv("https://raw.githubusercontent.com/claudiamarcelacaro/Maestria_IA/main/Proyecto_Grado/CUOC-indice-clasificacion-unica-ocupaciones-colombia-2022.csv", sep=';', encoding = "utf-8")

for denom in df['codigo_cuoc_2022']:
    if len(denom) == 5 and int(denom) >= 33330:
        url = f'https://ocupacol.mintrabajo.gov.co/Profile/OccupationalProfile/{denom}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        print(url)

        if soup.find_all('div', id='notfound'):
            print('No tiene contenido')
        else:
            # cuoc_funciones
            func = soup.find_all('div', id='profilebox3')
            funciones = list()

            for i in func:
                func1 = i.text.split('\n')
                for i1 in func1:
                    if i1.replace('\r', '').strip() != '':
                        funciones.append(i1.replace('\r', '').strip())

            if len(funciones) > 0:
                categoria = "funciones"
                escribir_archivo(denom, funciones, categoria)

            # cuoc_destrezas
            destr = soup.find_all('div', class_='col-lg-6 cardDestrezas')
            destrezas = list()

            for i in destr:
                destr1 = i.find_all("span", {"class": "badge badge-primary badge-inpar"})
                for i1 in destr1:
                    destrezas.append(i1.text.replace('\r\n', '').strip())

            if len(destrezas) > 0:
                categoria = "destrezas"
                escribir_archivo(denom, destrezas, categoria)

            # cuoc_ocupaciones_afines
            ocup = soup.find_all('div', class_='afines body-standard text-justify')
            ocupaciones = list()

            for i in ocup:
                ocup1 = i.find_all("a", {"class": "relatedOccupations"})
                for i1 in ocup1:
                    ocupaciones.append(i1.text.replace('\r\n', '').strip())

            if len(ocupaciones) > 0:
                categoria = "ocupaciones"
                escribir_archivo(denom, ocupaciones, categoria)

            # cuoc_conocimientos
            conoc = soup.find_all('div', class_='card card-margin cardDestrezas')
            conocimientos = list()

            for i in conoc:
                conoc1 = i.find_all("span", {"class": "badge badge-primary badge-par"})
                for i1 in conoc1:
                    conocimientos.append(i1.text.replace('\r\n', '').strip())

            if len(conocimientos) > 0:
                categoria = "conocimientos"
                escribir_archivo(denom, conocimientos, categoria)

            # cuoc_denom_ocup
            denocu = soup.find_all('ul', class_='ul-denominaciones text-justify')
            denom_ocupa = list()

            for i in denocu:
                denocu1 = i.find_all("li", {"class": "li-denominaciones"})
                for i1 in denocu1:
                    denom_ocupa.append(i1.text.replace('\r\n', '').strip())

            if len(denom_ocupa) > 0:
                categoria = "denominaciones_ocupacionales"
                escribir_archivo(denom, denom_ocupa, categoria)

            # cuoc_area_cualificacion
            cuali = soup.find_all('div', class_='card card-margin qualifications')
            cualificacion = list()

            for i in cuali:
                cuali1 = i.find_all("div", {"class": "denominaciones"})
                for i1 in cuali1:
                    cuali2 = i1.text.split('\n')
                    for i2 in cuali2:
                        if i2.replace('\r', '').strip() != '':
                            cualificacion.append(i2.replace('\r', '').strip())

            if len(cualificacion) > 0:
                categoria = "cualificacion"
                escribir_archivo(denom, cualificacion, categoria)

        sleep(randint(1, 5))


