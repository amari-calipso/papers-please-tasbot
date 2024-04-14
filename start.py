import json
import logging.config
import os
import pathlib

import win32com
import win32gui

from tas import TAS, Run

logger = logging.getLogger('tas.' + __name__)
log_config_path = os.path.join(TAS.PROGRAM_DIR, 'config', 'logging_config.json')
with open(log_config_path) as f:
    config = json.load(f)
logging.config.dictConfig(config)

tas = TAS()

# import all runs
for module in os.listdir(pathlib.Path('./runs')):
    if module.endswith(".py"):
        __import__(f"runs.{module[:-3]}", locals(), globals())

RUNS = []
for RunSubclass in Run.__subclasses__():
    logger.info(f'Initializing Run "{RunSubclass.__name__}"...')
    RunSubclass.TAS = TAS
    inst = RunSubclass()
    inst.tas = tas
    RUNS.append(inst)


def run():
    while True:
        i = TAS.select("Select run:", [run.__class__.__name__ for run in RUNS])
        act = TAS.select("Select action:", ["Run", "Test", "View credits"])

        if act in (0, 1):
            tas.hwnd = tas.getWinHWDN()
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(tas.hwnd)

        match act:
            case 0:
                RUNS[i].run()
            case 1:
                RUNS[i].test()
            case 2:
                print(RUNS[i].credits())


if __name__ == '__main__':
    run()