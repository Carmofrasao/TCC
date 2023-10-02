import operator

a = -1
m=0
i=0
with open(f'./histogramas/media/soma-frasao-geral.csv', "r") as f:
    geral_frasao = f.readlines()
with open(f'./histogramas/media/soma-ruschel-geral.csv', "r") as f:
    geral_ruschel = f.readlines()
    
passo = 0
syscall_bom_frasao = {}
syscall_ruim_frasao = {}
syscall_bom_ruschell = {}
syscall_ruim_ruschell = {}

for line in geral_frasao:
    line = line.replace('\n', '')
    line = line.split(',')
    if passo == 0:
        for sys in line:
            syscall_ruim_frasao[sys] = 0
        passo+=1
    elif passo == 1:
        i = 0
        for sys in syscall_ruim_frasao:
            syscall_ruim_frasao[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_ruim_frasao)
    elif passo == 2:
        for sys in line:
            syscall_bom_frasao[sys] = 0
        passo+=1
    elif passo == 3:
        i = 0
        for sys in syscall_bom_frasao:
            syscall_bom_frasao[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_bom_frasao)
passo = 0
for line in geral_ruschel:
    line = line.replace('\n', '')
    line = line.split(',')
    if passo == 0:
        for sys in line:
            syscall_ruim_ruschell[sys] = 0
        passo+=1
    elif passo == 1:
        i = 0
        for sys in syscall_ruim_ruschell:
            syscall_ruim_ruschell[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_ruim_ruschell)
    elif passo == 2:
        for sys in line:
            syscall_bom_ruschell[sys] = 0
        passo+=1
    elif passo == 3:
        i = 0
        for sys in syscall_bom_ruschell:
            syscall_bom_ruschell[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_bom_ruschell)

for sys in syscall_ruim_frasao:
    if syscall_ruim_frasao[sys] >= 50 or syscall_ruim_ruschell[sys] >= 50:
        print(sys+','+sys, end=',')
print()
for sys in syscall_ruim_frasao:
    if syscall_ruim_frasao[sys] >= 50 or syscall_ruim_ruschell[sys] >= 50:
        print(f'{syscall_ruim_frasao[sys]},{syscall_ruim_ruschell[sys]}', end=',')
print()