import os

syscall = { "read" : [] , "write" : [] , "open" : [] , "close" : [] , "stat" : [] , "fstat" : [] , "lstat" : [] , "poll" : [] , "lseek" : [] , "mmap" : [] , "mprotect" : [] , "munmap" : [] , "brk" : [] , "access" : [] , "pipe" : [] , "select" : [] , "sched_yield" : [] , "mremap" : [] , "msync" : [] , "mincore" : [] , "madvise" : [] , "shmget" : [] , "shmat" : [] , "shmctl" : [] , "dup" : [] , "dup2" : [] , "pause" : [] , "nanosleep" : [] , "getitimer" : [] , "alarm" : [] , "setitimer" : [] , "getpid" : [] , "sendfile" : [] , "socket" : [] , "connect" : [] , "accept" : [] , "sendto" : [] , "rt_sigaction" : [] , "rt_sigprocmask" : [] , "rt_sigreturn" : [] , "ioctl" : [] , "pread64" : [] , "pwrite64" : [] , "readv" : [] , "writev" : [] , "recvfrom" : [] , "sendmsg" : [] , "recvmsg" : [] , "shutdown" : [] , "bind" : [] , "listen" : [] , "getsockname" : [] , "getpeername" : [] , "socketpair" : [] , "setsockopt" : [] , "getsockopt" : [] , "clone" : [] , "fork" : [] , "vfork" : [] , "execve" : [] , "exit" : [] , "wait4" : [] , "kill" : [] , "uname" : [] , "semget" : [] , "semop" : [] , "semctl" : [] , "shmdt" : [] , "msgget" : [] , "msgsnd" : [] , "msgrcv" : [] , "msgctl" : [] , "fcntl" : [] , "flock" : [] , "fsync" : [] , "fdatasync" : [] , "truncate" : [] , "ftruncate" : [] , "getdents" : [] , "getcwd" : [] , "chdir" : [] , "fchdir" : [] , "rename" : [] , "mkdir" : [] , "rmdir" : [] , "creat" : [] , "link" : [] , "unlink" : [] , "symlink" : [] , "readlink" : [] , "chmod" : [] , "fchmod" : [] , "chown" : [] , "fchown" : [] , "lchown" : [] , "umask" : [] , "gettimeofday" : [] , "getrlimit" : [] , "getrusage" : [] , "sysinfo" : [] , "times" : [] , "getuid" : [] , "syslog" : [] , "getgid" : [] , "setuid" : [] , "setgid" : [] , "geteuid" : [] , "getegid" : [] , "setpgid" : [] , "getppid" : [] , "getpgrp" : [] , "setsid" : [] , "setreuid" : [] , "setregid" : [] , "getgroups" : [] , "setgroups" : [] , "setresuid" : [] , "getresuid" : [] , "setresgid" : [] , "getresgid" : [] , "getpgid" : [] , "setfsuid" : [] , "setfsgid" : [] , "getsid" : [] , "capget" : [] , "capset" : [] , "ptrace" : [] , "rt_sigpending" : [] , "rt_sigtimedwait" : [] , "rt_sigqueueinfo" : [] , "sigaltstack" : [] , "uselib" : [] , "_sysctl" : [] , "create_module" : [] , "rt_sigsuspend" : [] , "utime" : [] , "mknod" : [] , "personality" : [] , "ustat" : [] , "statfs" : [] , "fstatfs" : [] , "sysfs" : [] , "getpriority" : [] , "setpriority" : [] , "sched_setparam" : [] , "sched_getparam" : [] , "sched_setscheduler" : [] , "sched_getscheduler" : [] , "sched_get_priority_max" : [] , "sched_get_priority_min" : [] , "sched_rr_get_interval" : [] , "mlock" : [] , "munlock" : [] , "mlockall" : [] , "munlockall" : [] , "vhangup" : [] , "modify_ldt" : [] , "pivot_root" : [] , "prctl" : [] , "arch_prctl" : [] , "adjtimex" : [] , "setrlimit" : [] , "chroot" : [] , "sync" : [] , "acct" : [] , "settimeofday" : [] , "mount" : [] , "umount2" : [] , "swapon" : [] , "swapoff" : [] , "reboot" : [] , "sethostname" : [] , "setdomainname" : [] , "iopl" : [] , "ioperm" : [] , "init_module" : [] , "delete_module" : [] , "get_kernel_syms" : [] , "query_module" : [] , "nfsservctl" : [] , "set_thread_area" : [] , "io_setup" : [] , "io_submit" : [] , "get_thread_area" : [] , "epoll_ctl_old" : [] , "epoll_wait_old" : [] , "timer_create" : [] , "quotactl" : [] , "getpmsg" : [] , "putpmsg" : [] , "afs_syscall" : [] , "tuxcall" : [] , "security" : [] , "gettid" : [] , "readahead" : [] , "setxattr" : [] , "lsetxattr" : [] , "fsetxattr" : [] , "getxattr" : [] , "lgetxattr" : [] , "fgetxattr" : [] , "listxattr" : [] , "llistxattr" : [] , "flistxattr" : [] , "removexattr" : [] , "lremovexattr" : [] , "fremovexattr" : [] , "tkill" : [] , "time" : [] , "futex" : [] , "sched_setaffinity" : [] , "sched_getaffinity" : [] , "io_destroy" : [] , "io_getevents" : [] , "io_cancel" : [] , "lookup_dcookie" : [] , "epoll_create" : [] , "remap_file_pages" : [] , "getdents64" : [] , "set_tid_address" : [] , "restart_syscall" : [] , "semtimedop" : [] , "fadvise64" : [] , "timer_settime" : [] , "timer_gettime" : [] , "timer_getoverrun" : [] , "timer_delete" : [] , "clock_settime" : [] , "clock_gettime" : [] , "clock_getres" : [] , "clock_nanosleep" : [] , "exit_group" : [] , "epoll_wait" : [] , "epoll_ctl" : [] , "tgkill" : [] , "utimes" : [] , "vserver" : [] , "mq_notify" : [] , "kexec_load" : [] , "waitid" : [] , "set_robust_list" : [] , "get_robust_list" : [] , "vmsplice" : [] , "move_pages" : [] , "mbind" : [] , "set_mempolicy" : [] , "get_mempolicy" : [] , "mq_open" : [] , "mq_unlink" : [] , "mq_timedsend" : [] , "mq_timedreceive" : [] , "mq_getsetattr" : [] , "add_key" : [] , "request_key" : [] , "keyctl" : [] , "ioprio_set" : [] , "ioprio_get" : [] , "inotify_init" : [] , "inotify_add_watch" : [] , "inotify_rm_watch" : [] , "migrate_pages" : [] , "openat" : [] , "mkdirat" : [] , "mknodat" : [] , "fchownat" : [] , "futimesat" : [] , "newfstatat" : [] , "unlinkat" : [] , "renameat" : [] , "linkat" : [] , "symlinkat" : [] , "readlinkat" : [] , "fchmodat" : [] , "faccessat" : [] , "pselect6" : [] , "ppoll" : [] , "unshare" : [] , "splice" : [] , "tee" : [] , "sync_file_range" : [] , "utimensat" : [] , "epoll_pwait" : [] , "signalfd" : [] , "timerfd_create" : [] , "eventfd" : [] , "fallocate" : [] , "timerfd_settime" : [] , "timerfd_gettime" : [] , "accept4" : [] , "signalfd4" : [] , "eventfd2" : [] , "epoll_create1" : [] , "dup3" : [] , "pipe2" : [] , "preadv" : [] , "pwritev" : [] , "rt_tgsigqueueinfo" : [] , "recvmmsg" : [] , "sendmmsg" : [] , "process_vm_readv" : [] , "process_vm_writev" : [] , "execveat" : [] , "preadv2" : [] , "pwritev2" : [] , "inotify_init1" : [] , "perf_event_open" : [] , "fanotify_init" : [] , "fanotify_mark" : [] , "prlimit64" : [] , "name_to_handle_at" : [] , "open_by_handle_at" : [] , "clock_adjtime" : [] , "syncfs" : [] , "setns" : [] , "getcpu" : [] , "kcmp" : [] , "finit_module" : [] , "sched_setattr" : [] , "sched_getattr" : [] , "renameat2" : [] , "seccomp" : [] , "getrandom" : [] , "memfd_create" : [] , "kexec_file_load" : [] , "bpf" : [] , "userfaultfd" : [] , "membarrier" : [] , "mlock2" : [] , "copy_file_range" : [] , "pkey_mprotect" : [] , "pkey_alloc" : [] , "pkey_free" : [] , "statx" : [] , "io_pgetevents" : [] , "rseq" : [] , "pidfd_send_signal" : [] , "io_uring_setup" : [] , "io_uring_enter" : [] , "io_uring_register" : [] , "open_tree" : [] , "move_mount" : [] , "fsopen" : [] , "fsconfig" : [] , "fsmount" : [] , "fspick" : [] , "pidfd_open" : [] , "clone3" : [] , "close_range" : [] , "openat2" : [] , "pidfd_getfd" : [] , "faccessat2" : [] , "process_madvise" : [] , "epoll_pwait2" : [] , "mount_setattr" : [] , "quotactl_fd" : [] , "landlock_create_ruleset" : [] , "landlock_add_rule" : [] , "landlock_restrict_self" : [] , "memfd_secret" : [] , "process_mrelease" : [] , "futex_waitv" : [] , "set_mempolicy_home_node" : [] , "cachestat" : [] , "rt_sigaction" : [] , "rt_sigreturn" : [] , "ioctl" : [] , "readv" : [] , "writev" : [] , "recvfrom" : [] , "sendmsg" : [] , "recvmsg" : [] , "execve" : [] , "ptrace" : [] , "rt_sigpending" : [] , "rt_sigtimedwait" : [] , "rt_sigqueueinfo" : [] , "sigaltstack" : [] , "timer_create" : [] , "mq_notify" : [] , "kexec_load" : [] , "waitid" : [] , "set_robust_list" : [] , "get_robust_list" : [] , "vmsplice" : [] , "move_pages" : [] , "preadv" : [] , "pwritev" : [] , "rt_tgsigqueueinfo" : [] , "recvmmsg" : [] , "sendmmsg" : [] , "process_vm_readv" : [] , "process_vm_writev" : [] , "setsockopt" : [] , "getsockopt" : [] , "io_setup" : [] , "io_submit" : [] , "execveat" : [] , "preadv2" : [] , "pwritev2" : []
}

print("t", end=',')
i = 0
for sys in syscall:
   if i == 362:
       print(sys)
   else:
       print(sys, end=',')
   i+=1
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

a = -1
soma = list(range(len(syscall)))
with open(f'./histogramas/file-manager-frasao.csv', "r") as f:
    lines = f.readlines()
count = 0
# Trecho para contar o numero de chamadas de cada syscall
for line in lines:
    if (line.startswith("id")):
       continue
    
    line = line.replace('\n', '')
    linhaAux = line.split(',')

    for i in range(len(syscall)):
        soma[i] += int(linhaAux[i+2])
    count+=1
    if count == 10:
        a+=1
        print(f'{a}', end=',')
        for i in range(len(syscall)):
            if i+1 == len(syscall):
                print(soma[i]/10)
            else:
                print(soma[i]/10, end=',')
            soma[i] = 0
        count = 0
    