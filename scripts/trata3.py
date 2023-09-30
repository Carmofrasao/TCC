import operator

a = -1
m=0
i=0
with open(f'./histogramas/media/file-manager-frasao-geral.csv', "r") as f:
    file = f.readlines()
with open(f'./histogramas/media/simple-file-frasao-geral.csv', "r") as f:
    simple = f.readlines()
with open(f'./histogramas/media/warfare-frasao-geral.csv', "r") as f:
    warfare = f.readlines()
    
passo = 0
syscall_bom_file = {}
syscall_ruim_file = {}
syscall_bom_simple = {}
syscall_ruim_simple = {}
syscall_bom_warfare = {}
syscall_ruim_warfare = {}
ruim = {}
bom = {}

for line in file:
    line = line.replace('\n', '')
    line = line.split(',')
    if passo == 0:
        for sys in line:
            syscall_ruim_file[sys] = 0
        passo+=1
    elif passo == 1:
        i = 0
        for sys in syscall_ruim_file:
            syscall_ruim_file[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_ruim_file)
    elif passo == 2:
        for sys in line:
            syscall_bom_file[sys] = 0
        passo+=1
    elif passo == 3:
        i = 0
        for sys in syscall_bom_file:
            syscall_bom_file[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_bom_frasao)
passo = 0
for line in simple:
    line = line.replace('\n', '')
    line = line.split(',')
    if passo == 0:
        for sys in line:
            syscall_ruim_simple[sys] = 0
        passo+=1
    elif passo == 1:
        i = 0
        for sys in syscall_ruim_simple:
            syscall_ruim_simple[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_ruim_simple)
    elif passo == 2:
        for sys in line:
            syscall_bom_simple[sys] = 0
        passo+=1
    elif passo == 3:
        i = 0
        for sys in syscall_bom_simple:
            syscall_bom_simple[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_bom_ruschell)
passo = 0
for line in warfare:
    line = line.replace('\n', '')
    line = line.split(',')
    if passo == 0:
        for sys in line:
            syscall_ruim_warfare[sys] = 0
        passo+=1
    elif passo == 1:
        i = 0
        for sys in syscall_ruim_warfare:
            syscall_ruim_warfare[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_ruim_warfare)
    elif passo == 2:
        for sys in line:
            syscall_bom_warfare[sys] = 0
        passo+=1
    elif passo == 3:
        i = 0
        for sys in syscall_bom_warfare:
            syscall_bom_warfare[sys] = int(float(line[i]))
            i+=1
        passo+=1
        # print(syscall_bom_ruschell)

for sys in syscall_ruim_file:
    if sys == 't':
        continue
    ruim[sys] = int((syscall_ruim_file[sys] + syscall_ruim_simple[sys] + syscall_ruim_warfare[sys])/2)

a = 0
ruim = sorted(ruim.items(), key=operator.itemgetter(1), reverse=True)
print("t", end=',')
for sys in ruim:
    if m+1 == len(ruim):
        print(sys[0])
    else:
        print(sys[0], end=',')
    m+=1
m=0
print(f'{a}', end=',')
l=0
for sys in ruim:
    if l+1 == len(ruim):
        print(sys[1])
    else:
        print(sys[1], end=',')
    l+=1

a+=1
for sys in syscall_bom_file:
    if sys == 't':
        continue
    bom[sys] = int((syscall_bom_file[sys] + syscall_bom_simple[sys] + syscall_bom_warfare[sys])/2)

bom = sorted(bom.items(), key=operator.itemgetter(1), reverse=True)
print("t", end=',')
for sys in bom:
    if m+1 == len(bom):
        print(sys[0])
    else:
        print(sys[0], end=',')
    m+=1
m=0
print(f'{a}', end=',')
l=0
for sys in bom:
    if l+1 == len(bom):
        print(sys[1])
    else:
        print(sys[1], end=',')
    l+=1