import Utilidades as uti

from pathlib import Path


class AssetDownloader:
    def __init__(self, api_url, carpeta_cache):
        self.api_url = api_url
        self.carpeta_cache: Path = carpeta_cache
        self.session = uti.web_tools.Http_Session(verify=False)
        
    def download(self, url, filename):
        response = self.session.get(url)
        # uti.debug_print(response.headers)
        if self.carpeta_cache.joinpath(filename).exists() and response.headers.get('Content-Length') == str(self.carpeta_cache.joinpath(filename).stat().st_size):
            uti.debug_print('File already downloaded')
            return self.carpeta_cache / filename
        with open(self.carpeta_cache / filename, 'wb') as f:
            f.write(response.data)
        uti.debug_print('File downloaded', self.carpeta_cache / filename)
        return self.carpeta_cache / filename