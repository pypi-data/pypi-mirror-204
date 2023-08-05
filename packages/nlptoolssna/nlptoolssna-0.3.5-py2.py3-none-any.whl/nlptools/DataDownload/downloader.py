import os
import sys
from pathlib import Path
import requests  
import zipfile
from tqdm import tqdm

urls = {
    'morph':'https://portal.sina.birzeit.edu/20230418test27012000.pickle',
    'ner': 'http://portal.sina.birzeit.edu/867530901NED20230418modelv28.zip',
    'salma': 'http://portal.sina.birzeit.edu/98765432128.zip',
    'salma2021': 'http://portal.sina.birzeit.edu/98765432128_02_22_May_2021.zip'
}

def get_appdatadir():
    home = str(Path.home())

    if 'google.colab' in sys.modules:
        return Path('/content/nlptools')
    elif sys.platform == 'win32':
        return Path(home, 'AppData/Roaming/nlptools')
    elif sys.platform == 'darwin':
        return Path(home, 'Library/Application Support/nlptools')
    else:
        return Path(home, '.nlptools')



def download_file(url='https://github.com/eng-aomar/ts/raw/main/my_data.pickle', dest_path=get_appdatadir()):
    filename = os.path.basename(url)
    file_path = os.path.join(dest_path, filename)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # NOTE the stream=True parameter below
    try:
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                total_size = int(r.headers.get('content-length', 0))
                block_size = 8192
                progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
                for chunk in r.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
                progress_bar.close()

        # Extract zip file if downloaded file is a zip
        if zipfile.is_zipfile(file_path):
            extracted_folder_name = os.path.splitext(file_path)[0]
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                zip_file.extractall(extracted_folder_name)
            os.remove(file_path)
        
        return file_path

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f'Error 403: Forbidden. The requested file url {url} could not be downloaded due to insufficient permissions. Please check the URL and try again.')
        else:
            print('An error occurred while downloading the file:', e)


def download_files():
    for url in urls.values():
        download_file(url)





#download_file(downloadLink ,_get_appdatadir())