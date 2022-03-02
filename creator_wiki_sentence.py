from random import randint
import requests
from bs4 import BeautifulSoup
class CreatorSent:

    def text_get():
        s = randint(1, 7)
        step_fin = 0
        step_st = 0
        lenght = 100
        req = requests.get(f'https://ilibrary.ru/text/1146/p.{s}/index.html')
        root = BeautifulSoup(req.content, 'html.parser')
        shift = randint(0, len(root.text) - lenght * 2)
        if not root.text[shift].istitle():
            while root.text[shift + step_st].istitle() == False:
                step_st += 1
        lenght += step_st
        while root.text[lenght + step_fin + shift] != '.':
            step_fin += 1
        return root.text[shift + step_st:shift + lenght + step_fin + 1].replace('\n', '')

