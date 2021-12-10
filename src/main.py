import os.path as path
import sys
import gui

class Main:
    def __init__(self) -> None:
        self.gui = gui.Gui(self)

    def main(self) -> None:
        print(self.get_exe_dir())
        self.gui.mainloop()

    def get_exe_dir(self) -> str:
        return path.dirname(path.abspath(sys.argv[0]))

if __name__ == '__main__':
    Main().main()