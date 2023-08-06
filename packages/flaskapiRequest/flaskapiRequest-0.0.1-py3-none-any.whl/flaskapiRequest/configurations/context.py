class Context(type):

    def content(cls):
        return {key: value for key, value in cls.__dict__.items()
                if not key.startswith('_') and key != 'content'}

    def __getattr__(cls, item):
        return cls.__dict__[item]

    def __setattr__(cls, key, value):
        cls.__dict__[key] = value