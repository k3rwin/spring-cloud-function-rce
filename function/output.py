import time
from colorama import Fore,init

init(autoreset=True)
def suc_p(s):
    print(Fore.GREEN + "[%s][√]" % time.strftime("%H:%M:%S", time.localtime()) + s)


def info_p(s):
    print(Fore.YELLOW + "[%s][*]" % time.strftime("%H:%M:%S", time.localtime()) + s)


def fail_p(s):
    print(Fore.RED + "[%s][×]" % time.strftime("%H:%M:%S", time.localtime()) + s)

# info_p("info")