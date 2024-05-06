"""
Este arquivo realiza a conversão de uma estrutura de rede neural (classificação
ou regressão) gerada em python para uma versão adequada com a linguagem de 
'texto estruturado' usado no software de programação 800xA da ABB. O intuito é
agilizar o trabalho de engenheiros na implementação de redes neurais em ambiente
industrial. 

Este arquivo foi formulado considerando a sintaxe de redes neurais geradas em
python via biblioteca 'scikit-learn' que contenham um neurônio na camada entrada
e saída e múltiplas camadas ocultas com múltiplos neurônios. Portanto, redes
neurais que não cumpram estes requisitos podem não ser corretamente convertidas.

Uma breve descrição do funcionamento do código:
    
    Um arquivo .txt contendo informções da rede neural gerada deve ser salvo no
    mesmo diretório que este arquivo. Para gerar o arquivo .txt contendo tais
    informações, sugerimos copiar o código abaixo ao final do arquivo do usuário
    criado para gerar a rede neural. 

"""

import re
from Funcoes import dicionario_rede, escrever_no_arquivo

# -------- Input neural network information --------            

# -------- Validation of the existence of the .txt file in the folder
while True:
    original_name = input('Source file name: ')
    arquivo_rede = original_name + '.txt'

    try:
        # -------- Criando aquivo tabela e arquivo de destino -------- 
        arquivo_tabela = original_name + '_table' + '.txt'
        arquivo_escrito = original_name + '_800xA' + '.txt'
        with open(arquivo_rede, 'rb') as original:
            with open(arquivo_escrito, 'wb') as destiny:
                destiny.write(original.read())
            break    

    except FileNotFoundError:
        print(f"ATTENTION!\n The file {arquivo_rede} does not exist in this folder. Please enter the original file name again.\ndf")

rede_neural, camadas = dicionario_rede(arquivo_rede) #exportando as informações da rede neural do dicionário

with open(arquivo_escrito, 'w') as arquivo: 
    arquivo.write('(*As variáveis estão no formato Nij, onde i significa o número da camada e j significa o número do neurônio*)\n')

with open (arquivo_rede, 'r') as arquivo:
    linhas = arquivo.readlines()
    for linha in linhas:
        activation_function = linhas[1].split(":")[1].strip() ## Função de ativação geral
        out_activation_function = linhas[2].split(":")[1].strip() ## Função de ativação da camada de saída
        num_entradas = int(linhas[3].split(":")[1].strip()) ## Número de neurônios na camada de entrada

# -------- Construção da tabela de variáveis --------  
vetor_entrada = []
with open(arquivo_tabela, 'w') as arquivo:
    arquivo.write('Parametros:\n')
    for i in range(num_entradas):
        resposta = input(f"Digite a variável de entrada {i+1}: ")
        linha = f'{resposta}\treal\t\tin\tyes\n'
        arquivo.write(linha)
        vetor_entrada.append(resposta)
        
    variavel_saida = input("Digite a variável de saída: ")
    arquivo.write(f'{variavel_saida}\treal\t\tout\tyes\n')
    
vetor_tamanhos = []
for i in range(1, rede_neural['Número de camadas'] - 1):
    camada = camadas[i]
    neuronios = camada['Neurônios']
    vetor_tamanhos.append(len(neuronios))
vetor_tamanhos.append(1) 

## função para escrever no arquivo:
vetor_procurar, vetor_de_biases, vetor_saidas, neuronios_utilizados = escrever_no_arquivo(camadas, vetor_tamanhos, vetor_entrada, arquivo_escrito, rede_neural, activation_function, out_activation_function)

with open(arquivo_escrito, 'r') as arquivo_leitura:
        linhas = arquivo_leitura.readlines()
for indice, bias_value in zip(vetor_procurar, vetor_de_biases):
    for i, linha in enumerate(linhas):
        if indice in linha:
            linhas[i] = f"{linha.strip()}) + {bias_value}; \n"
with open(arquivo_escrito, 'w') as arquivo_escrita:
    arquivo_escrita.writelines(linhas)

with open(arquivo_tabela, 'a') as arquivo:
    arquivo.write('\nVariaveis:\n')
    for variavel, saida in zip(vetor_procurar, vetor_saidas):
        linha = f'{variavel.strip()}\treal\tretain\n'
        arquivo.write(linha)
        linha_saida = f'{saida.strip()}\treal\tretain\n'
        arquivo.write(linha_saida)
with open(arquivo_tabela, 'r') as arquivo:
    linhas = arquivo.readlines()
with open(arquivo_tabela, 'w') as arquivo:
    arquivo.writelines(linhas[:-1]) 

with open(arquivo_escrito, 'r') as arquivo:
    linhas = arquivo.readlines()
padrao = re.compile(rf'^{re.escape(vetor_saidas[-1])}\b')
for i, linha in enumerate(linhas):
    if padrao.match(linha):
        linhas[i] = padrao.sub(variavel_saida, linha)
with open(arquivo_escrito, 'w') as arquivo:
    arquivo.writelines(linhas)