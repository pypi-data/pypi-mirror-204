import platform
import socket
import os
import psutil
import sys
import time
import locale
from typing import Dict


class GetSystemInfo:
    """
    A class used to represent the System Information.

    ...

    Attributes
    ----------
    info : Dict[str, str]
        a dictionary containing various system information

    Methods
    -------
    get_system_info() -> Dict[str, str]:
        Returns a dictionary containing various system information.
    display_info():
        Prints the system information stored in the info attribute.
    """

    def __init__(self):
        self.info: Dict[str, str] = self.get_system_info()

    def get_system_info(self) -> Dict[str, str]:
        """
        Collects various system information and stores them in a dictionary.

        Returns
        -------
        Dict[str, str]
            A dictionary containing the following keys and their respective values:
            - os: Operating System name
            - os_version: Operating System version
            - architecture: System architecture
            - hostname: Hostname of the system
            - platform: Platform string
            - processor: Processor information
            - python_version: Python interpreter version
            - python_compiler: Python compiler information
            - num_cpu_cores: Number of CPU cores
            - total_memory: Total memory available in bytes
            - max_int_size: Maximum size of integers the interpreter can handle
            - current_time: Current local time as a string
            - default_encoding: Default encoding used by the system
            - default_locale: Default locale tuple (language code, encoding)
        """
        info = dict()
        _ = {
            'os': platform.system,
            'os_version': platform.version,
            'architecture': platform.machine,
            'hostname': socket.gethostname,
            'platform': platform.platform,
            'processor': platform.processor,
            'python_version': platform.python_version,
            'python_compiler': platform.python_compiler,
            'num_cpu_cores': os.cpu_count,
            'total_memory': psutil.virtual_memory,
            'max_int_size': sys.maxsize,
            'current_time': time.asctime,
            'current_user': os.getlogin,
            'default_encoding': sys.getdefaultencoding,
            'default_locale': locale.getdefaultlocale,
        }
        for k, v in _.items():
            try:
                if k == 'total_memory':
                    info[k] = v().total
                elif k == 'max_int_size':
                    info[k] = v
                else:
                    info[k] = v()
            except:
                info[k] = None
        return info

    def display_info(self) -> None:
        """Prints the system information stored in the info attribute."""
        for key, value in self.info.items():
            print(f"{key}: {value}")