import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def monta_linha(year, raw: dict):
    key = list(raw.keys())[0]
    values = raw.get(key)

    return [year, key, values[0], int(values[1])]

def trata_valor(text, contagem_amostra=None):
    trata_valores =lambda x: [ v.strip().replace(',','') for v in x.split('\n') if v]
    valores = trata_valores(text)
    matches = [x for x in re.findall( r'\d+\.\d+|\d+',"".join(valores))]
    percent, value = 0, 0
    if matches:
        percent = float(matches[0])
    try:
        value = float(matches[1])
    except Exception as ex:
        if contagem_amostra:
            contagem = re.findall(r'\d+', contagem_amostra.replace(',',''))
            if contagem:
                value = int((float(contagem[0]) * percent) / 100)
    
    return [percent, value] 


def captura_valores(table, contagem_amostra=None):
    trata_label = lambda x: "".join([l.strip() for l in x.split('\n') if l])
    return [{trata_label(tr.find("td", class_="label").text) : trata_valor(tr.find("td", class_="bar").text, contagem_amostra)} 
                for tr in table.find_all("tr")]

def request_survey(year):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
    resp = requests.get(f'https://survey.stackoverflow.co/{year}/', headers=headers)
    if resp.status_code == 200:
        site = BeautifulSoup(resp.text, "html.parser")
        tables = site.find_all("table", id=re.compile("^language"))
        if tables:
            valores = captura_valores(table=tables[0])
            return [monta_linha(year, valor) for valor in valores]
        else:
            artc = site.find_all("article", id="technology-programming-scripting-and-markup-languages")
            div = site.find_all("div", id=re.compile("^technology-programming"))
            span = artc[0].find_all("span", class_="ps-absolute")        
            tables = div[0].find_all('table')
            valores = captura_valores(table=tables[0], contagem_amostra=span[0].text)
            return [monta_linha(year, valor) for valor in valores]



if __name__ == '__main__':
    valores = []
    for year in range(2020,2024):
        valores.extend(request_survey(year))

    df = pd.DataFrame(valores, columns=["ano", "linguagem", "percental", "valor"])
    df.to_csv("stackoverflow.csv", index=False)

