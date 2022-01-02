import ronove
import gui
import database
import singleton

class Main(singleton.Singleton):
    def initialize(self) -> None:
        Ronove = ronove.Ronove
        Gui = gui.Gui
        Database = database.Database
        self.ronove = Ronove.get_instance()
        self.database = Database.get_instance()
        self.database.initialize(self.ronove.get_db_file_path())
        self.gui = Gui.get_instance()
        self.gui.initialize()

    def main(self) -> None:
        self.ronove.on_app_start()
        self.gui.mainloop()

if __name__ == '__main__':
    main = Main.get_instance()
    main.initialize()
    main.main()
