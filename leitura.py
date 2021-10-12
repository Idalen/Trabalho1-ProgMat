# Dentro de cada arquivo, estão os lucros cij. Em cada linha i estão os lucros do agente i executar a tarefa j, para i=1,...,n.

# Na pasta "insta", há arquivos nomeados "inst_1_n.txt", em que n é o número de tarefas/agentes. As demais instâncias são nomeadas "insta_u_v_n.txt", 
# em que n é o número de tarefas/agentes; u corresponde ao tipo do lucro cij (se o valor é igual 2, então o lucro está no intervalo de [5, 50]; 
# caso contrário, o valor é igual a 3 e o lucro está no intervalo de [5, 500]); v é um identificador da instância.

# Entao basicamente, para i = trabalhador e j = tarefa:
#       j0  j1  j2  j3  j4  jN
#   i0  .......................
#   i1  ........lucros.........
#   i2  ..........de...........
#   i3  .........cada..........
#   i4  .......trabalho........
#   iN  .......................

import numpy as np

# Dados sobre a formatacao dos nomes dos arquivos
pastas = ["a", "b"]
u = [2,3]
v = [1,2,3,4,5,6,7,8,9,10]
n = [50,100,200,500,1000]

# Leitura de tarefas/agentes (TALVEZ SEJA DESNECESSARIO)
# for tarefas_agentes in n: # Range para as variacoes de 50, 100, 200...
          
#     print("--------------------INICIO DE inst_"+ str(tarefas_agentes) +".txt---------------------")
            
#     # Faca a magica aqui...
#     tarefas_agentes = np.loadtxt("./insta/inst_1_"+ str(tarefas_agentes) +".txt")
            
#     print("--------------------FIM DE inst_"+ str(tarefas_agentes) +".txt------------------------")



# Leitura dos dados
for tipo_pasta in pastas: # Range para cada pasta, no caso pasta A e B
    for tipo_lucro in u: # Range para as variacoes de 2 e 3
        
        # Se tipo_lucro eh 2 entao lucro (cada item da matriz) esta no intervalo de [5, 50]
        # Se tipo_lucro eh 3 entao lucro (cada item da matriz) esta no intervalo de [5, 500]
        
        for instancia in v: # Range para as variacoes de 1,2,3,4,5...
            for tarefas_agentes in n: # Range para as variacoes de 50, 100, 200...
                print("--------------------INICIO DE inst"+tipo_pasta+"_"+str(tipo_lucro)+"_"+str(instancia)+"_"+ str(tarefas_agentes) +".txt---------------------")
                
                # Carregamento do arquivo para matriz_lida com numpy.loadtxt()
                matriz_lida = np.loadtxt("./inst"+tipo_pasta+"/inst"+tipo_pasta+"_"+str(tipo_lucro)+"_"+str(instancia)+"_"+ str(tarefas_agentes) +".txt")
                
                # Faca a magica aqui...
                # print(matriz_lida)
                
                print("--------------------FIM DE inst"+tipo_pasta+"_"+str(tipo_lucro)+"_"+str(instancia)+"_"+ str(tarefas_agentes) +".txt------------------------")
