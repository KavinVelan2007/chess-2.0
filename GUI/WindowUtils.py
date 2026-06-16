import os
import platform
from tkinter import TclError


def maximize_window(window):
    def apply_maximize():
        if os.environ.get("RUNNING_IN_DOCKER") == "1":
            width = window.winfo_screenwidth()
            height = window.winfo_screenheight()
            window.geometry(f"{width}x{height}+0+0")
            return

        try:
            window.state("zoomed")
            return
        except TclError:
            pass

        try:
            window.attributes("-zoomed", True)
            return
        except TclError:
            pass

        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        window.geometry(f"{width}x{height}+0+0")

    window.after(0, apply_maximize)
