import pygame as pg
import threading as th
import keyboard as ky
import sys, os , time

def bekle(sure):
    time.sleep(sure)

def basildi(tus:str):
    return ky.is_pressed(tus)




def carpma_listesi(nesne,diger):

    x = nesne.collidelist(diger)
    if x != -1:
        return 1
    else:    
        return 0




def dikdortgen_carp(nesne,diger):
    
    return pg.Rect.colliderect(nesne,diger)


def ses_yukle(ses):
    pg.mixer.music.load(ses)



def ses_cal():
    pg.mixer.music.play()


def s_duraklat():
    pg.mixer.music.pause()



def s_devam():
    pg.mixer.music.unpause()



def s_durdur():
    pg.mixer.stop()


pg.init()



class Turk_rect:
    def __init__(self,ozellik):
        self.rect = pg.rect.Rect(ozellik[0:2],ozellik[2:])
    
    def carp(self,diger,carpma_tip):
        return carpma_tip(self.rect,diger)
            
    def guncelle(self,ozellik):
        self.rect = pg.rect.Rect(ozellik[0:2],ozellik[2:])



class Turk_resim:
    def __init__(self,resim,boyut:list):
        self.resim = pg.transform.scale(pg.image.load(resim),boyut)
    def guncelle(self,resim,boyut:list):
        self.resim = pg.transform.scale(pg.image.load(resim),boyut)
        

    
class EKRAN:
    def __init__(self,x:int,y:int,baslik:str,ikon:str):
        if not ikon == "":
            self.ikon = pg.transform.scale(pg.image.load(ikon),(320,320))
            pg.display.set_icon(self.ikon)
        pg.display.set_caption(str(baslik))
        self.___ekran___ = pg.display.set_mode((x,y))
        self.running = True  # running özelliğini tanımla
        #self.dongu(normal_islem,event_islem,kapandi_islem,yenileme_cesidi)

    def yerlestir(self,nesne):
        if type(nesne[0]) == Turk_resim:
            self.___ekran___.blit(nesne[0].resim,(nesne[1],nesne[2]))
        else:
            self.___ekran___.blit(nesne[0],(nesne[1],nesne[2]))

    def ciz(self,nesne:Turk_rect,renk):
        pg.draw.rect(self.___ekran___,renk,nesne.rect)

    def update(self):
        pg.display.update()

    def flip(self):
        pg.display.flip()
        
    def dongu(self,normal_islem,event_islem,kapandi_islem,yenileme_cesidi):
        self.running = True
        while self.running:  # self.running özelliğini kullan
            self.events = pg.event.get()
            for self.event in self.events:
                if self.event.type == pg.QUIT:
                    kapandi_islem()
                    self.running = False

                event_islem()
            
            normal_islem()
            yenileme_cesidi()

        pg.quit()
        sys.exit()