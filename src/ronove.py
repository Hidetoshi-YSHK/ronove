from singleton import Singleton

class Ronove(Singleton):

    def __init__(self) -> None:
        super().__init__()
        print("init")

    pass
