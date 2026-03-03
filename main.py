import sys
import traceback
import gui


def exception_hook(exc_type, exc_value, exc_tb):
    traceback.print_exception(exc_type, exc_value, exc_tb)
    sys.exit(1)


sys.excepthook = exception_hook

gui.run_gui()


# CANT INPUT IN USERNAME THEN