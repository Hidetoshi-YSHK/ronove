from threading import Lock

class Singleton:
    _singleton_lock = Lock()
    _subclass_lock = None
    _subclass_instance = None

    def __new__(cls):
        raise NotImplementedError("Not allowed. Use get_instance().")

    @classmethod
    def __private_new__(cls):
        instance = super().__new__(cls)
        instance.__init__()
        return instance

    @classmethod
    def get_instance(cls):
        # Create a lock for subclass
        if cls._subclass_lock is None:
            with Singleton._singleton_lock:
                if cls._subclass_lock is None:
                    cls._subclass_lock = Lock()

        # Create a subclass instance
        if cls._subclass_instance is None:
            with cls._subclass_lock: 
                if cls._subclass_instance is None:
                    cls._subclass_instance = cls.__private_new__()

        return cls._subclass_instance
