import os.path as path
import sys
from database import Database
import gui

class Main:
    DB_FILE_NAME = "data.db"

    def __init__(self) -> None:
        self.gui = gui.Gui(self)
        self.database = Database(
            path.join(self.get_exe_dir(), self.DB_FILE_NAME))

    def main(self) -> None:
        self.gui.mainloop()

    def get_exe_dir(self) -> str:
        return path.dirname(path.abspath(sys.argv[0]))

if __name__ == '__main__':
    Main().main()