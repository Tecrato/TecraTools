import Utilidades as uti


class AssetDownloader:
    def __init__(self, api_url, carpeta_cache):
        self.api_url = api_url
        self.carpeta_cache = carpeta_cache
        self.session = uti.web_tools.Http_Session(verify=False)
        
    def download(self, url, filename):
        response = self.session.get(url)
        # uti.debug_print(response.headers)
        if self.carpeta_cache.joinpath(filename).exists() and response.headers.get('Content-Length') == str(self.carpeta_cache.joinpath(filename).stat().st_size):
            return
        with open(self.carpeta_cache / filename, 'wb') as f:
            f.write(response.data)