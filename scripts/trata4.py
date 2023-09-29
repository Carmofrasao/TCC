a = -1
m=0
i=0
with open(f'./histogramas/media/soma-ruschel-geral.csv', "r") as f:
    geral = f.readlines()
  
passo = 0
syscall_bom = {}
syscall_ruim = {}
n_bom = 0
n_ruim = 0
for line in geral:
    line = line.replace('\n', '')
    line = line.split(',')
    if passo == 0:
        for sys in line:
            syscall_ruim[sys] = 0
        passo+=1
    elif passo == 1:
        i = 0
        for sys in syscall_ruim:
            syscall_ruim[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_ruim_frasao)
    elif passo == 2:
        for sys in line:
            syscall_bom[sys] = 0
        passo+=1
    elif passo == 3:
        i = 0
        for sys in syscall_bom:
            syscall_bom[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_bom_frasao)

for sys in syscall_bom:
    if sys == 't':
        continue
    n_bom += syscall_bom[sys]

n_bom = n_bom / len(syscall_bom)
print(f'Média de chamadas normais: {n_bom}')
for sys in syscall_ruim:
    if sys == 't':
        continue
    n_ruim += syscall_ruim[sys]
n_ruim = n_ruim / len(syscall_ruim)
print(f'Média de chamadas anormais: {n_ruim}')
