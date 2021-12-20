import ronove;
import gui;
import database;
import singleton;

class Main(singleton.Singleton):
    def __init__(self) -> None:
        Ronove = ronove.Ronove
        Gui = gui.Gui
        Database = database.Database
        self.ronove = Ronove.get_instance()
        self.gui = Gui.get_instance()
        self.database = Database.get_instance()
        self.database.initialize(self.ronove.get_db_file_path())

    def main(self) -> None:
        self.gui.mainloop()

if __name__ == '__main__':
    Main.get_instance().main()
