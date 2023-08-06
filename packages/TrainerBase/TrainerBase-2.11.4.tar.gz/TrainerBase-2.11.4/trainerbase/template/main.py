from os import _exit as force_exit

from scripts import script_engine, system_script_engine
from gui import run_menu

from injections import *


def on_initialized():
    system_script_engine.start()
    script_engine.start()


def on_shutdown():
    system_script_engine.stop()
    script_engine.stop()


def main():
    run_menu(on_initialized=on_initialized)
    on_shutdown()
    force_exit(0)


if __name__ == "__main__":
    main()
