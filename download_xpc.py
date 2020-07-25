import os 
from urllib.parse import urlsplit
import pandas as pd
import requests
def download_xpc():
        df = pd.read_excel('link.xlsx')
        covers = df['cover']
        if not os.path.exists('images'):
            os.mkdir('images')
        for url in covers:
            fname = urlsplit(url).path.split('/')[-1]
            path = os.path.join(os.curdir + '\\images', fname)
            response = requests.get(url)
            with open(path, 'wb') as fp:
                for chunk in response.iter_content(1024):
                    fp.write(chunk)
    

if __name__ == '__main__':
    download_xpc()
