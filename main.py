try:
    import tkinter
    from gui import run_gui
    GUI_AVAILABLE = True
except ImportError:
    from cli import run_cli
    GUI_AVAILABLE = False


if __name__ == "__main__":
    if GUI_AVAILABLE:
        run_gui()
    else:
        print("Tkinter niedostępny — uruchamiam tryb konsolowy.")
        run_cli()