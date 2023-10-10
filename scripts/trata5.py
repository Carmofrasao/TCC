import operator

a = -1
m=0
i=0
with open(f'./histogramas/histogramas.csv', "r") as f:
    geral_frasao = f.readlines()
    
passo = 0
syscall_bom_frasao = {}
syscall_ruim_frasao = {}

for line in geral_frasao:
    line = line.replace('\n', '')
    line = line.split(',')
    if passo == 0:
        for sys in line:
            syscall_ruim_frasao[sys] = 0
            syscall_bom_frasao[sys] = 0
        passo+=1
    elif passo >= 1 and passo < 101:
        i = 0
        for sys in syscall_ruim_frasao:
            syscall_ruim_frasao[sys] += int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_ruim_frasao)
    elif passo >= 101:
        i = 0
        for sys in syscall_bom_frasao:
            syscall_bom_frasao[sys] += int(float(line[i]))
            i+=1
        # print(syscall_bom_frasao)
syscall_ruim_frasao.pop('t')
syscall_ruim_frasao.pop('id')
syscall_bom_frasao.pop('t')
syscall_bom_frasao.pop('id')
for sys in syscall_bom_frasao:
    syscall_bom_frasao[sys] = syscall_bom_frasao[sys]/100

for sys in syscall_ruim_frasao:
    syscall_ruim_frasao[sys] = syscall_ruim_frasao[sys]/100

for sys in syscall_ruim_frasao:
    if syscall_ruim_frasao[sys] >= 50 or syscall_bom_frasao[sys] >= 50:
        print(sys+','+sys, end=',')
print()
for sys in syscall_ruim_frasao:
    if syscall_ruim_frasao[sys] >= 50 or syscall_bom_frasao[sys] >= 50:
        print(f'{syscall_ruim_frasao[sys]},{syscall_bom_frasao[sys]}', end=',')
print()