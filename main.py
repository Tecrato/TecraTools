import pygame as pag
import Utilidades as uti
import Utilidades_pygame as uti_pag
from platformdirs import user_cache_path
from typing import override

from Utilidades_pygame.base_app_class import Base_class
from Utilidades_pygame.config_default import Config
from Assest_downloader import AssetDownloader
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

        self.buscar_programas()

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
            self.asset_downloader.download(self.api_url+x['icono'], x['icono'].split('/')[-1])
            bloque_nuevo = uti_pag.Bloque((20,100*i), (330,80), 'topleft', border_color='white', border_width=3, border_radius=10)
            bloque_nuevo.add(uti_pag.Text(x['nombre'].capitalize(), 13, self.config.fonts["mononoki"], (10, 10), dire='top'), (190,10))
            text_split = x['descripcion'].split(' ')
            text_des = '\n'.join([' '.join(text_split[i:i+5]) for i in range(0,len(text_split),5)])
            bloque_nuevo.add(uti_pag.Text(text_des, 10, self.config.fonts["mononoki"], (180, 10), dire='left'), (80,35))
            # bloque_nuevo.add(uti_pag.Text(x['descripcion'], 10, self.config.fonts["mononoki"], (50, 10), dire='top'), (50,35))
            # print(self.carpeta_cache/(x['icono'].split('/')[-1]))
            bloque_nuevo.add(uti_pag.Image(self.carpeta_cache/(x['icono'].split('/')[-1]), (30,30), 'topleft', (59,59), always_draw=True),'(10,10)')
            self.bloque_main_programas.add(bloque_nuevo, (0,100*i +20), clicking=True)

if __name__ == "__main__":
    # 415,550
    font_mononoki = "./Data/fonts/mononoki Bold Nerd Font Complete Mono.ttf"
    config = Config(
        resolution=(350,480),
        window_resize=False,
        title="TecraTools",
        window_title="TecraTools",
        my_company="Edouard Sandoval",
        author="Edouard Sandoval",
        version="1.0.0",
        fonts={"mononoki": "./Data/fonts/mononoki Bold Nerd Font Complete Mono.ttf"},
        noframe=True
    )
    app = TecraTools(config)