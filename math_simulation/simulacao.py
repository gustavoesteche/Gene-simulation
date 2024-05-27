from time import sleep
from seres_simulados import Populacao_simulada
from constantes import *

def main():

    total_data = {}
    for i in range(1, 10000):    
        populacao = Populacao_simulada(N_total_dom=15, N_hibrido=15, N_recessivo=15, prob_dom=6, 
                          prob_rec=10, tempo_vida_dom=10, tempo_vida_rec=10)
        geracao = 0
        run = True
        num_experimento = i
        
        data = {}
        while run:
            populacao.simulacao()
            if geracao % 20 == 0:
                data[geracao//20] = populacao.N_total_dom,populacao.N_hibrido,populacao.N_recessivo,populacao.populacao_total
            geracao += 1
            if populacao.populacao_total == 0 or geracao == 1000:
                run = False
        
        total_data[num_experimento] = data
        print(i)
    
    with open("math_simulation\data.txt", "a") as f:
        f.write(str(total_data))

main()
