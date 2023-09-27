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
comp_ruim = {}
comp_bom = {}

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
    if sys == 't':
        continue
    # if syscall_ruim_ruschell[sys] == 0:
    #     continue
    comp_ruim[sys] = syscall_ruim_frasao[sys] - syscall_ruim_ruschell[sys]

a = 0
comp_ruim = sorted(comp_ruim.items(), key=operator.itemgetter(1), reverse=True)
print("t", end=',')
for sys in comp_ruim:
    if m+1 == len(comp_ruim):
        print(sys[0])
    else:
        print(sys[0], end=',')
    m+=1
m=0
print(f'{a}', end=',')
l=0
for sys in comp_ruim:
    if l+1 == len(comp_ruim):
        print(sys[1])
    else:
        print(sys[1], end=',')
    l+=1

a+=1
for sys in syscall_bom_frasao:
    if sys == 't':
        continue
    # if syscall_bom_ruschell[sys] == 0:
    #     continue
    comp_bom[sys] = syscall_bom_frasao[sys] - syscall_bom_ruschell[sys]

comp_bom = sorted(comp_bom.items(), key=operator.itemgetter(1), reverse=True)
print("t", end=',')
for sys in comp_bom:
    if m+1 == len(comp_bom):
        print(sys[0])
    else:
        print(sys[0], end=',')
    m+=1
m=0
print(f'{a}', end=',')
l=0
for sys in comp_bom:
    if l+1 == len(comp_bom):
        print(sys[1])
    else:
        print(sys[1], end=',')
    l+=1

# import operator

# a = -1
# m=0
# i=0
# with open(f'./histogramas/media/simple-file-frasao-geral.csv', "r") as f:
#     geral_frasao = f.readlines()
    
# passo = 0
# syscall_bom_frasao = {}
# syscall_ruim_frasao = {}
# comp = {}

# for line in geral_frasao:
#     line = line.replace('\n', '')
#     line = line.split(',')
#     if passo == 0:
#         for sys in line:
#             syscall_ruim_frasao[sys] = 0
#         passo+=1
#     elif passo == 1:
#         i = 0
#         for sys in syscall_ruim_frasao:
#             syscall_ruim_frasao[sys] = int(float(line[i]))
#             i+=1
#         passo+=1
#         # print(syscall_ruim_frasao)
#     elif passo == 2:
#         for sys in line:
#             syscall_bom_frasao[sys] = 0
#         passo+=1
#     elif passo == 3:
#         i = 0
#         for sys in syscall_bom_frasao:
#             syscall_bom_frasao[sys] = int(float(line[i]))
#             i+=1
#         passo+=1
#         # print(syscall_bom_frasao)

# for sys in syscall_ruim_frasao:
#     if sys == 't':
#         continue
#     comp[sys] = syscall_ruim_frasao[sys] - syscall_bom_frasao[sys]

# a = 0
# comp_ruim = sorted(comp.items(), key=operator.itemgetter(1), reverse=True)
# print("t", end=',')
# for sys in comp_ruim:
#     if m+1 == len(comp_ruim):
#         print(sys[0])
#     else:
#         print(sys[0], end=',')
#     m+=1
# m=0
# print(f'01', end=',')
# l=0
# for sys in comp_ruim:
#     if l+1 == len(comp_ruim):
#         print(sys[1])
#     else:
#         print(sys[1], end=',')
#     l+=1