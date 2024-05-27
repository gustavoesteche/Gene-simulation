import random
import pygame
import threading
from constantes import *


class Seres: 
    def __init__(self, genes:str, tempo_vida:int , prob_rep:int, win1) -> None:
        self. genes = genes
        self.tempo = tempo_vida
        self.prob_rep = prob_rep
        self.vivo = True 
        self.def_carac()

        # características para a simulação visual 
        self.posy = random.randrange(0,HEIGHT)
        self.posx = random.randrange(0, WIDTH)
        self.vx = random.randrange(-SPEED,SPEED)
        self.vy = random.randrange(-SPEED,SPEED)
        self.rect_def()
        self.win = win1
        self.timer = threading.Timer(self.tempo, self._morte)
        self.timer.start()

    def _morte(self):
        self.vivo = False

    def rect_def(self):
        if self.tipo == 1:
            self.rect_image = pygame.image.load("visual_simulation\index.png")
            self.rect_image = pygame.transform.scale(self.rect_image, (6, 6))
            self.rect = self.rect_image.get_rect(topleft = (self.posx, self.posy))
        else:
            self.rect_image = pygame.image.load("visual_simulation\index (cópia).png")
            self.rect_image = pygame.transform.scale(self.rect_image, (6, 6))
            self.rect = self.rect_image.get_rect(topleft = (self.posx, self.posy))

    def def_carac(self):
        if self.genes == "aa":
            self.tipo = 0
            self.cor =  BLUE

        elif self.genes == "AA":
            self.tipo = 1
            self.cor = RED
        else:
            self.tipo = 1
            self.cor = PURPLE
        
    def desenhar_ser(self):
        pygame.draw.rect(self.win, self.cor, self.rect)

    def mover_ser(self):
        self.rect = self.rect.move(self.vx, self.vy)
        self.posx = self.rect.x
        self.posy = self.rect.y
        if self.posx >= 900 or self.posx <= 0:
            self.vx *= -1
        if self.posy >= 900 or self.posy <= 0:
            self.vy *= -1
            
class Populacao:
    def __init__(self, N_total_dom:int, N_hibrido:int, N_recessivo:int, prob_dom:int, 
                 prob_rec:int, tempo_vida_dom:int, tempo_vida_rec:int, win1 = None) -> None:
        self.N_total_dom = N_total_dom
        self.N_hibrido = N_hibrido
        self.N_recessivo = N_recessivo
        self.populacao_total = N_total_dom + N_hibrido + N_recessivo
        self.tempo_vida_dom = tempo_vida_dom
        self.tempo_vida_rec = tempo_vida_rec
        self.prob_rec = prob_rec
        self.prob_dom = prob_dom
        self.cria_populacao(prob_dom, prob_rec, tempo_vida_dom, tempo_vida_rec, win1)
        self.win = win1
    
    def cria_populacao(self, prob_dom, prob_rec, tempo_vida_dom, tempo_vida_rec, win1):
        self.populacao = []
        for i in range(self.N_total_dom):
            self.populacao.append(Seres("AA", tempo_vida_dom, prob_dom, win1))
        for i in range(self.N_hibrido):
            self.populacao.append(Seres("Aa", tempo_vida_dom, prob_dom, win1))
        for i in range(self.N_recessivo):
            self.populacao.append(Seres("aa", tempo_vida_rec, prob_rec, win1))

    def mover_desenhar(self):
        for i in range(len(self.populacao)):
            self.populacao[i].mover_ser()
            self.populacao[i].desenhar_ser()

    def matar(self):
        for ser in self.populacao:
            if ser.vivo == False:
                self.populacao.remove(ser)
                if ser.genes == "AA":
                    self.N_total_dom -= 1
                elif ser.genes == "aa":
                    self.N_recessivo -= 1
                else:
                    self.N_hibrido -= 1
                self.populacao_total -= 1

    def checar_sexo(self):
        for i in range(len(self.populacao)):
            for j in range(i + 1,len(self.populacao)):
                if self.populacao[i].rect.colliderect(self.populacao[j].rect):
                    x = random.randrange(1,10) 
                    if x <= min(self.populacao[i].prob_rep, self.populacao[j].prob_rep):
                        self.reproducao(self.populacao[i], self.populacao[j])

    def reproducao(self, ser1:Seres, ser2:Seres):
        x = ser1.genes[random.randrange(0,1)] + ser2.genes[random.randrange(0,1)]
        if x == "aa":
            self.populacao.append(Seres(x, self.tempo_vida_rec, self.prob_rec,self.win))
            self.N_recessivo += 1
        elif x == "AA": 
            self.populacao.append(Seres(x, self.tempo_vida_dom, self.prob_dom,self.win))
            self.N_total_dom += 1
        else:
            self.populacao.append(Seres(x, self.tempo_vida_dom, self.prob_dom,self.win))
            self.N_hibrido += 1
        self.populacao_total += 1

    def simulacao(self):
        self.mover_desenhar()
        self.checar_sexo()
        self.matar()
