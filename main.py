import pygame as pag
import Utilidades as uti
import Utilidades_pygame as uti_pag
from platformdirs import user_cache_path
from typing import override

from Utilidades_pygame.base_app_class import Base_class
from Utilidades_pygame.config_default import Config
from Assest_downloader import AssetDownloader
from componentes.principal import Programa_search


class TecraTools(Base_class):
    @override
    def otras_variables(self):
        self.can_resize = False
        self.windows_screen_size = uti.win32_tools.get_screen_size()
        self.windows_moving = False
        self.last_win_pos = (0,0)
        self.api_url = "https://tecrato.pythonanywhere.com"
        

        self.carpeta_cache = user_cache_path(self.config.title, self.config.author)
        self.carpeta_cache.mkdir(parents=True, exist_ok=True)
        
        self.asset_downloader = AssetDownloader(self.api_url, self.carpeta_cache)

        self.Func_pool.add('buscar_programas', self.buscar_programas)

    @override
    def generate_objs(self):

        self.btn_close = uti_pag.Button("X", 20, self.config.fonts["mononoki"], (self.config.resolution[0], 0), padding=(20,5), border_radius=0, dire='topright', func=self.exit)

        self.text_title = uti_pag.Text("TecraTools", 20, self.config.fonts["mononoki"], (self.config.resolution[0]//2, 30), dire='top')

        self.bloque_main_programas = uti_pag.Bloque((10,50), (340,400), 'topleft')

        self.lists_screens['main']["draw"] = [
            self.text_title,
            self.btn_close,
            self.bloque_main_programas
        ]
        self.lists_screens['main']["update"] = [
            self.text_title,
            self.btn_close,
            self.bloque_main_programas,
        ]
        self.lists_screens['main']["click"] = [
            self.btn_close,
            self.bloque_main_programas,
        ]
    
    @override
    def post_init(self):
        new_pos = self.windows_screen_size[0]-self.config.resolution[0]-20, self.windows_screen_size[1]-self.config.resolution[1]-60
        uti.win32_tools.setWinPos(self.hwnd, new_pos)
        self.last_win_pos = new_pos
        uti.win32_tools.front2(self.hwnd)

        # self.buscar_programas()
        self.Func_pool.start('buscar_programas')

    @override
    def otro_evento(self, actual_screen: str, evento: pag.event.Event):
        if evento.type == pag.MOUSEBUTTONDOWN and evento.button == 1:
            self.windows_moving = True
        elif evento.type == pag.MOUSEBUTTONUP and evento.button == 1:
            self.windows_moving = False
            self.last_win_pos = uti.win32_tools.get_window_rect(self.hwnd)[:2]
        elif evento.type == pag.MOUSEMOTION:
            if self.windows_moving and pag.mouse.get_pos() != self.last_win_pos:
                self.last_win_pos = self.last_click_pos_system+(pag.Vector2(uti.win32_tools.get_cursor_pos())-self.last_click_pos_system)-self.last_click_pos
                uti.win32_tools.setWinPos(self.hwnd, (int(self.last_win_pos[0]), int(self.last_win_pos[1])))
        elif evento.type == pag.KEYDOWN and evento.key == pag.K_ESCAPE:
            self.exit()

    #Funciones del programa
    def buscar_programas(self):
        response = uti.web_tools.get(self.api_url+"/api/programs/get_all").json

        self.bloque_main_programas.clear()
        
        for i,x in enumerate(response['lista']):
            # self.asset_downloader.download(self.api_url+x['icono'], x['icono'].split('/')[-1])
            self.bloque_main_programas.add(
                Programa_search(
                    (0,100*i +20), x['icono'], x['nombre'].capitalize(), x['descripcion'], self.config.fonts["mononoki"],
                    assest_downloader=self.asset_downloader,
                    api_url=self.api_url,
                    lock=self.lock,
                    item = x
                ), 
                clicking=True
            )

if __name__ == "__main__":
    # 415,550
    font_mononoki = "./Data/fonts/mononoki Bold Nerd Font Complete Mono.ttf"
    config = Config(
        resolution=(350,480),
        window_resize=False,
        title="TecraTools",
        icon='./Data/images/Logo.ico',
        window_title="TecraTools",
        my_company="Edouard Sandoval",
        author="Edouard Sandoval",
        version="0.4.0",
        fonts={"mononoki": "./Data/fonts/mononoki Bold Nerd Font Complete Mono.ttf"},
        noframe=True
    )
    app = TecraTools(config)