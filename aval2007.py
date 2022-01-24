#%%
import re
import pandas as pd
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

#%%
BASE_URL = "https://www.fct.pt/apoios/unidades/avaliacoes/2007/"

#%%
def parse_resultados():
    get = requests.get(BASE_URL + "resultados.phtml.pt")
    soup = BeautifulSoup(get.content, 'lxml')
    areas = {area.text.strip(): BASE_URL + area['href'] for area in soup.select('div#relatorio ul li ul li a')}
    return areas

def parse_areas(areas_dict: dict):
    data = []
    for area in tqdm(areas_dict):
        for centro in tqdm(parse_area(areas_dict[area], area)):
            data.append(centro)

    data = pd.DataFrame(data).set_index('codigo_centro')
    data.to_csv('fct_aval2007.csv')

def parse_area(area_url: str, area_name: str):
    get = requests.get(area_url.replace('areas', 'areas.phtml.pt'))
    area = BeautifulSoup(get.content, 'lxml')
    for centro in area.select('div#relatorio ul li'):
        yield parse_centro(centro)

def parse_centro(centro):
    centro_dict = dict()
    centro_dict['nome_centro'] = centro.select_one('h5 a').text
    centro_dict['codigo_centro'] = centro.select_one('h5 span').text[1:-1]
    keys = ['coord', 'instit', 'website', 'nr_inv', 'nr_phd', 'nr_phd_int', 'nr_grupos', 'aval_2007']
    for k, v in zip(keys, centro.select('p em')):
        centro_dict[k] = v.text.strip()
    return centro_dict

def main():
    areas = parse_resultados()
    parse_areas(areas)

#%%
if __name__ == '__main__':
    main()
# %%
