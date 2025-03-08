class SingletonMixin(object):
    """
    Mixin class that implements the Singleton pattern.

    Ensures that only one instance of the class is created.
    """

    def __new__(cls):
        """
        Overrides the __new__ method to implement the Singleton pattern.

        If an instance of the class does not exist, it creates one. Otherwise,
        it returns the existing instance.

        Returns:
            The singleton instance of the class.
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonMixin, cls).__new__(cls)
        return cls.instance
