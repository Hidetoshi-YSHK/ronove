"""
from ronove import Ronove
from gui import Gui
from database import Database
from singleton import Singleton
"""
import ronove
Ronove = ronove.Ronove
import gui
Gui = gui.Gui
import database
Database = database.Database
import singleton
Singleton = singleton.Singleton


class Main(Singleton):
    def __init__(self) -> None:
        self.ronove = Ronove.get_instance()
        self.gui = Gui.get_instance()
        self.database = Database.get_instance()
        self.database.initialize(self.ronove.get_db_file_path())

    def main(self) -> None:
        self.gui.mainloop()

if __name__ == '__main__':
    Main.get_instance().main()
