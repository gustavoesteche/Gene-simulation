import pygame
from time import sleep
from seres import Seres, Populacao
from constantes import *

WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("simulação de genes")


def main():
    populacao = Populacao(N_total_dom=15, N_hibrido=15, N_recessivo=15, prob_dom=6, 
                          prob_rec=10, tempo_vida_dom=10, tempo_vida_rec=10, win1=WIN)
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WIN.fill((0,0,0))
        populacao.simulacao()
        
        pygame.display.update()

    pygame.quit()

main()
