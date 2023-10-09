from itertools import islice
from syscalls import syscalls
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import LinearSVC
# from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.ensemble import AdaBoostClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score

import numpy as np

import argparse
import os

syscall = { "read" : 0 , "write" : 0 , "open" : 0 , "close" : 0 , "stat" : 0 , "fstat" : 0 , "lstat" : 0 , "poll" : 0 , "lseek" : 0 , "mmap" : 0 , "mprotect" : 0 , "munmap" : 0 , "brk" : 0 , "access" : 0 , "pipe" : 0 , "select" : 0 , "sched_yield" : 0 , "mremap" : 0 , "msync" : 0 , "mincore" : 0 , "madvise" : 0 , "shmget" : 0 , "shmat" : 0 , "shmctl" : 0 , "dup" : 0 , "dup2" : 0 , "pause" : 0 , "nanosleep" : 0 , "getitimer" : 0 , "alarm" : 0 , "setitimer" : 0 , "getpid" : 0 , "sendfile" : 0 , "socket" : 0 , "connect" : 0 , "accept" : 0 , "sendto" : 0 , "rt_sigaction" : 0 , "rt_sigprocmask" : 0 , "rt_sigreturn" : 0 , "ioctl" : 0 , "pread64" : 0 , "pwrite64" : 0 , "readv" : 0 , "writev" : 0 , "recvfrom" : 0 , "sendmsg" : 0 , "recvmsg" : 0 , "shutdown" : 0 , "bind" : 0 , "listen" : 0 , "getsockname" : 0 , "getpeername" : 0 , "socketpair" : 0 , "setsockopt" : 0 , "getsockopt" : 0 , "clone" : 0 , "fork" : 0 , "vfork" : 0 , "execve" : 0 , "exit" : 0 , "wait4" : 0 , "kill" : 0 , "uname" : 0 , "semget" : 0 , "semop" : 0 , "semctl" : 0 , "shmdt" : 0 , "msgget" : 0 , "msgsnd" : 0 , "msgrcv" : 0 , "msgctl" : 0 , "fcntl" : 0 , "flock" : 0 , "fsync" : 0 , "fdatasync" : 0 , "truncate" : 0 , "ftruncate" : 0 , "getdents" : 0 , "getcwd" : 0 , "chdir" : 0 , "fchdir" : 0 , "rename" : 0 , "mkdir" : 0 , "rmdir" : 0 , "creat" : 0 , "link" : 0 , "unlink" : 0 , "symlink" : 0 , "readlink" : 0 , "chmod" : 0 , "fchmod" : 0 , "chown" : 0 , "fchown" : 0 , "lchown" : 0 , "umask" : 0 , "gettimeofday" : 0 , "getrlimit" : 0 , "getrusage" : 0 , "sysinfo" : 0 , "times" : 0 , "getuid" : 0 , "syslog" : 0 , "getgid" : 0 , "setuid" : 0 , "setgid" : 0 , "geteuid" : 0 , "getegid" : 0 , "setpgid" : 0 , "getppid" : 0 , "getpgrp" : 0 , "setsid" : 0 , "setreuid" : 0 , "setregid" : 0 , "getgroups" : 0 , "setgroups" : 0 , "setresuid" : 0 , "getresuid" : 0 , "setresgid" : 0 , "getresgid" : 0 , "getpgid" : 0 , "setfsuid" : 0 , "setfsgid" : 0 , "getsid" : 0 , "capget" : 0 , "capset" : 0 , "ptrace" : 0 , "rt_sigpending" : 0 , "rt_sigtimedwait" : 0 , "rt_sigqueueinfo" : 0 , "sigaltstack" : 0 , "uselib" : 0 , "_sysctl" : 0 , "create_module" : 0 , "rt_sigsuspend" : 0 , "utime" : 0 , "mknod" : 0 , "personality" : 0 , "ustat" : 0 , "statfs" : 0 , "fstatfs" : 0 , "sysfs" : 0 , "getpriority" : 0 , "setpriority" : 0 , "sched_setparam" : 0 , "sched_getparam" : 0 , "sched_setscheduler" : 0 , "sched_getscheduler" : 0 , "sched_get_priority_max" : 0 , "sched_get_priority_min" : 0 , "sched_rr_get_interval" : 0 , "mlock" : 0 , "munlock" : 0 , "mlockall" : 0 , "munlockall" : 0 , "vhangup" : 0 , "modify_ldt" : 0 , "pivot_root" : 0 , "prctl" : 0 , "arch_prctl" : 0 , "adjtimex" : 0 , "setrlimit" : 0 , "chroot" : 0 , "sync" : 0 , "acct" : 0 , "settimeofday" : 0 , "mount" : 0 , "umount2" : 0 , "swapon" : 0 , "swapoff" : 0 , "reboot" : 0 , "sethostname" : 0 , "setdomainname" : 0 , "iopl" : 0 , "ioperm" : 0 , "init_module" : 0 , "delete_module" : 0 , "get_kernel_syms" : 0 , "query_module" : 0 , "nfsservctl" : 0 , "set_thread_area" : 0 , "io_setup" : 0 , "io_submit" : 0 , "get_thread_area" : 0 , "epoll_ctl_old" : 0 , "epoll_wait_old" : 0 , "timer_create" : 0 , "quotactl" : 0 , "getpmsg" : 0 , "putpmsg" : 0 , "afs_syscall" : 0 , "tuxcall" : 0 , "security" : 0 , "gettid" : 0 , "readahead" : 0 , "setxattr" : 0 , "lsetxattr" : 0 , "fsetxattr" : 0 , "getxattr" : 0 , "lgetxattr" : 0 , "fgetxattr" : 0 , "listxattr" : 0 , "llistxattr" : 0 , "flistxattr" : 0 , "removexattr" : 0 , "lremovexattr" : 0 , "fremovexattr" : 0 , "tkill" : 0 , "time" : 0 , "futex" : 0 , "sched_setaffinity" : 0 , "sched_getaffinity" : 0 , "io_destroy" : 0 , "io_getevents" : 0 , "io_cancel" : 0 , "lookup_dcookie" : 0 , "epoll_create" : 0 , "remap_file_pages" : 0 , "getdents64" : 0 , "set_tid_address" : 0 , "restart_syscall" : 0 , "semtimedop" : 0 , "fadvise64" : 0 , "timer_settime" : 0 , "timer_gettime" : 0 , "timer_getoverrun" : 0 , "timer_delete" : 0 , "clock_settime" : 0 , "clock_gettime" : 0 , "clock_getres" : 0 , "clock_nanosleep" : 0 , "exit_group" : 0 , "epoll_wait" : 0 , "epoll_ctl" : 0 , "tgkill" : 0 , "utimes" : 0 , "vserver" : 0 , "mq_notify" : 0 , "kexec_load" : 0 , "waitid" : 0 , "set_robust_list" : 0 , "get_robust_list" : 0 , "vmsplice" : 0 , "move_pages" : 0 , "mbind" : 0 , "set_mempolicy" : 0 , "get_mempolicy" : 0 , "mq_open" : 0 , "mq_unlink" : 0 , "mq_timedsend" : 0 , "mq_timedreceive" : 0 , "mq_getsetattr" : 0 , "add_key" : 0 , "request_key" : 0 , "keyctl" : 0 , "ioprio_set" : 0 , "ioprio_get" : 0 , "inotify_init" : 0 , "inotify_add_watch" : 0 , "inotify_rm_watch" : 0 , "migrate_pages" : 0 , "openat" : 0 , "mkdirat" : 0 , "mknodat" : 0 , "fchownat" : 0 , "futimesat" : 0 , "newfstatat" : 0 , "unlinkat" : 0 , "renameat" : 0 , "linkat" : 0 , "symlinkat" : 0 , "readlinkat" : 0 , "fchmodat" : 0 , "faccessat" : 0 , "pselect6" : 0 , "ppoll" : 0 , "unshare" : 0 , "splice" : 0 , "tee" : 0 , "sync_file_range" : 0 , "utimensat" : 0 , "epoll_pwait" : 0 , "signalfd" : 0 , "timerfd_create" : 0 , "eventfd" : 0 , "fallocate" : 0 , "timerfd_settime" : 0 , "timerfd_gettime" : 0 , "accept4" : 0 , "signalfd4" : 0 , "eventfd2" : 0 , "epoll_create1" : 0 , "dup3" : 0 , "pipe2" : 0 , "preadv" : 0 , "pwritev" : 0 , "rt_tgsigqueueinfo" : 0 , "recvmmsg" : 0 , "sendmmsg" : 0 , "process_vm_readv" : 0 , "process_vm_writev" : 0 , "execveat" : 0 , "preadv2" : 0 , "pwritev2" : 0 , "inotify_init1" : 0 , "perf_event_open" : 0 , "fanotify_init" : 0 , "fanotify_mark" : 0 , "prlimit64" : 0 , "name_to_handle_at" : 0 , "open_by_handle_at" : 0 , "clock_adjtime" : 0 , "syncfs" : 0 , "setns" : 0 , "getcpu" : 0 , "kcmp" : 0 , "finit_module" : 0 , "sched_setattr" : 0 , "sched_getattr" : 0 , "renameat2" : 0 , "seccomp" : 0 , "getrandom" : 0 , "memfd_create" : 0 , "kexec_file_load" : 0 , "bpf" : 0 , "userfaultfd" : 0 , "membarrier" : 0 , "mlock2" : 0 , "copy_file_range" : 0 , "pkey_mprotect" : 0 , "pkey_alloc" : 0 , "pkey_free" : 0 , "statx" : 0 , "io_pgetevents" : 0 , "rseq" : 0 , "pidfd_send_signal" : 0 , "io_uring_setup" : 0 , "io_uring_enter" : 0 , "io_uring_register" : 0 , "open_tree" : 0 , "move_mount" : 0 , "fsopen" : 0 , "fsconfig" : 0 , "fsmount" : 0 , "fspick" : 0 , "pidfd_open" : 0 , "clone3" : 0 , "close_range" : 0 , "openat2" : 0 , "pidfd_getfd" : 0 , "faccessat2" : 0 , "process_madvise" : 0 , "epoll_pwait2" : 0 , "mount_setattr" : 0 , "quotactl_fd" : 0 , "landlock_create_ruleset" : 0 , "landlock_add_rule" : 0 , "landlock_restrict_self" : 0 , "memfd_secret" : 0 , "process_mrelease" : 0 , "futex_waitv" : 0 , "set_mempolicy_home_node" : 0 , "cachestat" : 0
}
PAIRLESS = ['clone', 'exit', 'accept', 'poll', 'exit_group']

WINDOW_SIZE = 0
N_NEIGHBORS = 3

LABEL_MULT_NORMAL = 0
LABEL_MULT_ANORMAL = 1

LABEL_ONE_NORMAL = 1
LABEL_ONE_ANORMAL = -1

RUNS = 10

FILES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../wordpress", "{v}", "{b}")


def sliding_window_filter(input_file):
    result = ()
    def add_to_result(elem):
        if ("threat" in syscalls[elem.split(" ")[0]]):
            if syscall[elem.split(" ")[0]] == 1:
                syscall[elem.split(" ")[0]] = 0
                return
            if (syscalls[elem.split(" ")[0]]["threat"] != 4 and syscalls[elem.split(" ")[0]]["threat"] != 5):
                result = result + (syscalls[elem.split(" ")[0]]["id"],)
                if syscall not in PAIRLESS:
                    syscall[elem.split(" ")[0]] = 1
        else:
            raise Exception(f"Threat para {elem.split(' ')[0]} não encontrada")

    it = iter(input_file)
    for elem in islice(it, WINDOW_SIZE):
        add_to_result(elem)
    if len(result) == WINDOW_SIZE:
        yield result
    for elem in it:
        result = result[1:]
        add_to_result(elem)
        yield result

def sliding_window_raw(seq):
    result = ()
    def add_to_result(elem):
        if syscall[elem.split(" ")[0]] == 1:
            syscall[elem.split(" ")[0]] = 0
            return
        result += (syscalls[elem.split(" ")[0]]["id"],)
        if syscall not in PAIRLESS:
            syscall[elem.split(" ")[0]] = 1

    it = iter(seq)
    for elem in islice(it, WINDOW_SIZE):
        add_to_result(elem)
    if len(result) == WINDOW_SIZE:
        yield result
    for elem in it:
        result = result[1:]
        add_to_result(elem)
        yield result


def retrieve_dataset(filename, filter):

    with open(filename, "r") as input_file:
        if filter == "raw":
            dataset = list(sliding_window_raw(input_file))
        else:
            dataset = list(sliding_window_filter(input_file))

    return dataset


def define_labels(base_normal, base_exec, multi):
    labels = []

    label_normal = LABEL_MULT_NORMAL if multi else LABEL_ONE_NORMAL
    label_anormal = LABEL_MULT_ANORMAL if multi else LABEL_ONE_ANORMAL

    for window in base_normal:
        labels.append(label_normal)

    for window in base_exec:
        labels.append(label_anormal)

    return labels


def get_features(version, filter="raw"):

    path = FILES_PATH.format(v=version, b="normal/sysdig")
    base_normal = []
    base_exec = []

    for file in os.listdir(path):
        base_normal.extend(retrieve_dataset(os.path.join(path, file), filter))

    path = FILES_PATH.format(v=version, b="anormal/sysdig")

    for file_exec in os.listdir(path):
        base_exec.extend(retrieve_dataset(os.path.join(path, file_exec), filter))

    return base_normal, base_exec


def naive_bayes(base_normal, base_exec):

    print("\n> Naive Bayes")

    results = []

    print("[...] Retrieving datasets and labels")
    labels = define_labels(base_normal, base_exec, True)
    features = base_normal + base_exec

    for i in range(RUNS):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=2**i)

        gnb = GaussianNB()
        gnb.fit(X_train, y_train)
        y_pred = gnb.predict(X_test)

        score = (precision_score(y_test, y_pred, average="binary"), recall_score(y_test, y_pred, average="binary"), f1_score(y_test, y_pred, average="binary"), accuracy_score(y_test, y_pred))
        results.append(list(score))

    results = np.mean(results, axis=0)

    print("precision_score:", results[0])
    print("recall_score:", results[1])
    print("f1_score:", results[2])
    print("accuracy_score:", results[3])
    print("")

    return


def kneighbors(base_normal, base_exec):

    print("\n> K-Nearest Neighbors")

    results = []

    print("N_NEIGHBORS", str(N_NEIGHBORS))

    print("[...] Retrieving datasets and labels")
    labels = define_labels(base_normal, base_exec, True)
    features = base_normal + base_exec

    for i in range(RUNS):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=2**i)

        knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS, n_jobs=-1)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)

        score = (precision_score(y_test, y_pred, average="binary"), recall_score(y_test, y_pred, average="binary"), f1_score(y_test, y_pred, average="binary"), accuracy_score(y_test, y_pred))
        results.append(list(score))

    results = np.mean(results, axis=0)

    print("precision_score:", results[0])
    print("recall_score:", results[1])
    print("f1_score:", results[2])
    print("accuracy_score:", results[3])
    print("")

    return


def random_forest(base_normal, base_exec):

    print("\n> Random Forest")

    results = []

    print("[...] Retrieving datasets and labels")
    labels = define_labels(base_normal, base_exec, True)
    features = base_normal + base_exec

    for i in range(RUNS):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=2**i)

        rfc = RandomForestClassifier(n_estimators=100, n_jobs=-1)

        rfc.fit(X_train, y_train)
        y_pred = rfc.predict(X_test)

        score = (precision_score(y_test, y_pred, average="binary"), recall_score(y_test, y_pred, average="binary"), f1_score(y_test, y_pred, average="binary"), accuracy_score(y_test, y_pred))
        results.append(list(score))

    results = np.mean(results, axis=0)

    print("precision_score:", results[0])
    print("recall_score:", results[1])
    print("f1_score:", results[2])
    print("accuracy_score:", results[3])
    print("")

    return


def ada_boost(base_normal, base_exec):
    print("\n> Ada Boost")

    results = []

    print("[...] Retrieving datasets and labels")
    labels = define_labels(base_normal, base_exec, True)
    features = base_normal + base_exec

    for i in range(RUNS):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=2**i)

        abc = AdaBoostClassifier(base_estimator=RandomForestClassifier(n_jobs=-1))
        abc.fit(X_train, y_train)
        y_pred = abc.predict(X_test)

        score = (precision_score(y_test, y_pred, average="binary"), recall_score(y_test, y_pred, average="binary"), f1_score(y_test, y_pred, average="binary"), accuracy_score(y_test, y_pred))
        results.append(list(score))

    results = np.mean(results, axis=0)

    print("precision_score:", results[0])
    print("recall_score:", results[1])
    print("f1_score:", results[2])
    print("accuracy_score:", results[3])
    print("")

    return


def multilayer_perceptron(base_normal, base_exec):
    print("\n> Multilayer Perceptron")

    results = []

    print("[...] Retrieving datasets and labels")
    labels = define_labels(base_normal, base_exec, True)
    features = base_normal + base_exec

    for i in range(RUNS):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=2**i)

        mlp = MLPClassifier()
        mlp.fit(X_train, y_train)
        y_pred = mlp.predict(X_test)

        score = (precision_score(y_test, y_pred, average="binary"), recall_score(y_test, y_pred, average="binary"), f1_score(y_test, y_pred, average="binary"), accuracy_score(y_test, y_pred))
        results.append(list(score))

    results = np.mean(results, axis=0)

    print("precision_score:", results[0])
    print("recall_score:", results[1])
    print("f1_score:", results[2])
    print("accuracy_score:", results[3])
    print("")

    return


# def linear_svc():
#     print("\n> Linear SVC")
#
#     print("\n[...] Retrieving datasets and labels")
#     features,labels = get_features_labels()
#
#     X_train,X_test,y_train,y_test = train_test_split(features, labels, test_size=0.5, random_state=42)
#
#     lsvc = SVC()
#
#     lsvc.fit(X_train, y_train)
#     y_pred = lsvc.predict(X_test)
#
#     print("\nf1_score: ", f1_score(y_test, y_pred, average="binary"))
#     print("\nrecall_score: ", recall_score(y_test, y_pred, average="binary"))
#     print("\nprecision_score: ", precision_score(y_test, y_pred, average="binary"))
#     print("\n")
#
#     return lsvc

def one_class_svm(base_normal, base_exec):
    print("\n> One Class SVM")

    results = []

    print("[...] Retrieving datasets and labels")
    labels = define_labels(base_normal, base_exec, False)
    features = base_normal + base_exec

    for i in range(RUNS):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=2**i)

        onesvm = OneClassSVM(gamma="scale", nu=0.01)
        trainX = []
        for x, y in zip(X_train, y_train):
            if (y == 1):
                trainX.append(x)

        onesvm.fit(trainX)
        y_pred = onesvm.predict(X_test)

        score = (precision_score(y_test, y_pred, average="binary", pos_label=-1), recall_score(y_test, y_pred, average="binary", pos_label=-1), f1_score(y_test, y_pred, average="binary", pos_label=-1), accuracy_score(y_test, y_pred))
        results.append(list(score))

    results = np.mean(results, axis=0)

    print("precision_score:", results[0])
    print("recall_score:", results[1])
    print("f1_score:", results[2])
    print("accuracy_score:", results[3])
    print("")

    return


def isolation_forest(base_normal, base_exec):

    print("\n> Isolation Forest")

    results = []

    print("[...] Retrieving datasets and labels")
    labels = define_labels(base_normal, base_exec, False)
    features = base_normal + base_exec

    for i in range(RUNS):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=2**i)

        clf = IsolationForest(n_jobs=-1)
        trainX = []
        for x, y in zip(X_train, y_train):
            if (y == 1):
                trainX.append(x)

        clf.fit(trainX)
        y_pred = clf.predict(X_test)

        score = (precision_score(y_test, y_pred, average="binary", pos_label=-1), recall_score(y_test, y_pred, average="binary", pos_label=-1), f1_score(y_test, y_pred, average="binary", pos_label=-1), accuracy_score(y_test, y_pred))
        results.append(list(score))

    results = np.mean(results, axis=0)

    print("precision_score:", results[0])
    print("recall_score:", results[1])
    print("f1_score:", results[2])
    print("accuracy_score:", results[3])
    print("")

    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("window_size", help="Window size", type=int)
    parser.add_argument("-d", "--dataset", help="Dataset version to use", choices=["logs"], default="logs")
    parser.add_argument("-f", "--filter", help="Filter mode", choices=["raw", "filter"], default="raw")
    args = parser.parse_args()

    if args.window_size <= 0:
        raise argparse.ArgumentTypeError("window_size must be greater than 0")

    WINDOW_SIZE = args.window_size

    print(" ".join(("\n --- WINDOW_SIZE =", str(WINDOW_SIZE), "({}) --- \n".format(args.filter))))

    base_normal, base_exec = get_features(args.dataset, args.filter)

    # naive_bayes(base_normal, base_exec)
    # kneighbors(base_normal, base_exec)
    random_forest(base_normal, base_exec)
    multilayer_perceptron(base_normal, base_exec)
    # ada_boost(base_normal, base_exec)

    one_class_svm(base_normal, base_exec)
    isolation_forest(base_normal, base_exec)
