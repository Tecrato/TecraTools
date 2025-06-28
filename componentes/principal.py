import pygame as pag
import Utilidades as uti
import Utilidades_pygame as uti_pag

from threading import Thread
import webbrowser

class Programa_search(uti_pag.Bloque):
    def __init__(
            self, pos, img, title, descripcion, font,assest_downloader=None, api_url=None, carpeta_cache=None,
            lock=None, item = None
                 ):
        super().__init__(
            pos, (330,80), 'topleft', border_color='white', border_width=3, border_radius=10,scroll_x=False,
            
        )
        self.func_to_hover = self.show_download_button
        self.func_out_hover = self.hide_download_button
        self.asset_downloader = assest_downloader
        self.api_url = api_url
        self.carpeta_cache = carpeta_cache
        self.img_path = img
        self.lock = lock
        self.title = title
        self.item = item



        self.btn_descargar = uti_pag.Button("Descargar", 10, font, (pag.Vector2(self.rect.width,2.5)-(10,0)), padding=(10,0), min_height=35, min_width=90, border_radius=10, text_aling='center', dire='topright', color='black', color_rect=(40,168,34), color_rect_active='lightgreen', func=self.download)
        self.btn_descargar.smothmove(.8,1,1.2)
        
        self.btn_seleccionar = uti_pag.Button("Seleccionar", 10, font, (pag.Vector2(self.rect.width,self.rect.height)-(10,2.5)), padding=(10,0), min_height=35, min_width=90, border_radius=10, text_aling='center', dire='bottomright', func=self.download)
        self.btn_seleccionar.smothmove(.8,1,1.2)

        self.img = uti_pag.Image('./Data/images/Logo.png', (20,20), 'topleft', (55,55), always_draw=True)

        self.add(uti_pag.Text(title, 13, font, (10, 10), dire='left'))
        self.add(uti_pag.Text(descripcion, 10, font, (85, 20), dire='topleft', text_align='left', max_width=140, wrap=True))
        self.add(self.img)

        self.add(
            self.btn_descargar,
            drawing=True,
            clicking=True
        )
        self.add(
            self.btn_seleccionar,
            drawing=True,
            clicking=True
        )
        Thread(target=self.set_img).start()

    def show_download_button(self):
        # self.btn_descargar.right = self.right-10
        ...
    
    def hide_download_button(self):
        # self.btn_descargar.pos = pag.Vector2(self.rect.width,2.5)+(200,0)
        ...

    def update_hover(self, mouse_pos: tuple=(-100000,-100000)):
        return super().update_hover(mouse_pos)

    def set_img(self):
        try:
            img = self.asset_downloader.download(self.api_url+'/'+self.img_path, self.img_path.split('/')[-1])
        except:
            return
        with self.lock:
            self.img.path = img
        
    def download(self):
        url = uti.get(self.api_url+'/api/programs',params={'program':self.item['nombre'],'version':'last'})
        webbrowser.open(url.json['url'])