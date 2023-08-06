# -*- coding: utf-8 -*-

from ..win32.functions import GetProcessIdByWindowTitle
import psutil


def get_process_id_by_process_name(process_name: str) -> int:
    """
    Get a process name and return its process ID.
    """
    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid


def get_process_id_by_window_title(window_title: str) -> int:
    """
    Get a window title and return its process ID.
    """
    return GetProcessIdByWindowTitle(window_title)


def pid_exists(pid: int) -> bool:
    """
    Check if the process ID exists.
    """
    return psutil.pid_exists(pid)
