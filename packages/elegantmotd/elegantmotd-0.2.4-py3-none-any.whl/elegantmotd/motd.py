import os
import platform
import re
from datetime import datetime, timezone

from art import text2art
from rich.console import Console
from rich.style import Style
from rich.table import Table

from .cpu import CPU
from .disk import Disk
from .load import Load
from .loggedinusers import LoggedInUsers
from .memory import Memory
from .network import Network
from .process import Process
from .temperature import Temperature


def get_distro_info():
    try:
        with open("/etc/lsb-release") as f:
            content = f.read()
        release_info = dict(re.findall(r'(\w+)=(.*)', content))
        distro = f"{release_info['DISTRIB_ID']} {release_info['DISTRIB_RELEASE']}"
        codename = release_info['DISTRIB_CODENAME']
    except FileNotFoundError:
        distro = "Unknown"
        codename = "unknown"

    return distro, codename


def get_kernel_info():
    return platform.release()


def get_architecture():
    return platform.machine()


def display():
    distro, codename = get_distro_info()
    kernel = get_kernel_info()
    architecture = get_architecture()

    console = Console()
    console.print(f"💻 [blue bold]{distro} {codename} LTS (GNU/Linux {kernel} {architecture}) [/]💻")
    console.print(f"[orange1 bold]{text2art(os.getlogin(), font='small')}[/]", end="")
    local_time = datetime.now(timezone.utc).astimezone()
    utc_offset = round(local_time.utcoffset().total_seconds() / 3600)
    table = Table(
        show_header=False,
        box=None,
        title_justify="left",
        title=f"  System information as of {local_time.strftime('%a. %d %B %Y %H:%M:%S')} UTC+{utc_offset}\n",
        title_style=Style(color="white", italic=False, bold=True, ),
        expand=True,
        leading=1,
        padding=(0, 2)
    )

    table.add_column("Info", style="bold CYAN")
    table.add_column("Value", style="bold WHITE")

    sysinfos = [Load(), Disk(), Memory(), Temperature(), Process(), LoggedInUsers(), Network(), CPU()]

    [table.add_row(f"{info}:", sysinfo.infos[info]) for sysinfo in sysinfos for info in sysinfo.infos]

    console.print(table)
    console.print()
