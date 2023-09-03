import os
import operator

syscall = { "read" : 0 , "write" : 0 , "open" : 0 , "close" : 0 , "stat" : 0 , "fstat" : 0 , "lstat" : 0 , "poll" : 0 , "lseek" : 0 , "mmap" : 0 , "mprotect" : 0 , "munmap" : 0 , "brk" : 0 , "access" : 0 , "pipe" : 0 , "select" : 0 , "sched_yield" : 0 , "mremap" : 0 , "msync" : 0 , "mincore" : 0 , "madvise" : 0 , "shmget" : 0 , "shmat" : 0 , "shmctl" : 0 , "dup" : 0 , "dup2" : 0 , "pause" : 0 , "nanosleep" : 0 , "getitimer" : 0 , "alarm" : 0 , "setitimer" : 0 , "getpid" : 0 , "sendfile" : 0 , "socket" : 0 , "connect" : 0 , "accept" : 0 , "sendto" : 0 , "rt_sigaction" : 0 , "rt_sigprocmask" : 0 , "rt_sigreturn" : 0 , "ioctl" : 0 , "pread64" : 0 , "pwrite64" : 0 , "readv" : 0 , "writev" : 0 , "recvfrom" : 0 , "sendmsg" : 0 , "recvmsg" : 0 , "shutdown" : 0 , "bind" : 0 , "listen" : 0 , "getsockname" : 0 , "getpeername" : 0 , "socketpair" : 0 , "setsockopt" : 0 , "getsockopt" : 0 , "clone" : 0 , "fork" : 0 , "vfork" : 0 , "execve" : 0 , "exit" : 0 , "wait4" : 0 , "kill" : 0 , "uname" : 0 , "semget" : 0 , "semop" : 0 , "semctl" : 0 , "shmdt" : 0 , "msgget" : 0 , "msgsnd" : 0 , "msgrcv" : 0 , "msgctl" : 0 , "fcntl" : 0 , "flock" : 0 , "fsync" : 0 , "fdatasync" : 0 , "truncate" : 0 , "ftruncate" : 0 , "getdents" : 0 , "getcwd" : 0 , "chdir" : 0 , "fchdir" : 0 , "rename" : 0 , "mkdir" : 0 , "rmdir" : 0 , "creat" : 0 , "link" : 0 , "unlink" : 0 , "symlink" : 0 , "readlink" : 0 , "chmod" : 0 , "fchmod" : 0 , "chown" : 0 , "fchown" : 0 , "lchown" : 0 , "umask" : 0 , "gettimeofday" : 0 , "getrlimit" : 0 , "getrusage" : 0 , "sysinfo" : 0 , "times" : 0 , "getuid" : 0 , "syslog" : 0 , "getgid" : 0 , "setuid" : 0 , "setgid" : 0 , "geteuid" : 0 , "getegid" : 0 , "setpgid" : 0 , "getppid" : 0 , "getpgrp" : 0 , "setsid" : 0 , "setreuid" : 0 , "setregid" : 0 , "getgroups" : 0 , "setgroups" : 0 , "setresuid" : 0 , "getresuid" : 0 , "setresgid" : 0 , "getresgid" : 0 , "getpgid" : 0 , "setfsuid" : 0 , "setfsgid" : 0 , "getsid" : 0 , "capget" : 0 , "capset" : 0 , "ptrace" : 0 , "rt_sigpending" : 0 , "rt_sigtimedwait" : 0 , "rt_sigqueueinfo" : 0 , "sigaltstack" : 0 , "uselib" : 0 , "_sysctl" : 0 , "create_module" : 0 , "rt_sigsuspend" : 0 , "utime" : 0 , "mknod" : 0 , "personality" : 0 , "ustat" : 0 , "statfs" : 0 , "fstatfs" : 0 , "sysfs" : 0 , "getpriority" : 0 , "setpriority" : 0 , "sched_setparam" : 0 , "sched_getparam" : 0 , "sched_setscheduler" : 0 , "sched_getscheduler" : 0 , "sched_get_priority_max" : 0 , "sched_get_priority_min" : 0 , "sched_rr_get_interval" : 0 , "mlock" : 0 , "munlock" : 0 , "mlockall" : 0 , "munlockall" : 0 , "vhangup" : 0 , "modify_ldt" : 0 , "pivot_root" : 0 , "prctl" : 0 , "arch_prctl" : 0 , "adjtimex" : 0 , "setrlimit" : 0 , "chroot" : 0 , "sync" : 0 , "acct" : 0 , "settimeofday" : 0 , "mount" : 0 , "umount2" : 0 , "swapon" : 0 , "swapoff" : 0 , "reboot" : 0 , "sethostname" : 0 , "setdomainname" : 0 , "iopl" : 0 , "ioperm" : 0 , "init_module" : 0 , "delete_module" : 0 , "get_kernel_syms" : 0 , "query_module" : 0 , "nfsservctl" : 0 , "set_thread_area" : 0 , "io_setup" : 0 , "io_submit" : 0 , "get_thread_area" : 0 , "epoll_ctl_old" : 0 , "epoll_wait_old" : 0 , "timer_create" : 0 , "quotactl" : 0 , "getpmsg" : 0 , "putpmsg" : 0 , "afs_syscall" : 0 , "tuxcall" : 0 , "security" : 0 , "gettid" : 0 , "readahead" : 0 , "setxattr" : 0 , "lsetxattr" : 0 , "fsetxattr" : 0 , "getxattr" : 0 , "lgetxattr" : 0 , "fgetxattr" : 0 , "listxattr" : 0 , "llistxattr" : 0 , "flistxattr" : 0 , "removexattr" : 0 , "lremovexattr" : 0 , "fremovexattr" : 0 , "tkill" : 0 , "time" : 0 , "futex" : 0 , "sched_setaffinity" : 0 , "sched_getaffinity" : 0 , "io_destroy" : 0 , "io_getevents" : 0 , "io_cancel" : 0 , "lookup_dcookie" : 0 , "epoll_create" : 0 , "remap_file_pages" : 0 , "getdents64" : 0 , "set_tid_address" : 0 , "restart_syscall" : 0 , "semtimedop" : 0 , "fadvise64" : 0 , "timer_settime" : 0 , "timer_gettime" : 0 , "timer_getoverrun" : 0 , "timer_delete" : 0 , "clock_settime" : 0 , "clock_gettime" : 0 , "clock_getres" : 0 , "clock_nanosleep" : 0 , "exit_group" : 0 , "epoll_wait" : 0 , "epoll_ctl" : 0 , "tgkill" : 0 , "utimes" : 0 , "vserver" : 0 , "mq_notify" : 0 , "kexec_load" : 0 , "waitid" : 0 , "set_robust_list" : 0 , "get_robust_list" : 0 , "vmsplice" : 0 , "move_pages" : 0 , "mbind" : 0 , "set_mempolicy" : 0 , "get_mempolicy" : 0 , "mq_open" : 0 , "mq_unlink" : 0 , "mq_timedsend" : 0 , "mq_timedreceive" : 0 , "mq_getsetattr" : 0 , "add_key" : 0 , "request_key" : 0 , "keyctl" : 0 , "ioprio_set" : 0 , "ioprio_get" : 0 , "inotify_init" : 0 , "inotify_add_watch" : 0 , "inotify_rm_watch" : 0 , "migrate_pages" : 0 , "openat" : 0 , "mkdirat" : 0 , "mknodat" : 0 , "fchownat" : 0 , "futimesat" : 0 , "newfstatat" : 0 , "unlinkat" : 0 , "renameat" : 0 , "linkat" : 0 , "symlinkat" : 0 , "readlinkat" : 0 , "fchmodat" : 0 , "faccessat" : 0 , "pselect6" : 0 , "ppoll" : 0 , "unshare" : 0 , "splice" : 0 , "tee" : 0 , "sync_file_range" : 0 , "utimensat" : 0 , "epoll_pwait" : 0 , "signalfd" : 0 , "timerfd_create" : 0 , "eventfd" : 0 , "fallocate" : 0 , "timerfd_settime" : 0 , "timerfd_gettime" : 0 , "accept4" : 0 , "signalfd4" : 0 , "eventfd2" : 0 , "epoll_create1" : 0 , "dup3" : 0 , "pipe2" : 0 , "preadv" : 0 , "pwritev" : 0 , "rt_tgsigqueueinfo" : 0 , "recvmmsg" : 0 , "sendmmsg" : 0 , "process_vm_readv" : 0 , "process_vm_writev" : 0 , "execveat" : 0 , "preadv2" : 0 , "pwritev2" : 0 , "inotify_init1" : 0 , "perf_event_open" : 0 , "fanotify_init" : 0 , "fanotify_mark" : 0 , "prlimit64" : 0 , "name_to_handle_at" : 0 , "open_by_handle_at" : 0 , "clock_adjtime" : 0 , "syncfs" : 0 , "setns" : 0 , "getcpu" : 0 , "kcmp" : 0 , "finit_module" : 0 , "sched_setattr" : 0 , "sched_getattr" : 0 , "renameat2" : 0 , "seccomp" : 0 , "getrandom" : 0 , "memfd_create" : 0 , "kexec_file_load" : 0 , "bpf" : 0 , "userfaultfd" : 0 , "membarrier" : 0 , "mlock2" : 0 , "copy_file_range" : 0 , "pkey_mprotect" : 0 , "pkey_alloc" : 0 , "pkey_free" : 0 , "statx" : 0 , "io_pgetevents" : 0 , "rseq" : 0 , "pidfd_send_signal" : 0 , "io_uring_setup" : 0 , "io_uring_enter" : 0 , "io_uring_register" : 0 , "open_tree" : 0 , "move_mount" : 0 , "fsopen" : 0 , "fsconfig" : 0 , "fsmount" : 0 , "fspick" : 0 , "pidfd_open" : 0 , "clone3" : 0 , "close_range" : 0 , "openat2" : 0 , "pidfd_getfd" : 0 , "faccessat2" : 0 , "process_madvise" : 0 , "epoll_pwait2" : 0 , "mount_setattr" : 0 , "quotactl_fd" : 0 , "landlock_create_ruleset" : 0 , "landlock_add_rule" : 0 , "landlock_restrict_self" : 0 , "memfd_secret" : 0 , "process_mrelease" : 0 , "futex_waitv" : 0 , "set_mempolicy_home_node" : 0 , "cachestat" : 0
}

"""
for _, _, arquivos in os.walk('./wordpress/logs/anormal/sysdig'):
    for arquivo in arquivos:
        with open(f'./wordpress/logs/anormal/sysdig/{arquivo}', "r") as f:
            lines = f.readlines()

        # Trecho para tirar o que não é syscall
        # with open(f'./wordpress/logs/anormal/sysdig/{arquivo}', "w") as f:
        #     for line in lines:
        #         linhaAux = line.split(' ')
        #         call = linhaAux[8:]
        #         f.write(' '.join(call))


        # Trecho para contar o numero de chamadas de cada syscall
        for line in lines:
            linhaAux = line.split(' ')
            call = linhaAux[0]
            syscall[call] += 1
        print(f'{id},0', end=',')
        id += 1
        for sys in syscall.values():
            if i == 362:
                print(sys)
            else:
                print(sys, end=',')
            i+=1
        i=0
        for sys in syscall:
            syscall[sys] = 0
        
for _, _, arquivos in os.walk('./wordpress/logs/normal/sysdig'):
    for arquivo in arquivos:
        with open(f'./wordpress/logs/normal/sysdig/{arquivo}', "r") as f:
            lines = f.readlines()

        # Trecho para contar o numero de chamadas de cada syscall
        for line in lines:
            linhaAux = line.split(' ')
            call = linhaAux[0]
            syscall[call] += 1
        print(f'{id},1', end=',')
        id += 1
        for sys in syscall.values():
            if i == 362:
                print(sys)
            else:
                print(sys, end=',')
            i+=1
        i=0
                
        for sys in syscall:
            syscall[sys] = 0

for l in range(1, 11):
    with open(f'./teste_frasao/anormal/warfare-{l}.log', "r") as f:
        lines = f.readlines()

    # Trecho para contar o numero de chamadas de cada syscall
    for line in lines:
        #if (line.startswith("---")):
        #    continue
        linhaAux = line.split(' ')
        call = linhaAux[0]
        syscall[call] += 1
    print(f'{id},0', end=',')
    id += 1
    for sys in syscall.values():
        if i+1 == len(syscall):
            print(sys)
        else:
            print(sys, end=',')
        i+=1
    i=0
    for sys in syscall:
        syscall[sys] = 0
        
for l in range(1, 11):
    with open(f'./teste_frasao/normal/warfare-{l}.log', "r") as f:
        lines = f.readlines()

    # Trecho para contar o numero de chamadas de cada syscall
    for line in lines:
        #if (line.startswith("---")):
        #    continue
        linhaAux = line.split(' ')
        call = linhaAux[0]
        syscall[call] += 1
    print(f'{id},1', end=',')
    id += 1
    for sys in syscall.values():
        if i+1 == len(syscall):
            print(sys)
        else:
            print(sys, end=',')
        i+=1
    i=0
            
    for sys in syscall:
        syscall[sys] = 0

print(f'0', end=',')
id += 1
for sys in syscall.values():
    if i+1 == len(syscall):
        print(sys)
    else:
        print(sys, end=',')
    i+=1
i=0
for sys in syscall:
    syscall[sys] = 0
        
for l in range(1, 11):
    with open(f'./teste_frasao/normal/warfare-{l}.log', "r") as f:
        lines = f.readlines()

    # Trecho para contar o numero de chamadas de cada syscall
    for line in lines:
        #if (line.startswith("---")):
        #    continue
        linhaAux = line.split(' ')
        call = linhaAux[0]
        syscall[call] += 1
    print(f'{id},1', end=',')
    id += 1
    for sys in syscall.values():
        if i+1 == len(syscall):
            print(sys)
        else:
            print(sys, end=',')
        i+=1
    i=0
            
    for sys in syscall:
        syscall[sys] = 0
"""

# a = -1
# i=0
# with open(f'./histogramas/simple-file-frasao.csv', "r") as f:
#     lines = f.readlines()
# count = 0
# # Trecho para contar o numero de chamadas de cada syscall
# for line in lines:
#     if (line.startswith("id")):
#        continue
#     line = line.replace('\n', '')
#     linhaAux = line.split(',')
    
#     for sys in syscall:
#         syscall[sys].append(int(linhaAux[i+2]))
#         i+=1
#     i=0
#     count+=1
#     if count == 10:
#         for sys in syscall:
#             syscall[sys].sort()
#         a+=1
#         print(f'{a}', end=',')
#         l=0
#         for sys in syscall.values():
#             if l+1 == len(syscall):
#                 print((sys[4]+sys[5])/2)
#             else:
#                 print((sys[4]+sys[5])/2, end=',')
#             l+=1
#         for sys in syscall:
#             syscall[sys].clear()
#         count = 0

# a = -1
# soma = list(range(len(syscall)))
# with open(f'./histogramas/file-manager-frasao.csv', "r") as f:
#     lines = f.readlines()
# count = 0
# # Trecho para contar o numero de chamadas de cada syscall
# for line in lines:
#     if (line.startswith("id")):
#        continue
    
#     line = line.replace('\n', '')
#     linhaAux = line.split(',')

#     for i in range(len(syscall)):
#         soma[i] += int(linhaAux[i+2])
#     count+=1
#     if count == 10:
#         a+=1
#         print(f'{a}', end=',')
#         for i in range(len(syscall)):
#             if i+1 == len(syscall):
#                 print(soma[i]/10)
#             else:
#                 print(soma[i]/10, end=',')
#             soma[i] = 0
#         count = 0

m = 0
a = -1
passou = True
with open(f'./histogramas/media/warfare-ruschel-geral.csv', "r") as f:
    lines = f.readlines()
count = 0
# Trecho para contar o numero de chamadas de cada syscall
for line in lines:
    if (line.startswith("t")):
       continue
    
    line = line.replace('\n', '')
    linhaAux = line.split(',')
    u = 0
    for sys in syscall:
        syscall[sys] = float(linhaAux[u+1])
        u+=1
    sysOrder = sorted(syscall.items(), key=operator.itemgetter(1), reverse=True)
    if passou:
        print("t", end=',')
        for sys in sysOrder:
            if m+1 == len(syscall):
                print(sys[0])
            else:
                print(sys[0], end=',')
            m+=1
        passou = False
    m=0
    a+=1
    print(f'{a}', end=',')
    l=0
    for sys in sysOrder:
        if l+1 == len(syscall):
            print(sys[1])
        else:
            print(sys[1], end=',')
        l+=1

    u = 0
    for sys in syscall:
        syscall[sys] = 0
        u+=1