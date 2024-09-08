class SingletonMixin(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonMixin, cls).__new__(cls)
        return cls.instance
