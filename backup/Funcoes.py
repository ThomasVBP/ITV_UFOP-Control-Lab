########################

#Funções

########################

def dicionario_rede(arquivo_rede):
    rede_neural = {'Camadas': []}
    with open(arquivo_rede, 'r') as arquivo:
        camadas = []
        camada = None  # Inicialize camada como None
        for linha in arquivo:
            linha = linha.strip()
            if linha.startswith("Número de camadas:"):
                rede_neural['Número de camadas'] = int(linha.split(":")[1].strip())
            elif linha.startswith("Camada"):
                if camada:
                    camadas.append(camada)
                camada = {}
                camada['Neurônios'] = []
                camada['Biases'] = {}  
            elif linha.startswith("Neurônio"):
                neuronio = linha.split(":")
                valor = int(neuronio[0].split()[-1])
                camada['Neurônios'].append({'Neurônio': valor, 'Pesos': {}})
            elif linha.startswith("Peso para Neurônio"):
                partes = linha.split(":")
                neuronio = int(partes[0].split()[-1])
                peso = float(partes[1].strip())
                camada['Neurônios'][-1]['Pesos'][f'Peso para Neurônio {neuronio}'] = peso
            elif linha.startswith("Bias para Neurônio"):
                partes = linha.split(":")
                neuronio = int(partes[0].split()[-1])
                bias = float(partes[1].strip())
                camada['Biases'][f'Bias para Neurônio {neuronio}'] = bias
        if camada:  
            camadas.append(camada)
            
    rede_neural['Camadas'] = camadas
    return rede_neural, camadas

print()

########
def escrever_no_arquivo(camadas, vetor_tamanhos, vetor_entrada, arquivo_escrito, rede_neural, activation_function, out_activation_function):
    vetor_procurar = []; vetor_de_biases = []; vetor_saidas = [];
    neuronios_utilizados = set() # pra armazenar os valores de saída
    for i, camada in enumerate(rede_neural['Camadas']): # (0, numero_de_camadas):
        if i < len(rede_neural['Camadas']):
            camada = camadas[i]
            with open(arquivo_escrito, 'a') as arquivo: 
                if i == len(rede_neural['Camadas']) - 1:
                    arquivo.write('\n(*Informações de entrada e saída dos neurônios da camada de saída*)\n\n')
                    arquivo.write('(## Calculo das entradas do neurônio ##)\n\n')
                else: 
                    arquivo.write(f'\n(*Informações de entrada e saída dos neurônios da camada oculta {i+1}*)\n\n')
                    arquivo.write('(## Calculo da(s) entrada(s) do(s) neurônio(s) ##)\n\n')
            neuronios = camada['Neurônios']; biases = camada['Biases']
            novo_vetor = [0] * vetor_tamanhos[i] ##vetor com tamanho
            for x in range(len(vetor_entrada)):
                y = vetor_entrada.pop(0)            
                for j, neuronio in enumerate(neuronios):
                    if j == x:
                        pesos_do_neuronio = neuronio['Pesos']
                        for peso_key, peso_value in pesos_do_neuronio.items():
                            numero_do_neuronio = int(peso_key.split()[-1])
                            peso_value = f'{peso_value:.15f}'                   
                            if i == len(rede_neural['Camadas']):  # última camada
                                with open(arquivo_escrito, 'a') as arquivo:
                                    if j == 0:
                                        arquivo.write(f'N{i}{numero_do_neuronio} := (')
                                    else:
                                        arquivo.write(f'{y} * {peso_value} + ')
                            else:
                                if numero_do_neuronio in neuronios_utilizados:
                                    with open(arquivo_escrito, 'r') as arquivo_leitura:
                                        linhas = arquivo_leitura.readlines()
                                    with open(arquivo_escrito, 'w') as arquivo:
                                        for linha in linhas:
                                            if linha.startswith(f'N{i}{numero_do_neuronio} :='):
                                                nova_linha = f'{linha.strip()} + {y} * {peso_value}\n'
                                                arquivo.write(nova_linha)
                                            else:
                                                arquivo.write(linha)
                                else:
                                    with open(arquivo_escrito, 'a') as arquivo:
                                        arquivo.write(f'N{i}{numero_do_neuronio} := ({y} * {peso_value}\n')
                                    neuronios_utilizados.add(numero_do_neuronio)
                            chave = f'N{i}{numero_do_neuronio} '
                            if chave not in vetor_procurar:
                                vetor_procurar.append(chave)                  
            with open(arquivo_escrito, 'a') as arquivo: 
                arquivo.write('\n(## Saída do(s) neurônio(s) - Aplicação da função de ativação ##) \n\n')
            for bias_key, bias_value in biases.items():
                if i == len(rede_neural['Camadas']):
                    with open(arquivo_escrito, 'a') as arquivo: 
                        arquivo.write(f'{bias_value}; \n')
                else: 
                    vetor_de_biases.append(bias_value)      
    
            with open(arquivo_escrito, 'a') as arquivo: 
                if i == len(camadas) - 1:
                    activation = out_activation_function
                else:
                    activation = activation_function
                for z in range(len(novo_vetor)):
                    with open(arquivo_escrito, 'a') as arquivo:
                        if activation == 'relu':
                            arquivo.write(f'N{i}{z}out := Max(0, N{i}{z});\n')
                        elif activation == 'tanh':
                            arquivo.write(f'N{i}{z}out := (exp(N{i}{z}) - exp(-N{i}{z})) / (exp(N{i}{z}) + exp(-N{i}{z}));\n')
                        elif activation == 'logistic':
                            arquivo.write(f'N{i}{z}out := 1 / (1 + exp(-N{i}{z}));\n')
                        elif activation == 'identity':
                            arquivo.write(f'N{i}{z}out := N{i}{z};\n')
                    vetor_entrada.append(f'N{i}{z}out')
                    vetor_saidas.append(f'N{i}{z}out')          
            neuronios_utilizados.clear()
            
    return vetor_procurar, vetor_de_biases, vetor_saidas, neuronios_utilizados