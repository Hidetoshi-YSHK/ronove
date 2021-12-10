import os
import os.path as path
import sys

class Main:
    def __init__(self) -> None:
        pass

    def main(self) -> None:
        print(self.get_exe_dir())
        pass

    def get_exe_dir(self) -> str:
        return path.dirname(path.abspath(sys.argv[0]))

Main().main()