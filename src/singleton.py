import threading

class Singleton:
    _singleton_instance = None
    _singleton_lock = threading.Lock()

    def __new__(cls):
        raise NotImplementedError("Not allowed. Use get_instance().")

    @classmethod
    def __private_new__(cls):
        instance = super().__new__(cls)
        instance.__init__()
        return instance

    @classmethod
    def get_instance(cls):
        if cls._singleton_instance is None:
            with cls._singleton_lock: 
                if cls._singleton_instance is None:
                    cls._singleton_instance = cls.__private_new__()

        return cls._singleton_instance
