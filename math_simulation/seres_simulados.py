import random
import threading
from constantes import *


class Seres_simulados: 
    def __init__(self, genes:str, tempo_vida:int , prob_rep:int) -> None:
        self.genes = genes
        self.tempo = tempo_vida
        self.prob_rep = prob_rep
        self.vivo = True 
        self.def_carac()
        self.posy = random.randrange(0,HEIGHT)
        self.posx = random.randrange(0, WIDTH)
        self.vx = random.randrange(-SPEED,SPEED)
        self.vy = random.randrange(-SPEED,SPEED)
        self.timer = threading.Timer(self.tempo, self._morte)
        self.timer.start()

    def _morte(self):
        self.vivo = False

    def def_carac(self):
        if self.genes == "aa":
            self.tipo = 0
        elif self.genes == "AA":
            self.tipo = 1
        else:
            self.tipo = 1

    def mover_ser(self):
        self.posx += self.vx
        self.posy += self.vy
        if self.posx >= 900 or self.posx <= 0:
            self.vx *= -1
        if self.posy >= 900 or self.posy <= 0:
            self.vy *= -1
            
class Populacao_simulada:
    def __init__(self, N_total_dom:int, N_hibrido:int, N_recessivo:int, prob_dom:int, 
                 prob_rec:int, tempo_vida_dom:int, tempo_vida_rec:int) -> None:
        self.N_total_dom = N_total_dom
        self.N_hibrido = N_hibrido
        self.N_recessivo = N_recessivo
        self.populacao_total = N_total_dom + N_hibrido + N_recessivo
        self.tempo_vida_dom = tempo_vida_dom
        self.tempo_vida_rec = tempo_vida_rec
        self.prob_rec = prob_rec
        self.prob_dom = prob_dom
        self.cria_populacao(prob_dom, prob_rec, tempo_vida_dom, tempo_vida_rec)
    
    def cria_populacao(self, prob_dom:int, prob_rec:int, tempo_vida_dom:int, tempo_vida_rec:int):
        self.populacao = []
        for i in range(self.N_total_dom):
            self.populacao.append(Seres_simulados("AA", tempo_vida_dom, prob_dom))
        for i in range(self.N_hibrido):
            self.populacao.append(Seres_simulados("Aa", tempo_vida_dom, prob_dom))
        for i in range(self.N_recessivo):
            self.populacao.append(Seres_simulados("aa", tempo_vida_rec, prob_rec))

    def mover_populacao(self):
        for i in range(len(self.populacao)):
            self.populacao[i].mover_ser()

    def colisao(self, ser1:Seres_simulados, ser2:Seres_simulados):
        return (ser1.posx < ser2.posx and ser2.posx < ser1.posx + 6) and (ser1.posy < ser2.posy and ser2.posy < ser1.posy + 6)

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

    def checar_relacao(self):
        for i in range(len(self.populacao)):
            for j in range(i + 1,len(self.populacao)):
                if self.colisao(self.populacao[i], self.populacao[j]):
                    x = random.randrange(1,10) 
                    if x <= min(self.populacao[i].prob_rep, self.populacao[j].prob_rep):
                        self.reproducao(self.populacao[i], self.populacao[j])

    def reproducao(self, ser1:Seres_simulados, ser2:Seres_simulados):
        x = ser1.genes[random.randrange(0,1)] + ser2.genes[random.randrange(0,1)]
        if x == "aa":
            self.populacao.append(Seres_simulados(x, self.tempo_vida_rec, self.prob_rec))
            self.N_recessivo += 1
        elif x == "AA": 
            self.populacao.append(Seres_simulados(x, self.tempo_vida_dom, self.prob_dom))
            self.N_total_dom += 1
        else:
            self.populacao.append(Seres_simulados(x, self.tempo_vida_dom, self.prob_dom))
            self.N_hibrido += 1
        self.populacao_total += 1
        
    def simulacao(self):
        self.mover_populacao()
        self.checar_relacao()
        self.matar()
