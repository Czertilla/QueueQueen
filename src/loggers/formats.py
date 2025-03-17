from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from colorama import Fore, Style, Back

cb = lambda x: Fore.BLUE + x + Fore.RESET
cg = lambda x: Fore.GREEN + x + Fore.RESET
cr = lambda x: Fore.RED + x + Fore.RESET
cc = lambda x: Fore.CYAN + x + Fore.RESET
cy = lambda x: Fore.YELLOW + x + Fore.RESET
cm = lambda x: Fore.MAGENTA + x + Fore.RESET
br = lambda x: Back.RED + x + Back.RESET
c_ = Fore.RESET
s_ = Style.RESET_ALL
sb = lambda x: Style.BRIGHT + x + Style.NORMAL
act = cg("%(asctime)s")
prc = f"[{cc('%(process)s')}]"
lvl = "%(levelname)-8s"
loc = f"{cm('%(name)s')}:{cb('%(funcName)s')}:{cc('%(lineno)s')}"
msg = "%(message)s"
exc = cr("%(exc_info)s")

FORMATS = {
    DEBUG: f"{act} {prc} {cb(lvl)} | {loc} - {msg}",
    INFO: f"{act} {prc} {cg(lvl)} | {loc} - {msg}",
    WARNING: f"{act} {prc} {cy(lvl)} | {loc} - {cy(msg)}",
    ERROR: f"{act} {prc} {cr(lvl)} | {loc} - {cr(msg)} || {exc}",
    CRITICAL: f"{act} {prc} {sb(br(lvl))} | {loc} - {sb(cr(msg))} || {exc}",
}
