import types

class PipelineException(Exception):
    pass

class InvalidArgumentException(PipelineException):
    pass

class Pipeline(object):

    methods = {}

    @classmethod
    def register(cls, func):
        cls.methods[func.__name__] = func
        return func

    def __init__(self):
        super(Pipeline, self).__init__()
        self.gen = []

    def __getattr__(self, name):
        if name not in self.methods:
            raise AttributeError

        def inner(self, *args, **kwargs):
            self.gen = self.methods[name](self.gen, *args, **kwargs)
            return self
        return types.MethodType(inner, self)        

    def __len__(self):
        return self.gen.__len__()

    def __iter__(self):
        return self.gen.__iter__()

    @classmethod
    def _getfn(cls, fn):
        if isinstance(fn, types.FunctionType):
            return fn
        if fn in cls.methods:
            return cls.methods[fn]
        raise InvalidArgumentException

@Pipeline.register
def map(lst, fn, *args, **kwargs):
    return (fn(elm, *args, **kwargs) for elm in lst)

@Pipeline.register
def filter(lst, fn, *args, **kwargs):
    return (elm for elm in lst if fn(elm, *args, **kwargs))

@Pipeline.register
def take(lst, count, start=0, step=1):
    for i in range(start):
        next(lst)
    for i in range(count):
        yield next(lst)
        for i in range(step-1):
            next(lst)

