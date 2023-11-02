

with open(f'plot_duplo.csv', 'r') as f:
    geral = f.readlines()

ini = 0
soma = 0
for line in geral:
    if ini == 0:
        ini += 1
        continue
    i = 0
    line = line.replace('\n', '')
    line = line.split(',')
    
    for sys in line:
        if line[i] == '':
            continue
        soma += int(float(line[i]))
        i+=1

print(f'Total sys usada: {soma}')

with open(f'./histogramas/media/soma-ruschel-geral.csv', 'r') as f:
    geral = f.readlines()

passo = 0
n_ruim_rus = 0

for line in geral:
    line = line.replace('\n', '')
    line = line.split(',')

    if passo == 0:
        passo+=1
        continue
    
    i = 0

    for sys in line:
        n_ruim_rus += int(float(line[i]))
        i+=1
    break

with open(f'./histogramas/media/soma-frasao-geral.csv', 'r') as f:
    geral = f.readlines()

passo = 0
n_ruim_fra = 0

for line in geral:
    line = line.replace('\n', '')
    line = line.split(',')

    if passo == 0:
        passo += 1
        continue
    
    i = 0

    for sys in line:
        n_ruim_fra += int(float(line[i]))
        i+=1
    break
soma_t = n_ruim_rus+n_ruim_fra
print(f'Total: {soma_t}')

print(f'Porcentagem {soma/soma_t}')
